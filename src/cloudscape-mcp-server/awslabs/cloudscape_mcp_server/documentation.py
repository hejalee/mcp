"""Cloudscape documentation search functionality."""

import httpx
import re
from .models import CloudscapeDocResult, ComponentInfo, DesignToken
from bs4 import BeautifulSoup
from loguru import logger
from markdownify import markdownify as md
from typing import List, Optional
from urllib.parse import urljoin, urlparse


class CloudscapeDocumentationSearcher:
    """Search and retrieve Cloudscape design system documentation."""

    def __init__(self):
        """Initialize the documentation searcher."""
        self.base_url = 'https://cloudscape.design'
        self.client = httpx.Client(timeout=30.0)

    async def search_documentation(
        self, query: str, max_results: int = 10
    ) -> List[CloudscapeDocResult]:
        """Search Cloudscape documentation for relevant content."""
        try:
            # For now, we'll implement a basic search by crawling key pages
            # In a production version, you might want to use a proper search API
            search_results = []

            # Define key documentation sections to search
            sections = ['/components/', '/foundation/', '/patterns/', '/get-started/']

            for section in sections:
                section_results = await self._search_section(
                    section, query, max_results // len(sections)
                )
                search_results.extend(section_results)

            # Sort by relevance (basic keyword matching for now)
            search_results.sort(
                key=lambda x: self._calculate_relevance(x.content, query), reverse=True
            )

            return search_results[:max_results]

        except Exception as e:
            logger.error(f'Error searching documentation: {e}')
            return []

    async def get_component_documentation(self, component_name: str) -> Optional[ComponentInfo]:
        """Get detailed documentation for a specific Cloudscape component."""
        try:
            # Construct component URL
            component_url = f'{self.base_url}/components/{component_name.lower()}/'

            response = self.client.get(component_url)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract component information
            name = component_name
            description = self._extract_description(soup)
            props = self._extract_props(soup)
            examples = self._extract_examples(soup)
            related_components = self._extract_related_components(soup)

            return ComponentInfo(
                name=name,
                description=description,
                props=props,
                examples=examples,
                related_components=related_components,
            )

        except Exception as e:
            logger.error(f'Error getting component documentation for {component_name}: {e}')
            return None

    async def get_design_tokens(self, category: Optional[str] = None) -> List[DesignToken]:
        """Get Cloudscape design tokens."""
        try:
            tokens_url = f'{self.base_url}/foundation/visual-foundation/design-tokens/'

            response = self.client.get(tokens_url)
            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            tokens = self._extract_design_tokens(soup, category)

            return tokens

        except Exception as e:
            logger.error(f'Error getting design tokens: {e}')
            return []

    async def _search_section(
        self, section: str, query: str, max_results: int
    ) -> List[CloudscapeDocResult]:
        """Search within a specific documentation section."""
        try:
            section_url = urljoin(self.base_url, section)
            response = self.client.get(section_url)

            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links within this section
            links = soup.find_all('a', href=True)
            results = []

            for link in links[:max_results]:
                href = link.get('href')
                if not href or not href.startswith('/'):
                    continue

                page_url = urljoin(self.base_url, href)
                page_result = await self._search_page(page_url, query)

                if page_result and self._is_relevant(page_result.content, query):
                    results.append(page_result)

            return results

        except Exception as e:
            logger.error(f'Error searching section {section}: {e}')
            return []

    async def _search_page(self, url: str, query: str) -> Optional[CloudscapeDocResult]:
        """Search a specific page for relevant content."""
        try:
            response = self.client.get(url)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text().strip() if title_elem else 'Untitled'

            # Extract main content
            content_elem = soup.find('main') or soup.find('article') or soup.find('body')
            if content_elem:
                # Convert to markdown for better readability
                content = md(str(content_elem))
                # Clean up the content
                content = re.sub(r'\n\s*\n', '\n\n', content).strip()
            else:
                content = ''

            # Determine component type if applicable
            component_type = self._extract_component_type(url, soup)

            return CloudscapeDocResult(
                title=title,
                url=url,
                content=content[:2000],  # Limit content length
                component_type=component_type,
            )

        except Exception as e:
            logger.error(f'Error searching page {url}: {e}')
            return None

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract component description from the page."""
        # Look for description in common locations
        desc_selectors = ['.component-description', '.description', 'p:first-of-type', '.lead']

        for selector in desc_selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()

        return 'No description available'

    def _extract_props(self, soup: BeautifulSoup) -> List[str]:
        """Extract component props from the documentation."""
        props = []

        # Look for props table or list
        props_section = soup.find('section', {'id': 'props'}) or soup.find('div', class_='props')
        if props_section:
            # Extract from table
            table = props_section.find('table')
            if table:
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        prop_name = cells[0].get_text().strip()
                        props.append(prop_name)

        return props

    def _extract_examples(self, soup: BeautifulSoup) -> List[str]:
        """Extract code examples from the documentation."""
        examples = []

        # Look for code blocks
        code_blocks = soup.find_all(['pre', 'code'])
        for block in code_blocks:
            code = block.get_text().strip()
            if len(code) > 20:  # Filter out small snippets
                examples.append(code)

        return examples[:5]  # Limit to 5 examples

    def _extract_related_components(self, soup: BeautifulSoup) -> List[str]:
        """Extract related components from the documentation."""
        related = []

        # Look for related components section
        related_section = soup.find('section', string=re.compile(r'related', re.I))
        if related_section:
            links = related_section.find_all('a')
            for link in links:
                component_name = link.get_text().strip()
                if component_name:
                    related.append(component_name)

        return related

    def _extract_design_tokens(
        self, soup: BeautifulSoup, category: Optional[str] = None
    ) -> List[DesignToken]:
        """Extract design tokens from the design tokens page."""
        tokens = []

        # This would need to be customized based on the actual structure
        # of the Cloudscape design tokens page
        token_sections = soup.find_all('section', class_='token-section')

        for section in token_sections:
            section_title = section.find('h2', 'h3')
            token_category = section_title.get_text().strip() if section_title else 'unknown'

            if category and category.lower() not in token_category.lower():
                continue

            # Extract individual tokens
            token_items = section.find_all('div', class_='token-item')
            for item in token_items:
                name_elem = item.find('.token-name')
                value_elem = item.find('.token-value')
                desc_elem = item.find('.token-description')

                if name_elem and value_elem:
                    tokens.append(
                        DesignToken(
                            name=name_elem.get_text().strip(),
                            value=value_elem.get_text().strip(),
                            category=token_category,
                            description=desc_elem.get_text().strip() if desc_elem else None,
                        )
                    )

        return tokens

    def _extract_component_type(self, url: str, soup: BeautifulSoup) -> Optional[str]:
        """Extract component type from URL or page content."""
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')

        if 'components' in path_parts:
            idx = path_parts.index('components')
            if idx + 1 < len(path_parts):
                return path_parts[idx + 1]

        return None

    def _calculate_relevance(self, content: str, query: str) -> float:
        """Calculate relevance score for search results."""
        if not content or not query:
            return 0.0

        content_lower = content.lower()
        query_lower = query.lower()

        # Simple keyword matching
        query_words = query_lower.split()
        matches = sum(1 for word in query_words if word in content_lower)

        return matches / len(query_words) if query_words else 0.0

    def _is_relevant(self, content: str, query: str, threshold: float = 0.1) -> bool:
        """Check if content is relevant to the query."""
        return self._calculate_relevance(content, query) >= threshold

    def __del__(self):
        """Clean up HTTP client."""
        if hasattr(self, 'client'):
            self.client.close()

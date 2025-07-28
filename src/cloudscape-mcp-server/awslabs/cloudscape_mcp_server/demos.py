"""Cloudscape demos repository search functionality."""

import git
import re
import tempfile
from .models import CloudscapeDemoResult
from loguru import logger
from pathlib import Path
from typing import List, Optional


class CloudscapeDemosSearcher:
    """Search and analyze Cloudscape demos repository."""

    def __init__(self):
        """Initialize the demos searcher."""
        self.repo_url = 'https://github.com/cloudscape-design/demos.git'
        self.repo_path: Optional[Path] = None
        self._ensure_repo()

    def _ensure_repo(self):
        """Ensure the demos repository is cloned and up to date."""
        try:
            # Use a temporary directory for the repo
            temp_dir = tempfile.mkdtemp(prefix='cloudscape_demos_')
            self.repo_path = Path(temp_dir)

            logger.info(f'Cloning Cloudscape demos repository to {self.repo_path}')
            git.Repo.clone_from(self.repo_url, self.repo_path, depth=1)

        except Exception as e:
            logger.error(f'Error cloning repository: {e}')
            self.repo_path = None

    async def search_demos(self, query: str, max_results: int = 10) -> List[CloudscapeDemoResult]:
        """Search through demo files for relevant examples."""
        if not self.repo_path or not self.repo_path.exists():
            logger.error('Repository not available')
            return []

        try:
            results = []

            # Search through common demo file types
            file_patterns = ['*.tsx', '*.ts', '*.jsx', '*.js', '*.json']

            for pattern in file_patterns:
                for file_path in self.repo_path.rglob(pattern):
                    if self._should_skip_file(file_path):
                        continue

                    demo_result = await self._search_file(file_path, query)
                    if demo_result and self._is_relevant(demo_result.content, query):
                        results.append(demo_result)

            # Sort by relevance
            results.sort(key=lambda x: self._calculate_relevance(x.content, query), reverse=True)

            return results[:max_results]

        except Exception as e:
            logger.error(f'Error searching demos: {e}')
            return []

    async def get_demo_implementation(self, demo_name: str) -> Optional[CloudscapeDemoResult]:
        """Get the implementation details for a specific demo."""
        if not self.repo_path or not self.repo_path.exists():
            return None

        try:
            # Search for demo by name
            for file_path in self.repo_path.rglob('*'):
                if not file_path.is_file():
                    continue

                if (
                    demo_name.lower() in file_path.name.lower()
                    or demo_name.lower() in str(file_path).lower()
                ):
                    return await self._analyze_demo_file(file_path)

            return None

        except Exception as e:
            logger.error(f'Error getting demo implementation for {demo_name}: {e}')
            return None

    async def analyze_demo_patterns(
        self, component_name: Optional[str] = None
    ) -> List[CloudscapeDemoResult]:
        """Analyze common patterns in demo implementations."""
        if not self.repo_path or not self.repo_path.exists():
            return []

        try:
            patterns = []

            # Look for files that contain common patterns
            for file_path in self.repo_path.rglob('*.tsx'):
                if self._should_skip_file(file_path):
                    continue

                content = file_path.read_text(encoding='utf-8', errors='ignore')

                # Filter by component if specified
                if component_name and component_name.lower() not in content.lower():
                    continue

                # Look for interesting patterns
                if self._contains_interesting_patterns(content):
                    demo_result = await self._analyze_demo_file(file_path)
                    if demo_result:
                        patterns.append(demo_result)

            return patterns[:10]  # Limit results

        except Exception as e:
            logger.error(f'Error analyzing demo patterns: {e}')
            return []

    async def _search_file(self, file_path: Path, query: str) -> Optional[CloudscapeDemoResult]:
        """Search within a specific file for relevant content."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            if not self._is_relevant(content, query):
                return None

            return await self._analyze_demo_file(file_path, content)

        except Exception as e:
            logger.error(f'Error searching file {file_path}: {e}')
            return None

    async def _analyze_demo_file(
        self, file_path: Path, content: Optional[str] = None
    ) -> Optional[CloudscapeDemoResult]:
        """Analyze a demo file and extract relevant information."""
        try:
            if content is None:
                content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Extract demo information
            demo_name = self._extract_demo_name(file_path, content)
            description = self._extract_description(content)
            components_used = self._extract_components_used(content)

            # Get relative path from repo root
            relative_path = file_path.relative_to(self.repo_path)

            return CloudscapeDemoResult(
                file_path=str(relative_path),
                demo_name=demo_name,
                content=content[:3000],  # Limit content length
                description=description,
                components_used=components_used,
            )

        except Exception as e:
            logger.error(f'Error analyzing demo file {file_path}: {e}')
            return None

    def _extract_demo_name(self, file_path: Path, content: str) -> str:
        """Extract demo name from file path or content."""
        # Try to get from file name first
        name = file_path.stem

        # Look for title or name in content
        title_patterns = [
            r'title:\s*["\']([^"\']+)["\']',
            r'name:\s*["\']([^"\']+)["\']',
            r'<title>([^<]+)</title>',
            r'// ([^\\n]+) Demo',
        ]

        for pattern in title_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return name.replace('-', ' ').replace('_', ' ').title()

    def _extract_description(self, content: str) -> Optional[str]:
        """Extract description from demo content."""
        # Look for common description patterns
        desc_patterns = [
            r'description:\s*["\']([^"\']+)["\']',
            r'// Description:\s*([^\\n]+)',
            r'/\*\*\s*([^*]+)\s*\*/',
            r'<p[^>]*>([^<]+)</p>',
        ]

        for pattern in desc_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                desc = match.group(1).strip()
                if len(desc) > 10:  # Filter out very short descriptions
                    return desc

        return None

    def _extract_components_used(self, content: str) -> List[str]:
        """Extract Cloudscape components used in the demo."""
        components = set()

        # Look for import statements
        import_pattern = r'import\s+{([^}]+)}\s+from\s+["\']@cloudscape-design/components["\']'
        matches = re.findall(import_pattern, content)

        for match in matches:
            # Split by comma and clean up
            component_names = [name.strip() for name in match.split(',')]
            components.update(component_names)

        # Look for JSX usage patterns
        jsx_pattern = r'<([A-Z][a-zA-Z]+)'
        jsx_matches = re.findall(jsx_pattern, content)

        # Filter to likely Cloudscape components (start with capital letter)
        cloudscape_components = [comp for comp in jsx_matches if comp[0].isupper()]
        components.update(cloudscape_components)

        return sorted(components)

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during search."""
        skip_patterns = [
            'node_modules',
            '.git',
            'dist',
            'build',
            '.next',
            'coverage',
            '__pycache__',
            '.DS_Store',
            'package-lock.json',
            'yarn.lock',
        ]

        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)

    def _contains_interesting_patterns(self, content: str) -> bool:
        """Check if content contains interesting patterns worth analyzing."""
        interesting_patterns = [
            r'@cloudscape-design/components',
            r'useState',
            r'useEffect',
            r'interface\s+\w+Props',
            r'type\s+\w+\s*=',
            r'const\s+\w+:\s*React\.FC',
        ]

        return any(re.search(pattern, content) for pattern in interesting_patterns)

    def _calculate_relevance(self, content: str, query: str) -> float:
        """Calculate relevance score for search results."""
        if not content or not query:
            return 0.0

        content_lower = content.lower()
        query_lower = query.lower()

        # Simple keyword matching with weights
        query_words = query_lower.split()
        matches = 0

        for word in query_words:
            # Higher weight for matches in imports or component names
            if f'import.*{word}' in content_lower:
                matches += 3
            elif f'<{word}' in content_lower:
                matches += 2
            elif word in content_lower:
                matches += 1

        return matches / len(query_words) if query_words else 0.0

    def _is_relevant(self, content: str, query: str, threshold: float = 0.1) -> bool:
        """Check if content is relevant to the query."""
        return self._calculate_relevance(content, query) >= threshold

    def __del__(self):
        """Clean up temporary repository."""
        if self.repo_path and self.repo_path.exists():
            try:
                import shutil

                shutil.rmtree(self.repo_path)
            except Exception as e:
                logger.warning(f'Could not clean up temporary repo: {e}')

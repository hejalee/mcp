"""Pydantic models for Cloudscape MCP Server."""

from pydantic import BaseModel, Field
from typing import List, Optional


class CloudscapeDocResult(BaseModel):
    """Result from Cloudscape documentation search."""

    title: str = Field(description='Title of the documentation page')
    url: str = Field(description='URL to the documentation page')
    content: str = Field(description='Content excerpt from the page')
    component_type: Optional[str] = Field(
        default=None, description='Type of component if applicable'
    )


class CloudscapeDemoResult(BaseModel):
    """Result from Cloudscape demos repository search."""

    file_path: str = Field(description='Path to the demo file')
    demo_name: str = Field(description='Name of the demo')
    content: str = Field(description='Code content from the demo')
    description: Optional[str] = Field(default=None, description='Description of the demo')
    components_used: List[str] = Field(
        default_factory=list, description='Cloudscape components used in this demo'
    )


class ComponentInfo(BaseModel):
    """Information about a Cloudscape component."""

    name: str = Field(description='Component name')
    description: str = Field(description='Component description')
    props: List[str] = Field(default_factory=list, description='Available props')
    examples: List[str] = Field(default_factory=list, description='Usage examples')
    related_components: List[str] = Field(default_factory=list, description='Related components')


class DesignToken(BaseModel):
    """Cloudscape design token information."""

    name: str = Field(description='Token name')
    value: str = Field(description='Token value')
    category: str = Field(description='Token category (color, spacing, typography, etc.)')
    description: Optional[str] = Field(default=None, description='Token description')

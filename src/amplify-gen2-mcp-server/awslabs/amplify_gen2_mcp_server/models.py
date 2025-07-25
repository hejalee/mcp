# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data models for the AWS Amplify Gen2 MCP Server."""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class SearchResult(BaseModel):
    """Represents a search result from Amplify documentation or samples."""

    name: str = Field(..., description="Name of the file or resource")
    path: str = Field(..., description="Path within the repository")
    url: str = Field(..., description="URL to access the resource")
    download_url: Optional[str] = Field(None, description="Direct download URL for the content")
    repository: str = Field(..., description="Repository where the resource is located")
    relevance_score: float = Field(0.0, description="Relevance score for the search query")
    content_preview: Optional[str] = Field(None, description="Preview of the content")


class DocumentationContent(BaseModel):
    """Represents documentation content retrieved from a URL."""

    url: str = Field(..., description="Source URL of the content")
    title: Optional[str] = Field(None, description="Title extracted from the content")
    content: str = Field(..., description="The actual content in markdown format")
    content_length: int = Field(..., description="Length of the content in characters")
    truncated: bool = Field(False, description="Whether the content was truncated")


class ProjectTemplate(BaseModel):
    """Represents an Amplify Gen2 project template."""

    name: str = Field(..., description="Name of the template")
    repository: str = Field(..., description="Repository containing the template")
    framework: str = Field(..., description="Frontend framework (react, vue, angular, next, ai)")
    description: str = Field(..., description="Description of the template")
    features: List[str] = Field(default_factory=list, description="List of features included")
    setup_instructions: Optional[str] = Field(None, description="Setup instructions")
    demo_url: Optional[str] = Field(None, description="URL to live demo if available")


class GuidanceResponse(BaseModel):
    """Represents guidance response for Amplify Gen2 topics."""

    topic: str = Field(..., description="The topic the guidance is for")
    summary: str = Field(..., description="Summary of the guidance")
    detailed_guidance: str = Field(..., description="Detailed guidance content")
    code_examples: List[Dict[str, Any]] = Field(default_factory=list, description="Code examples")
    related_topics: List[str] = Field(default_factory=list, description="Related topics")
    references: List[str] = Field(default_factory=list, description="Reference URLs")


class TroubleshootingResponse(BaseModel):
    """Represents troubleshooting guidance for Amplify Gen2 issues."""

    issue: str = Field(..., description="The issue being troubleshot")
    diagnosis: str = Field(..., description="Diagnosis of the issue")
    solutions: List[str] = Field(..., description="List of potential solutions")
    prevention: Optional[str] = Field(None, description="How to prevent this issue")
    related_issues: List[str] = Field(default_factory=list, description="Related common issues")
    references: List[str] = Field(default_factory=list, description="Reference documentation URLs")

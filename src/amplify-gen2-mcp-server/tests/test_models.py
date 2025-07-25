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

"""Tests for the AWS Amplify Gen2 MCP Server models."""

import pytest
from awslabs.amplify_gen2_mcp_server.models import (
    DocumentationContent,
    GuidanceResponse,
    ProjectTemplate,
    SearchResult,
    TroubleshootingResponse,
)
from pydantic import ValidationError


def test_search_result_model():
    """Test SearchResult model validation."""
    data = {
        "name": "test-file.md",
        "path": "docs/test-file.md",
        "url": "https://github.com/aws-amplify/docs/blob/main/docs/test-file.md",
        "repository": "aws-amplify/docs",
        "relevance_score": 0.85
    }

    result = SearchResult(**data)
    assert result.name == "test-file.md"
    assert result.relevance_score == 0.85
    assert result.download_url is None  # Optional field


def test_documentation_content_model():
    """Test DocumentationContent model validation."""
    data = {
        "url": "https://example.com/doc.md",
        "content": "# Test Content\n\nThis is test content.",
        "content_length": 35,
        "truncated": False
    }

    content = DocumentationContent(**data)
    assert content.url == "https://example.com/doc.md"
    assert content.content_length == 35
    assert not content.truncated


def test_project_template_model():
    """Test ProjectTemplate model validation."""
    data = {
        "name": "React Template",
        "repository": "aws-samples/amplify-vite-react-template",
        "framework": "react",
        "description": "A React template for Amplify Gen2",
        "features": ["authentication", "data", "storage"]
    }

    template = ProjectTemplate(**data)
    assert template.framework == "react"
    assert len(template.features) == 3
    assert "authentication" in template.features


def test_guidance_response_model():
    """Test GuidanceResponse model validation."""
    data = {
        "topic": "authentication",
        "summary": "How to set up authentication",
        "detailed_guidance": "Detailed steps for authentication setup...",
        "code_examples": [{"language": "typescript", "code": "const auth = ..."}],
        "related_topics": ["authorization", "user-management"]
    }

    guidance = GuidanceResponse(**data)
    assert guidance.topic == "authentication"
    assert len(guidance.code_examples) == 1
    assert "authorization" in guidance.related_topics


def test_troubleshooting_response_model():
    """Test TroubleshootingResponse model validation."""
    data = {
        "issue": "deployment fails",
        "diagnosis": "Missing environment variables",
        "solutions": ["Set required env vars", "Check IAM permissions"],
        "prevention": "Use environment validation"
    }

    troubleshooting = TroubleshootingResponse(**data)
    assert troubleshooting.issue == "deployment fails"
    assert len(troubleshooting.solutions) == 2
    assert troubleshooting.prevention == "Use environment validation"


def test_required_fields_validation():
    """Test that required fields are validated."""
    with pytest.raises(ValidationError):
        SearchResult()  # Missing required fields

    with pytest.raises(ValidationError):
        DocumentationContent(url="test")  # Missing content and content_length

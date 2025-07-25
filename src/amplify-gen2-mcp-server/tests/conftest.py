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

"""Test configuration for AWS Amplify Gen2 MCP Server."""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_github_response():
    """Mock GitHub API response for testing."""
    return {
        'items': [
            {
                'name': 'test-file.md',
                'path': 'docs/test-file.md',
                'html_url': 'https://github.com/aws-amplify/docs/blob/main/docs/test-file.md',
                'download_url': 'https://raw.githubusercontent.com/aws-amplify/docs/main/docs/test-file.md'
            }
        ]
    }


@pytest.fixture
def mock_requests_get():
    """Mock requests.get for testing."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'items': []}
    mock_response.text = "# Test Content\n\nThis is test content."
    return mock_response

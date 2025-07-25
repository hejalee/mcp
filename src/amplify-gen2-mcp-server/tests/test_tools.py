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

"""Tests for the AWS Amplify Gen2 MCP Server tools."""

import unittest
from awslabs.amplify_gen2_mcp_server.tools import (
    generate_amplify_gen2_code,
    get_amplify_gen2_best_practices,
    get_amplify_gen2_guidance,
    troubleshoot_amplify_gen2,
)
from unittest.mock import MagicMock


class TestAmplifyGen2Tools(unittest.TestCase):
    """Test cases for Amplify Gen2 MCP Server tools."""

    def test_get_amplify_gen2_guidance(self):
        """Test get_amplify_gen2_guidance function."""
        ctx = MagicMock()

        # Test with valid topic
        result = get_amplify_gen2_guidance(ctx, "authentication")
        self.assertIsInstance(result, str)
        self.assertIn("authentication", result.lower())
        self.assertIn("amplify", result.lower())

        # Test with invalid topic
        result = get_amplify_gen2_guidance(ctx, "invalid_topic")
        self.assertIsInstance(result, str)
        self.assertIn("invalid_topic", result.lower())

    def test_generate_amplify_gen2_code(self):
        """Test generate_amplify_gen2_code function."""
        ctx = MagicMock()

        # Test with valid feature and framework
        result = generate_amplify_gen2_code(ctx, "authentication", "react")
        self.assertIsInstance(result, str)
        self.assertIn("authentication", result.lower())
        self.assertIn("react", result.lower())

        # Test with invalid feature and framework
        result = generate_amplify_gen2_code(ctx, "invalid", "invalid")
        self.assertIsInstance(result, str)
        self.assertIn("invalid", result.lower())

    def test_get_amplify_gen2_best_practices(self):
        """Test get_amplify_gen2_best_practices function."""
        ctx = MagicMock()

        # Test with valid area
        result = get_amplify_gen2_best_practices(ctx, "authentication")
        self.assertIsInstance(result, str)
        self.assertIn("Amplify Gen2 Authentication Best Practices", result)

        # Test with invalid area
        result = get_amplify_gen2_best_practices(ctx, "invalid_area")
        self.assertIsInstance(result, str)
        self.assertIn("not available yet", result)

    def test_troubleshoot_amplify_gen2(self):
        """Test troubleshoot_amplify_gen2 function."""
        ctx = MagicMock()

        # Test with valid issue
        result = troubleshoot_amplify_gen2(ctx, "deployment issues")
        self.assertIsInstance(result, str)
        self.assertIn("deployment", result.lower())
        self.assertIn("troubleshooting", result.lower())

        # Test with another valid issue
        result = troubleshoot_amplify_gen2(ctx, "authentication problems")
        self.assertIsInstance(result, str)
        self.assertIn("authentication", result.lower())

        # Test with invalid issue
        result = troubleshoot_amplify_gen2(ctx, "invalid_issue")
        self.assertIsInstance(result, str)
        self.assertIn("invalid_issue", result.lower())


if __name__ == "__main__":
    unittest.main()

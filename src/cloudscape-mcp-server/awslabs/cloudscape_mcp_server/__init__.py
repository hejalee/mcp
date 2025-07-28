"""Cloudscape MCP Server."""

__version__ = '1.0.0'

try:
    from importlib.metadata import version

    __version__ = version('awslabs.cloudscape-mcp-server')
except ImportError:
    # importlib.metadata is not available in Python < 3.8
    pass
except Exception:
    # package is not installed
    pass

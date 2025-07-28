# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies
RUN uv venv && uv sync --all-groups

# Create a non-root user
RUN useradd -m -u 1000 mcp && chown -R mcp:mcp /app
USER mcp

# Expose port (if needed for HTTP mode)
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV FASTMCP_LOG_LEVEL=ERROR

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import awslabs.cloudscape_mcp_server; print('OK')" || exit 1

# Default command
CMD ["uv", "run", "awslabs.cloudscape-mcp-server"]

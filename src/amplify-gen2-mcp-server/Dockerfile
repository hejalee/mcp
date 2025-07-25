FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir uv
RUN pip install --no-cache-dir mcp>=1.0.0 pydantic>=2.0.0 loguru>=0.7.0

# Copy the package
COPY . .

# Install the package
RUN pip install --no-cache-dir -e .

# Health check
COPY docker-healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-healthcheck.sh
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 CMD ["docker-healthcheck.sh"]

# Run the server
CMD ["python", "-m", "awslabs.amplify_gen2_mcp_server"]

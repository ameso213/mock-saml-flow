FROM python:3.12-slim

# Install system dependencies following the dependencies from the pyproject.toml file that are required to build the xmlsec package.
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
 #
WORKDIR /app

# Copy project files because the pyproject.toml file is required to install dependencies and the src dir contains the files required to run the test.
COPY pyproject.toml .
COPY src/ ./src/

# Install pip to make sure i have the latest version and -e ".[dev,test] which installs dependencies for development and testing.
RUN pip install --upgrade pip
RUN pip install -e ".[dev,test]"


EXPOSE 8000

#this
CMD ["python", "-m", "mock_saml_flow.sp"]






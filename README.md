# mock-saml-flow

Mock SAML 2.0 flows using [pytest](https://pytest.org/) and
[PySAML2](https://github.com/IdentityPython/pysaml2/) by running `make
smoke`; requires Python 3.11+, GNU Make, jq, and a POSIX shell
environment.




## Configuration Workflow

### 1. Define Role-Specific Dockerfiles
Separate Dockerfiles were created to have two different images and containers for the Service Provider and Identity Provider.

touch Dockerfile.sp Dockerfile.idp


### 2. Base Image Selection
The `python:3.12-slim` image was chosen over `scratch`.it has the Python interpreter and `pip` pre-installed, which are required to support the SAML security libraries.

### 3. Orchestration with Docker Compose
A `docker-compose.yaml` file was created to manage the internal networking between the two services.

touch docker-compose.yaml

### 4. Service Definition & Networking
The `sp` and `idp` services were defined and a shared bridge network called `saml-network` was created to allow private communication between the two containers.

### 5. Port Mapping
To allow external access from the browser on the host machine, internal container ports were mapped to the host:
*   **SP**: Port 8000
*   **IdP**: Port 8080

### 6. Service Discovery
The environment variable `IDP_URL=http://idp:8080` was injected into the SP container. This allows the SP to locate the IdP.



# MLForge Docker Images

MLForge provides Docker images to help you quickly deploy and run MLForge in containerized environments.

## Image Variants

### MLForge:VERSION (default)

This image contains only the core MLForge package without extra dependencies. Most integrations (backend store databases, artifact stores, etc.) will not work without additional packages.

Use this image as a lightweight base when you want full control over which dependencies to install, or when you only need basic MLForge functionality.

### MLForge:VERSION-full

This image contains MLForge with all extra dependencies, including:

- Database drivers (MySQL, PostgreSQL, SQL Server)
- Cloud storage integrations (AWS S3, Azure Blob, GCS)
- AI Gateway and GenAI capabilities

> [!NOTE]
> The `-full` image variant is only available starting from **MLForge v3.9.0** and later versions. Earlier versions only provide the default `MLForge:VERSION` image.

Use this image when you need comprehensive MLForge functionality with multiple integrations.

**Note:** Replace `VERSION` with the actual MLForge version (e.g., `3.9.0`) or use `latest-full` for the most recent release.

## Quick Start

### Basic Usage

Run MLForge server with default settings (SQLite backend, local file storage):

```bash
docker run -p 5000:5000 MLForge:latest-full MLForge server --host 0.0.0.0
```

Access the MLForge UI at http://localhost:5000

### With MySQL Backend

```bash
docker run -p 5000:5000 \
  -e MLForge_BACKEND_STORE_URI=mysql+pymysql://user:password@mysql-host:3306/MLForge \
  MLForge:latest-full \
  MLForge server --backend-store-uri $MLForge_BACKEND_STORE_URI --host 0.0.0.0
```

### With PostgreSQL Backend

```bash
docker run -p 5000:5000 \
  -e MLForge_BACKEND_STORE_URI=postgresql://user:password@postgres-host:5432/MLForge \
  MLForge:latest-full \
  MLForge server --backend-store-uri $MLForge_BACKEND_STORE_URI --host 0.0.0.0
```

### With S3 Artifact Storage

```bash
docker run -p 5000:5000 \
  -e AWS_ACCESS_KEY_ID=your-access-key \
  -e AWS_SECRET_ACCESS_KEY=your-secret-key \
  MLForge:latest-full \
  MLForge server --artifacts-destination s3://your-bucket/path --host 0.0.0.0
```

### With Azure Blob Storage

```bash
docker run -p 5000:5000 \
  -e AZURE_STORAGE_CONNECTION_STRING="your-connection-string" \
  MLForge:latest-full \
  MLForge server --artifacts-destination wasbs://container@account.blob.core.windows.net/path --host 0.0.0.0
```

## Docker Compose Example

Here's an example `docker-compose.yml` for running MLForge with MySQL:

```yaml
version: "3.8"

services:
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: MLForge
      MYSQL_USER: MLForge
      MYSQL_PASSWORD: MLForge
    volumes:
      - mysql-data:/var/lib/mysql
    ports:
      - "3306:3306"

  MLForge:
    image: MLForge:latest-full
    depends_on:
      - mysql
    ports:
      - "5000:5000"
    environment:
      MLForge_BACKEND_STORE_URI: mysql+pymysql://MLForge:MLForge@mysql:3306/MLForge
    command: MLForge server --backend-store-uri $MLForge_BACKEND_STORE_URI --host 0.0.0.0

volumes:
  mysql-data:
```

## Environment Variables

Common environment variables for configuring MLForge:

- `MLForge_BACKEND_STORE_URI` - Backend store URI (database connection string)
- `MLForge_DEFAULT_ARTIFACT_ROOT` - Default location for storing artifacts
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` - AWS credentials for S3
- `AZURE_STORAGE_CONNECTION_STRING` - Azure storage connection string
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to GCP service account key file

## Running the Development Version

### Build the dev image

From the repository root:

```bash
docker build -f docker/Dockerfile.full.dev -t MLForge-dev .
```

This installs MLForge in editable mode with all extras: `[extras,db,databricks,gateway,genai,sqlserver]`

### Run the dev image

```bash
docker run -p 5000:5000 MLForge-dev MLForge server --host 0.0.0.0
```

**Note:** The dev Docker image is intended for testing backend changes only, not for production use.

## Building Custom Images

If you need to customize the image, you can use the base image and add your own dependencies:

```dockerfile
FROM MLForge:latest

# Install additional dependencies
RUN pip install MLForge[extras,db] your-custom-package

# Add custom configurations
COPY your-config.yaml /opt/MLForge/
```

Or start from the full image and add more:

```dockerfile
FROM MLForge:latest-full

# Install additional custom packages
RUN pip install your-custom-package
```

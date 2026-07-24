# MLForge with Docker Compose (PostgreSQL + S3-Compatible Storage)

This directory provides a **Docker Compose** setup for running **MLForge** locally with a **PostgreSQL** backend store and **RustFS** for S3-compatible artifact storage.

---

## Overview

- **MLForge Tracking Server**  
  Serves the REST API and UI (default: `http://localhost:5000`).

- **PostgreSQL**  
  Stores MLForge's metadata (experiments, runs, params, metrics).

- **RustFS Artifact Storage**  
  Stores model files and run artifacts.

---

## Prerequisites

- **Git**
- **Docker** and **Docker Compose**
- On macOS/Windows: Docker Desktop
- On Linux: Docker Engine + compose plugin

Verify installation:

```bash
docker --version
docker compose version
```

---

## 1. Clone the Repository

```bash
git clone https://github.com/MLForge/MLForge.git
cd MLForge/docker-compose/
```

---

## 2. Configure Environment

Copy and customize the environment file:

```bash
cp .env.dev.example .env
```

The `.env` file defines:

- MLForge server port
- PostgreSQL credentials
- S3 bucket name
- S3-compatible endpoint URL
- Backend-specific configuration for RustFS

**Common variables**:

- **PostgreSQL**

  - `POSTGRES_USER=MLForge`
  - `POSTGRES_PASSWORD=MLForge`
  - `POSTGRES_DB=MLForge`

- **S3**

  - `AWS_ACCESS_KEY_ID=s3admin`
  - `AWS_SECRET_ACCESS_KEY=s3admin`
  - `AWS_DEFAULT_REGION=us-east-1`
  - `S3_BUCKET=MLForge`

- **RustFS**

  - `RUSTFS_CONSOLE_ENABLE=true`

- **MLForge**
  - `MLForge_VERSION=latest`
  - `MLForge_HOST=0.0.0.0`
  - `MLForge_PORT=5000`
  - `MLForge_BACKEND_STORE_URI=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}`
  - `MLForge_ARTIFACTS_DESTINATION=s3://${S3_BUCKET}`
  - `MLForge_S3_ENDPOINT_URL=http://storage:9000`

---

## 3. Launch the Stack

Inside directory **MLForge/docker-compose**:

```bash
docker compose up -d
```

This will:

- Start PostgreSQL
- Start RustFS
- Start MLForge
- Create the S3 bucket if it doesn't exist

Check status:

```bash
docker compose ps
```

Tail logs:

```bash
docker compose logs -f
```

---

## 4. Access MLForge

Once running:

- Open `http://localhost:5000` (or the port defined in `.env`)

You can now log runs, metrics, artifacts, and models to your local MLForge instance.

---

## 5. Shutdown

To stop and remove containers:

```bash
docker compose down
```

To reset everything, including volumes:

```bash
docker compose down -v
```

---

## Tips & Troubleshooting

### RustFS Notes (important)

- Set **server domains/host** so virtual-hosted requests can be resolved by RustFS:

  ```env
  RUSTFS_SERVER_DOMAINS=storage:9000
  ```

  (match the compose service DNS name)

- Prefer AWS CLI **`s3api`** for bucket creation. Some S3 clients default to **path-style** on custom endpoints; if bucket creation fails with `InvalidBucketName`, switch to `s3api` or a client like MinIO `mc`.

- Inside MLForge, use the internal endpoint:
  ```env
  MLForge_S3_ENDPOINT_URL=http://storage:9000
  MLForge_ARTIFACTS_DESTINATION=s3://MLForge/
  ```

### Healthcheck Example

RustFS usually responds on `/health` with a json that contains the status of the server:

```sh
curl -s http://127.0.0.1:9000/health | grep -q '\"status\"\\s*:\\s*\"ok\"'
```

Use that in a container healthcheck (no `-f`, 4xx may appear during bootstrap).

---

### Artifact Upload Issues

Verify:

- `MLForge_ARTIFACTS_DESTINATION=s3://<bucket>/`
- `MLForge_S3_ENDPOINT_URL=http://<service>:<port>`
- AWS credentials match the backend configuration

To verify S3 storage is working:

```bash
aws --endpoint-url=${MLForge_S3_ENDPOINT_URL} s3api list-buckets

echo hi > /tmp/t.txt
aws --endpoint-url=${MLForge_S3_ENDPOINT_URL} s3 cp /tmp/t.txt s3://${S3_BUCKET}/t.txt
aws --endpoint-url=${MLForge_S3_ENDPOINT_URL} s3 cp s3://${S3_BUCKET}/t.txt -
```

If this passes, MLForge can read and write artifacts to RustFS.

### Troubleshooting

- `InvalidBucketName` on create-bucket → use `s3api` (virtual-host friendly) or MinIO `mc`; ensure `RUSTFS_SERVER_DOMAINS` matches the S3 hostname.
- Endpoint issues from MLForge → make sure `MLForge_S3_ENDPOINT_URL` uses the **service name** visible from MLForge (e.g., `http://storage:9000`).

### Resetting the Environment

```bash
docker compose down -v
docker compose up -d
```

### Logs

```bash
docker compose logs -f MLForge
docker compose logs -f postgres
docker compose logs -f storage
```

### Port Conflicts

Edit `.env` and restart containers:

```bash
docker compose down
docker compose up -d
```

---

## Next Steps

- Point your training scripts to this server:
  ```bash
  export MLForge_TRACKING_URI=http://localhost:5000
  ```
- Start logging runs with `MLForge.start_run()` (Python) or the MLForge CLI.
- Customize the `.env` and `docker-compose.yml` to fit your local workflow (e.g., change image tags, add volumes, etc.).

---

**You now have a fully local MLForge stack with persistent metadata and artifact storage—ideal for development and experimentation.**

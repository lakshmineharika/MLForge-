# MLForge Tracking Server Security Configuration Guide

This document provides a quick reference for AI assistants to understand MLForge tracking server security options and configurations.

## Overview

The MLForge tracking server includes built-in security middleware to protect against common web vulnerabilities:

- **DNS rebinding attacks** - via Host header validation
- **Cross-Origin Resource Sharing (CORS) attacks** - via origin validation
- **Clickjacking** - via X-Frame-Options header

## Starting the Server

```bash
# Basic start (localhost-only, secure by default)
MLForge server

# Allow connections from other machines
MLForge server --host 0.0.0.0

# Custom port
MLForge server --port 8080
```

## Security Configuration Options

### 1. Host Header Validation (`--allowed-hosts`)

Prevents DNS rebinding attacks by validating the Host header in incoming requests.

```bash
# Allow specific hosts
MLForge server --allowed-hosts "MLForge.company.com,10.0.0.100:5000"

# Allow hosts with wildcards
MLForge server --allowed-hosts "MLForge.company.com,192.168.*,app-*.internal.com"

# DANGEROUS: Allow all hosts (not recommended for production)
MLForge server --allowed-hosts "*"
```

**Default behavior**: Allows localhost (all ports) and private IP ranges (10._, 192.168._, 172.16-31.\*).

### 2. CORS Origin Validation (`--cors-allowed-origins`)

Controls which web applications can make requests to your MLForge server.

```bash
# Allow specific origins
MLForge server --cors-allowed-origins "https://app.company.com,https://notebook.company.com"

# DANGEROUS: Allow all origins (only for development)
MLForge server --cors-allowed-origins "*"
```

**Default behavior**: Allows `http://localhost:*, http://127.0.0.1:*, http://[::1]:*` (all ports).

### 3. Clickjacking Protection (`--x-frame-options`)

Controls whether the MLForge UI can be embedded in iframes.

```bash
# Default: Same origin only
MLForge server --x-frame-options SAMEORIGIN

# Deny all iframe embedding
MLForge server --x-frame-options DENY

# Allow iframe embedding from anywhere (not recommended)
MLForge server --x-frame-options NONE
```

### 4. Disable Security Middleware (`--disable-security-middleware`)

**DANGEROUS**: Completely disables all security protections.

```bash
# Only for testing - removes all security protections
MLForge server --disable-security-middleware
```

## Common Configuration Scenarios

### Local Development (Default)

```bash
MLForge server
# Security: Enabled (localhost-only)
# Access: Only from local machine
```

### Team Development Server

```bash
MLForge server \
  --host 0.0.0.0 \
  --allowed-hosts "MLForge.dev.company.com,192.168.*" \
  --cors-allowed-origins "https://notebook.dev.company.com"
```

### Production Server

```bash
MLForge server \
  --host 0.0.0.0 \
  --allowed-hosts "MLForge.prod.company.com" \
  --cors-allowed-origins "https://app.prod.company.com,https://notebook.prod.company.com" \
  --x-frame-options DENY
```

### Docker Container Setup

```bash
# In docker-compose.yml, set environment variables:
environment:
  MLForge_SERVER_ALLOWED_HOSTS: "tracking-server:5000,localhost:5000,127.0.0.1:5000"
  MLForge_SERVER_CORS_ALLOWED_ORIGINS: "http://frontend:3000"
```

## Environment Variables

All CLI options can be set via environment variables:

- `MLForge_SERVER_ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `MLForge_SERVER_CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins
- `MLForge_SERVER_X_FRAME_OPTIONS` - Clickjacking protection setting
- `MLForge_SERVER_DISABLE_SECURITY_MIDDLEWARE` - Set to "true" to disable security

## Security Messages

When starting the server, users see one of these messages:

1. **Default configuration**:

   ```bash
   [MLForge] Security middleware enabled with default settings (localhost-only).
   To allow connections from other hosts, use --host 0.0.0.0 and configure
   --allowed-hosts and --cors-allowed-origins.
   ```

2. **Custom configuration**:

   ```bash
   [MLForge] Security middleware enabled. Allowed hosts: MLForge.company.com, 192.168.*.
   CORS origins: https://app.company.com.
   ```

3. **Security disabled**:

   ```bash
   [MLForge] WARNING: Security middleware is DISABLED. Your MLForge server is vulnerable to various attacks.
   ```

## Implementation Details

- Security middleware is implemented in:
  - Flask: `MLForge/server/security.py`
  - FastAPI: `MLForge/server/fastapi_security.py`
- Configuration messages displayed in: `MLForge/cli/__init__.py` (server function)
- Security is enabled by default unless explicitly disabled

## Testing Security Configuration

```bash
# Test Host header validation
curl -H "Host: evil.com" http://localhost:5000/api/2.0/MLForge/experiments/search
# Should return: 400 Bad Request - Invalid Host header

# Test CORS
curl -H "Origin: https://evil.com" http://localhost:5000/api/2.0/MLForge/experiments/search
# Should not include Access-Control-Allow-Origin header for unauthorized origin
```

## Important Notes

1. **Security by default**: The server is secure by default, only accepting localhost connections
2. **Host validation**: When using `--host 0.0.0.0`, always configure `--allowed-hosts`
3. **CORS in production**: Always specify exact origins, never use "\*" in production
4. **Docker networking**: Container names (e.g., "tracking-server") must be in allowed hosts
5. **Private IPs**: Default configuration allows private IP ranges for development convenience

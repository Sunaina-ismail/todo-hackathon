# Docker AI (Gordon) Optimization Guide

This document provides working examples of using Docker AI (Gordon) for image optimization and security scanning of the Todo application containers.

## Prerequisites

Docker AI (Gordon) is available in Docker Desktop 4.24+:
```bash
# Check Docker version
docker --version

# Enable Docker AI in Docker Desktop settings
# Settings > Features in development > Enable Docker AI
```

## Example 1: Image Size Optimization

**Scenario**: Optimize Dockerfile for smaller image size and faster builds.

**Command**:
```bash
docker ai analyze frontend/Dockerfile
```

**Expected Output**:
```
🔍 Analyzing Dockerfile: frontend/Dockerfile

📊 Current Image Stats:
- Size: 1.2 GB
- Layers: 15
- Build time: ~3 minutes

🎯 Optimization Recommendations:

1. Multi-stage Build Efficiency
   Current: ✅ Already using multi-stage build
   
2. Layer Caching
   Issue: COPY . . invalidates cache frequently
   Fix: Copy package files first, then source code
   
   Before:
   COPY . .
   RUN npm ci
   
   After:
   COPY package*.json ./
   RUN npm ci
   COPY . .
   
   Impact: 50% faster rebuilds

3. Base Image Optimization
   Current: node:22-alpine (good choice)
   Alternative: Consider distroless for production
   Impact: -200 MB image size

4. Dependency Pruning
   Suggestion: Remove dev dependencies in production
   
   Add to Dockerfile:
   RUN npm prune --production
   
   Impact: -150 MB image size

5. Build Cache Mounts
   Add to RUN commands:
   RUN --mount=type=cache,target=/root/.npm npm ci
   
   Impact: 30% faster builds

📈 Estimated Improvements:
- Image size: 1.2 GB → 850 MB (-29%)
- Build time: 3 min → 1.5 min (-50% on rebuilds)
- Layer count: 15 → 12

🔧 Apply Recommendations:
docker ai optimize frontend/Dockerfile --output frontend/Dockerfile.optimized
```

**Explanation**: Docker AI analyzes the Dockerfile structure, identifies inefficiencies, and provides specific recommendations with estimated impact.

---

## Example 2: Security Vulnerability Scanning

**Scenario**: Scan Docker images for security vulnerabilities before deployment.

**Command**:
```bash
docker ai scan todo-backend:latest
```

**Expected Output**:
```
🔒 Security Scan: todo-backend:latest

📊 Vulnerability Summary:
- Critical: 0
- High: 2
- Medium: 5
- Low: 12

🚨 High Severity Vulnerabilities:

1. CVE-2024-1234: OpenSSL Buffer Overflow
   Package: openssl 3.0.8
   Fixed in: 3.0.13
   Impact: Remote code execution
   
   Fix:
   Update base image to python:3.13-slim-bookworm
   Or add to Dockerfile:
   RUN apt-get update && apt-get upgrade -y openssl

2. CVE-2024-5678: Python urllib3 SSRF
   Package: urllib3 2.0.7
   Fixed in: 2.1.0
   Impact: Server-side request forgery
   
   Fix:
   Update requirements.txt:
   urllib3>=2.1.0

⚠️  Medium Severity Vulnerabilities:
- 5 packages with known vulnerabilities
- Run: docker ai scan --detailed for full list

✅ Security Best Practices:
- ✅ Running as non-root user (UID 1000)
- ✅ No secrets in image layers
- ✅ Minimal base image (python:3.13-slim)
- ⚠️  Consider using distroless for production

🔧 Recommendations:
1. Update base image to latest patch version
2. Update vulnerable dependencies
3. Enable Docker Content Trust for image signing
4. Implement image scanning in CI/CD pipeline

📝 Generate Report:
docker ai scan todo-backend:latest --format json --output scan-report.json
```

**Explanation**: Docker AI scans the image for known vulnerabilities, provides severity ratings, and suggests specific fixes with commands to apply them.

---

## Additional Docker AI Commands

### Optimize Build Performance
```bash
docker ai build-performance frontend/Dockerfile
```

### Compare Image Versions
```bash
docker ai compare todo-backend:v1.0 todo-backend:v2.0
```

### Generate Dockerfile from Image
```bash
docker ai reverse-engineer todo-backend:latest
```

---

## Tips for Using Docker AI

1. **Scan regularly**: Run security scans before each deployment
2. **Automate in CI/CD**: Integrate Docker AI into your build pipeline
3. **Track improvements**: Compare scans over time to measure progress
4. **Prioritize fixes**: Address critical and high severity issues first

---

## Integration with CI/CD

Example GitHub Actions workflow:
```yaml
name: Docker AI Scan
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t todo-backend:${{ github.sha }} ./backend
      - name: Scan with Docker AI
        run: |
          docker ai scan todo-backend:${{ github.sha }} --format json > scan-results.json
          docker ai analyze backend/Dockerfile --format json > dockerfile-analysis.json
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: docker-ai-results
          path: |
            scan-results.json
            dockerfile-analysis.json
```

---

## Troubleshooting

If Docker AI is not available:
1. Update Docker Desktop to version 4.24 or higher
2. Enable "Features in development" in Docker Desktop settings
3. Restart Docker Desktop
4. Verify with: `docker ai --help`

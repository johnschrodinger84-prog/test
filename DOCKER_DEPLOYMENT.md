# Docker Deployment Guide

Complete guide for deploying the Universal AI Platform using Docker.

---

## 📋 Prerequisites

- Docker Engine 20.10+ installed
- Docker Compose 2.0+ installed
- Google Gemini API key

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Set Environment Variables
Create a `.env` file in the project root:

```bash
# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=production
EOF
```

### 3. Build and Run with Docker Compose

**Start the application:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the application:**
```bash
docker-compose down
```

---

## 🐳 Docker Commands

### Build the Image
```bash
docker build -t universal-ai-platform .
```

### Run the Container
```bash
docker run -d \
  --name universal-ai-platform \
  -p 5000:5000 \
  -e GEMINI_API_KEY=your_api_key_here \
  -v $(pwd)/uploads:/app/uploads \
  universal-ai-platform
```

### Access the Application
Once running, access the application at:
- **API:** http://localhost:5000
- **Health Check:** http://localhost:5000/core/health
- **Landing Page:** http://localhost:5000

---

## 📦 Image Details

### Base Image
- **Python:** 3.11-slim (Debian-based)
- **Size:** ~250 MB (optimized)

### Installed Components
- Flask + Flask-CORS
- Gunicorn (production WSGI server)
- Google Generative AI SDK
- Python Magic (file type detection)
- Pillow (image processing)

### Port
- **Exposed:** 5000
- **Protocol:** HTTP

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key |
| `FLASK_ENV` | No | production | Flask environment (production/development) |
| `FLASK_APP` | No | main.py | Flask application entry point |

### Volume Mounts

```yaml
volumes:
  - ./uploads:/app/uploads  # Persistent file storage
```

---

## 🏥 Health Checks

The container includes automatic health checks:

**Configuration:**
- **Endpoint:** `/core/health`
- **Interval:** 30 seconds
- **Timeout:** 10 seconds
- **Start Period:** 40 seconds
- **Retries:** 3

**Check Health Status:**
```bash
docker inspect --format='{{json .State.Health}}' universal-ai-platform
```

---

## 🔧 Production Deployment

### Using Gunicorn (Default)

The Dockerfile uses Gunicorn with optimal settings:

```bash
gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 4 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  main:app
```

**Worker Calculation:**
- **Formula:** `(2 × CPU_cores) + 1`
- **Default:** 4 workers (assumes 2 CPU cores)

**Adjust Workers:**
```dockerfile
# In Dockerfile, modify the CMD line:
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "8", ...]
```

### Scaling with Docker Compose

```bash
# Scale to 3 instances
docker-compose up -d --scale web=3
```

---

## 🌐 Reverse Proxy Setup

### Nginx Configuration

```nginx
upstream universal_ai {
    server localhost:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://universal_ai;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers (if needed at proxy level)
        add_header Access-Control-Allow-Origin *;
    }

    # Increase timeout for AI processing
    proxy_connect_timeout 300;
    proxy_send_timeout 300;
    proxy_read_timeout 300;
}
```

### Traefik Configuration

```yaml
version: '3.8'

services:
  web:
    build: .
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.universal-ai.rule=Host(`your-domain.com`)"
      - "traefik.http.services.universal-ai.loadbalancer.server.port=5000"
```

---

## 📊 Monitoring & Logs

### View Live Logs
```bash
docker-compose logs -f web
```

### View Last 100 Lines
```bash
docker-compose logs --tail=100 web
```

### Export Logs to File
```bash
docker-compose logs web > app.log
```

### Container Stats
```bash
docker stats universal-ai-platform
```

---

## 🔐 Security Best Practices

### 1. Don't Expose Secrets in Dockerfile
✅ **Use environment variables** or Docker secrets

```bash
# Good: Pass at runtime
docker run -e GEMINI_API_KEY=$GEMINI_API_KEY ...

# Bad: Hardcode in Dockerfile
ENV GEMINI_API_KEY=hardcoded_key_here
```

### 2. Use Multi-Stage Builds (Advanced)
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", ...]
```

### 3. Run as Non-Root User
```dockerfile
# Add after WORKDIR in Dockerfile
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
```

### 4. Scan for Vulnerabilities
```bash
docker scan universal-ai-platform
```

---

## 🐛 Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker logs universal-ai-platform
```

**Common issues:**
- Missing `GEMINI_API_KEY` environment variable
- Port 5000 already in use
- Insufficient disk space

### Port Already in Use

**Find process using port 5000:**
```bash
# Linux/Mac
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

**Change port mapping:**
```bash
docker run -p 8080:5000 ...  # Access on port 8080 instead
```

### Health Check Failing

**Test manually:**
```bash
docker exec universal-ai-platform curl http://localhost:5000/core/health
```

**Disable health check (for debugging):**
```yaml
# In docker-compose.yml
healthcheck:
  disable: true
```

### Out of Memory

**Increase memory limit:**
```bash
docker run --memory="1g" ...
```

Or in docker-compose.yml:
```yaml
services:
  web:
    mem_limit: 1g
```

---

## 🚢 Deployment Platforms

### AWS ECS/Fargate
```bash
# Build and push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.region.amazonaws.com
docker tag universal-ai-platform:latest <account>.dkr.ecr.region.amazonaws.com/universal-ai:latest
docker push <account>.dkr.ecr.region.amazonaws.com/universal-ai:latest
```

### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/universal-ai
gcloud run deploy --image gcr.io/PROJECT-ID/universal-ai --platform managed
```

### Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name universal-ai-platform \
  --image universal-ai-platform \
  --dns-name-label universal-ai \
  --ports 5000
```

### DigitalOcean App Platform
```yaml
# .do/app.yaml
name: universal-ai-platform
services:
  - name: web
    github:
      repo: your-username/your-repo
      branch: main
    dockerfile_path: Dockerfile
    http_port: 5000
    envs:
      - key: GEMINI_API_KEY
        scope: RUN_TIME
        type: SECRET
```

---

## 📈 Performance Tuning

### Optimize Worker Count
```python
# Calculate optimal workers
import multiprocessing
workers = (2 * multiprocessing.cpu_count()) + 1
```

### Enable Caching
Add Redis for response caching:

```yaml
# docker-compose.yml
services:
  web:
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### Resource Limits
```yaml
# docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

---

## 🧪 Testing the Docker Image

### Run Tests Inside Container
```bash
docker run --rm universal-ai-platform pytest
```

### Interactive Shell
```bash
docker exec -it universal-ai-platform /bin/bash
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/core/health

# Direct API
curl -X POST http://localhost:5000/api/direct \
  -H "Content-Type: application/json" \
  -d '{"parts": ["Hello"], "model_name": "gemini-2.5-flash"}'
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)

---

## 💡 Tips

1. **Always use `.dockerignore`** to reduce image size
2. **Pin dependency versions** in requirements.txt for reproducibility
3. **Use health checks** to ensure container reliability
4. **Monitor resource usage** with `docker stats`
5. **Keep images updated** with security patches
6. **Use Docker secrets** for sensitive data in production
7. **Enable logging drivers** for centralized log management

---

## 🆘 Support

For issues or questions:
- Check container logs: `docker logs universal-ai-platform`
- Review health status: `docker inspect universal-ai-platform`
- Verify environment variables: `docker exec universal-ai-platform env`

---

**Built with ❤️ for containerized deployment**

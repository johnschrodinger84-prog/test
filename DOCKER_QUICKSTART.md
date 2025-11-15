# Docker Quick Start 🐳

Get the Universal AI Platform running in Docker in under 2 minutes.

---

## Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Gemini API key ([Get API Key](https://ai.google.dev/))

---

## 🚀 Option 1: Docker Compose (Recommended)

### 1. Create `.env` file
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### 2. Start the application
```bash
docker-compose up -d
```

### 3. Test it
```bash
curl http://localhost:5000/core/health
```

**✅ Done!** Your API is running at http://localhost:5000

---

## 🐳 Option 2: Docker Run

### 1. Build the image
```bash
docker build -t universal-ai-platform .
```

### 2. Run the container
```bash
docker run -d \
  --name universal-ai-platform \
  -p 5000:5000 \
  -e GEMINI_API_KEY=your_api_key_here \
  universal-ai-platform
```

### 3. Check logs
```bash
docker logs -f universal-ai-platform
```

---

## 📋 Useful Commands

| Action | Command |
|--------|---------|
| **Stop** | `docker-compose down` |
| **View logs** | `docker-compose logs -f` |
| **Restart** | `docker-compose restart` |
| **Rebuild** | `docker-compose up -d --build` |
| **Shell access** | `docker exec -it universal-ai-platform bash` |

---

## 🧪 Test the API

### Health Check
```bash
curl http://localhost:5000/core/health
```

### Direct AI Query
```bash
curl -X POST http://localhost:5000/api/direct \
  -H "Content-Type: application/json" \
  -d '{
    "parts": ["What is 2+2?"],
    "model_name": "gemini-2.5-flash"
  }'
```

### Diet Tracker Example
```bash
curl -X POST http://localhost:5000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "diet-tracker",
    "data": {
      "user_task": "Create a meal plan",
      "is_image_used": false,
      "selected_solution_language": "English",
      "physical_activity": "moderate",
      "gender": "male",
      "age": 30,
      "height": 175.0,
      "weight": 80.0
    }
  }'
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Use a different port
docker run -p 8080:5000 ...
# Access at http://localhost:8080
```

### Check Container Status
```bash
docker ps -a
```

### View Container Logs
```bash
docker logs universal-ai-platform
```

### Restart Container
```bash
docker restart universal-ai-platform
```

---

## 📚 Full Documentation

For detailed deployment options, see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

For API documentation, see [API_CLIENT_GUIDE.md](API_CLIENT_GUIDE.md)

# MPAssist Docker Setup

## Quick Start

### First Time Setup

1. **Build the Docker images:**
   ```bash
   cd docker
   docker compose build
   ```

2. **Start Ollama service (background):**
   ```bash
   docker compose up -d ollama
   ```
   Wait ~30 seconds for Ollama to be ready.

3. **Run MPAssist (interactive mode):**
   ```bash
   docker compose run --rm mpassist-app
   ```

   This will:
   - Wait for Ollama to be ready
   - Pull required models (llama3, mxbai-embed-large)
   - Run ingest.py to create vector database
   - Start the interactive CLI

### Subsequent Runs

Once the database is created, simply run:
```bash
cd docker
docker compose run --rm mpassist-app
```

The entrypoint script will detect the existing database and skip ingestion.

## Commands

### Interactive Mode (Recommended)
```bash
docker compose run --rm mpassist-app
```
- Opens interactive terminal
- You can type commands and chat with the agent
- Exit with Ctrl+C

### Background Mode (Not recommended for CLI)
```bash
docker compose up -d
```
- Runs in background, but you won't be able to interact
- Use `docker logs -f mpassist_app` to see output

### Rebuild After Code Changes
```bash
docker compose build --no-cache
docker compose run --rm mpassist-app
```

### Reset Database (Force Re-ingestion)
```bash
# Delete the database folder on your host
rm -rf ../db

# Run again
docker compose run --rm mpassist-app
```

### Stop All Services
```bash
docker compose down
```

## Architecture

### Services

1. **ollama** - LLM service
   - Runs Ollama for embeddings and chat
   - Persists models in `docker/ollama_models/`
   - Healthcheck ensures it's ready before app starts

2. **mpassist-app** - Python application
   - Runs the multi-agent RAG system
   - Mounts `src/`, `db/`, and `masterportal-docs/` from host
   - Interactive terminal mode

### Startup Flow

```
docker compose run --rm mpassist-app
  ↓
entrypoint.sh starts
  ↓
[1/5] Wait for Ollama (health check)
  ↓
[2/5] Pull models (llama3, mxbai-embed-large)
  ↓
[3/5] Check database
  ├─ Exists? Skip ingestion
  └─ Missing? Run ingest.py
  ↓
[4/5] Verify dependencies
  ↓
[5/5] Start main.py (interactive CLI)
  ↓
👤 You: [ready to chat]
```

## Troubleshooting

### "Ollama service did not become ready"
- Check if Ollama container is running: `docker ps`
- Check Ollama logs: `docker logs ollama_service`
- Try restarting: `docker compose restart ollama`

### "Ingestion failed"
- Check if masterportal-docs folder exists
- Check disk space
- View full logs in terminal output

### "Cannot connect to Ollama"
- Ensure OLLAMA_HOST env var is set correctly
- Check network: `docker network ls`
- Verify containers are on same network

### Code changes not reflected
- Source files are mounted, so changes should appear immediately
- If not, rebuild: `docker compose build`

## Environment Variables

- `OLLAMA_HOST` - Ollama service URL (default: http://ollama:11434)

## Volumes

- `../src` → `/app/src` - Source code (hot-reload)
- `../db` → `/app/db` - Vector database (persisted)
- `../masterportal-docs` → `/app/masterportal-docs` - Documentation
- `./ollama_models` → `/root/.ollama` - Ollama models (persisted)

## Network

All services run on the default `docker_default` network, allowing them to communicate using service names (e.g., `http://ollama:11434`).

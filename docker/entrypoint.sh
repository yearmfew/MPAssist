#!/bin/bash
set -e

echo "================================================"
echo "MPAssist Docker Startup Script"
echo "================================================"

# ============================================================================
# STEP 1: Wait for Ollama service to be ready
# ============================================================================
echo ""
echo "[1/5] Waiting for Ollama service..."

MAX_RETRIES=30
RETRY_COUNT=0

until curl -s http://ollama:11434/api/tags > /dev/null 2>&1; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "ERROR: Ollama service did not become ready after $MAX_RETRIES attempts"
    echo "Please check if the ollama container is running properly"
    exit 1
  fi
  
  echo "  Waiting for Ollama... (attempt $RETRY_COUNT/$MAX_RETRIES)"
  sleep 2
done

echo "  ✓ Ollama service is ready"

# ============================================================================
# STEP 2: Pull required Ollama models (if not already present)
# ============================================================================
echo ""
echo "[2/5] Checking Ollama models..."

# Check if llama3 exists
if ! curl -s http://ollama:11434/api/tags | grep -q "llama3"; then
  echo "  Pulling llama3 model (this may take a while)..."
  curl -X POST http://ollama:11434/api/pull -d '{"name": "llama3"}' 2>&1 | grep -v "^$"
  echo "  ✓ llama3 model ready"
else
  echo "  ✓ llama3 model already exists"
fi

# Check if mxbai-embed-large exists
if ! curl -s http://ollama:11434/api/tags | grep -q "mxbai-embed-large"; then
  echo "  Pulling mxbai-embed-large model (this may take a while)..."
  curl -X POST http://ollama:11434/api/pull -d '{"name": "mxbai-embed-large"}' 2>&1 | grep -v "^$"
  echo "  ✓ mxbai-embed-large model ready"
else
  echo "  ✓ mxbai-embed-large model already exists"
fi

# ============================================================================
# STEP 3: Check if vector database exists, run ingestion if needed
# ============================================================================
echo ""
echo "[3/5] Checking vector database..."

DB_FILE="/app/db/chroma.sqlite3"

if [ ! -f "$DB_FILE" ]; then
  echo "  Vector database not found. Running ingestion..."
  echo "  This will process documents and create embeddings..."
  echo ""
  
  cd /app
  python3 ingest.py
  
  if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Ingestion failed!"
    echo "Please check the logs above for details"
    exit 1
  fi
  
  echo ""
  echo "  ✓ Ingestion completed successfully"
else
  echo "  ✓ Vector database found (skipping ingestion)"
  echo "    To re-ingest, delete the db/ folder and restart"
fi

# ============================================================================
# STEP 4: Verify all dependencies are ready
# ============================================================================
echo ""
echo "[4/5] Verifying dependencies..."

# Check if db exists
if [ ! -d "/app/db" ]; then
  echo "  ERROR: Database directory not found!"
  exit 1
fi

# Check if masterportal-docs exists
if [ ! -d "/app/masterportal-docs" ]; then
  echo "  WARNING: masterportal-docs directory not found!"
  echo "  The application may not work correctly without documentation"
fi

echo "  ✓ All dependencies verified"

# ============================================================================
# STEP 5: Start the MPAssist application
# ============================================================================
echo ""
echo "[5/5] Starting MPAssist CLI..."
echo "================================================"
echo ""

cd /app/src
exec python3 main.py

# MPAssist

Masterportal Configuration Assistant - Generate `config.json` files using AI.

This application helps you create configuration files for the Masterportal WebGIS platform through an interactive conversational interface powered by IONOS AI Model Hub.

## Quick Start (Web Interface)

### Prerequisites
- Python 3.10+

### Installation (Docker)

1. Clone the repository and change into the project directory:

```bash
git clone <repo-url>
cd MPAssist
```
2. Create .env file using env.example file. Paste your Token here

3. Create vector database using ingest.py
```bash
python ingest.py
```
4. Change into the Docker directory:

```bash
cd docker
```

5. Build the Docker image:

```bash
docker-compose build --no-cache
```

6. Start the container:

```bash
docker-compose up
```

The web app will be available at: http://localhost:7860


## Some helper commands (Development)

- Docker — remove all unused images, containers and volumes:
```bash
docker system prune -a --volumes
```

- Clear Python cache:
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
```
# MPAssist

Masterportal Configuration Assistant - Generate `config.json` files using AI and RAG.

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

3. Change into the Docker directory:

```bash
cd docker
```

4. Build the Docker image:

```bash
docker-compose build --no-cache
```

5. Start the container:

```bash
docker-compose up
```

The web app will be available at: http://localhost:7860

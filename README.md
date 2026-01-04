# MPAssist
Config file creation using llms. 

# Run project on local with python

## 1. Start Ollama service
ollama serve

## 2. Pull required models (first time only)
ollama pull llama3
ollama pull mxbai-embed-large

## 3. Install Python dependencies
pip install -r requirements.txt

## 4. Create vector database (first time only)
python ingest.py

## 5. Run the application
cd src
python main.py


# Quick Start with Docker

*NOTE:* Using Ollama on docker container forces the system. It could be harmful if your system not have that power.
On mac m1 and 16GB Ram it makes too much noises at the last step :) 

Running LLM on container will be removed in later processes of project. 
Right now it is not recommended to run the app on docker.

## 1. Clone the repository
git clone <repo-url>
cd MPAssist

## 2. Navigate to docker directory
cd docker

## 3. Build and start Ollama service
docker-compose up -d ollama

## 4. Run the application
docker-compose run --rm mpassist-app






## Clear python cache folders on terminal in src ordner 

find . -type d -name "__pycache__" -exec rm -rf {} +
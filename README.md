# MPAssist
Config file creation using llms. 

---

## 🚀 Quick Start with Virtual Environment (Recommended)

### Prerequisites
- Python 3.8+ installed on your system
- Ollama installed and running locally

### Installation

#### 1. Clone the repository
```bash
git clone <repo-url>
cd MPAssist
```

#### 2. Run setup script
This will create a virtual environment and install all dependencies:
```bash
./setup.sh
```
    If there are problems becuase of python and pip try this
    sudo apt install python3.8-venv

#### 3. Start Ollama service
In a separate terminal:
```bash
ollama serve
```

#### 4. Pull required models (first time only)
```bash
ollama pull llama3
ollama pull mxbai-embed-large
```

#### 5. Activate virtual environment
```bash
source venv/bin/activate
```

#### 6. Create vector database (first time only)
```bash
python ingest.py
```

#### 7. Run the application
```bash
./run.sh
```

### Daily Usage

After initial setup, you only need:
```bash
# 1. Make sure Ollama is running (in a separate terminal)
ollama serve

# 2. Run the application
./run.sh
```

### Manual Virtual Environment Management

If you prefer to manage the virtual environment manually:

#### Create virtual environment
```bash
python3 -m venv venv
```

#### Activate virtual environment
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Deactivate virtual environment (when done)
```bash
deactivate
```

---

## 🐍 Run project on local with Python (without venv)

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

---

# 🐳 Quick Start with Docker

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
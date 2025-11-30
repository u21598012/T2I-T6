# Ubuntu Health Advice System

A comprehensive health advice system that combines AI-powered agents with a user-friendly Streamlit interface to provide personalized medical precautions, dietary recommendations, and side effect information.

## Architecture

The system consists of several components:

- **Flask API** ([api.py](api.py)) - Backend API that interfaces with ARK AI agents
- **Streamlit UI** ([ui/app.py](ui/app.py)) - User-friendly web interface with authentication
- **ARK Agents** - AI agents for medical precautions, dietary advice, side effects, and health summaries
- **JSON Server** - Mock database for patient data and recommendations
- **FastAPI Service** ([main.py](main.py)) - News API integration for health-related articles

## Prerequisites

- Python 3.11+
- Node.js and npm (for ARK platform)
- ARK CLI installed globally (`npm install -g @mckinsey/ark`)
- JSON Server for mock database

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd T2I-T6
```

### 2. Install Python Dependencies

```bash
# Install main API dependencies
pip install -r requirements.txt

# Install Streamlit UI dependencies
cd ui
pip install -r ui/requirements.txt
cd ..
```

### 3. Set Up ARK Agents

Initialize your ARK team with the agents:

```bash
ark team create team/team-v1
ark team add-agent team/team-v1 agents/pda.yaml
ark team add-agent team/team-v1 agents/medical-precaution.yaml
ark team add-agent team/team-v1 agents/dietary.yaml
ark team add-agent team/team-v1 agents/side-effect-agent.yaml
ark team add-agent team/team-v1 agents/sanitizing-agent.yaml
ark team add-agent team/team-v1 agents/health-summary-agent.yaml
```

Add the tools:

```bash
ark tool add tools/get-patient-info.yaml
ark tool add tools/list_patients.yaml
ark tool add tools/get-medical-precautions.yaml
ark tool add tools/get-dietary-recommendations.yaml
```

### 4. Set Up Mock Database

Install JSON Server:

```bash
npm install -g json-server
```

Start JSON Server (in a separate terminal):

```bash
json-server --watch data/db.json --port 5000
```

## Running the Application

You need to start **three services** in separate terminal windows:

### Terminal 1: JSON Server (Mock Database)

```bash
json-server --watch data/db.json --port 5000
```

### Terminal 2: Flask API

```bash
python api.py
```

The Flask API will start on `http://localhost:5001`

### Terminal 3: Streamlit UI

```bash
cd ui
streamlit run app.py
```

The Streamlit app will open automatically in your browser at `http://localhost:8501`

**Default Login Credentials:**
- Username: `Tech2Impact` | Password: `password123`
- Username: `admin` | Password: `admin123`

## Using the Application

### 1. Login Page
- Enter your credentials to access the system
- Default users are defined in [ui/app.py](ui/app.py)

### 2. Patient Info Page
- Fill in patient details (name, age, gender, chronic disease)
- Add allergy information
- Record daily meals (breakfast, lunch, dinner)
- Click "Save Patient Info" to store the data

### 3. Chat Interface
- Ask health-related questions
- The system will provide:
  - Medical precautions based on condition and age
  - Dietary recommendations
  - Potential side effects
  - Personalized health summaries

### Example Prompts:
- "Hi, this is John Doe" (retrieves patient info)
- "What precautions should I take?"
- "What should I eat today?"
- "What side effects might I experience?"

## Project Structure

```
T2I-T6/
├── agents/                          # ARK agent configurations
│   ├── pda.yaml                    # Personal data retrieval agent
│   ├── medical-precaution.yaml     # Medical precautions agent
│   ├── dietary.yaml                # Dietary recommendations agent
│   ├── side-effect-agent.yaml      # Side effects analysis agent
│   ├── sanitizing-agent.yaml       # Content sanitization agent
│   └── health-summary-agent.yaml   # Health summary generator
├── tools/                          # ARK tool configurations
│   ├── get-patient-info.yaml
│   ├── list_patients.yaml
│   ├── get-medical-precautions.yaml
│   └── get-dietary-recommendations.yaml
├── data/
│   └── db.json                     # Mock database
├── ui/
│   ├── app.py                      # Streamlit application
│   ├── requirements.txt            # UI dependencies
│   └── patient_data/               # Patient data storage
├── api.py                          # Flask API server
├── main.py                         # FastAPI news service
├── chatbot_ui.py                   # Alternative chatbot UI
├── requirements.txt                # Main dependencies
└── Dockerfile                      # Docker configuration
```

## API Endpoints

### Flask API (Port 5001)

- `POST /health-advice` - Get health advice based on prompt
- `POST /health-advice/full` - Get complete output with reasoning
- `GET /health` - Health check endpoint

### FastAPI News Service (Port 8080)

- `GET /v1/news?topic={topic}` - Fetch health-related news articles

## Docker Deployment

Build the Docker image:

```bash
docker build -t health-advice-api .
```

Run the container:

```bash
docker run -p 8080:8080 health-advice-api
```

## Troubleshooting

### Common Issues

**"Could not connect to API"**
- Ensure Flask API is running on port 5001
- Check if JSON Server is running on port 5000

**"ARK query failed"**
- Verify ARK CLI is installed: `ark --version`
- Check that agents are properly registered: `ark team list`
- Ensure tools are added: `ark tool list`

**"No patient data found"**
- Fill in patient information in the "Patient Info" page first
- Verify JSON Server is running with [data/db.json](data/db.json)

## Features

**Multi-Agent System**
- Personal data retrieval
- Medical precaution analysis
- Dietary recommendations
- Side effect identification
- Content sanitization
- Health summary generation

**User-Friendly Interface**
- Secure authentication
- Patient data management
- Meal tracking
- Real-time chat interface
- Session persistence

**Smart Recommendations**
- Age-specific guidance
- Gender-specific considerations
- Allergy accommodations
- Meal-based dietary advice

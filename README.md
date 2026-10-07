# Drone Simulation AI

This project now includes a Python AI layer for mission planning and autonomous decision support.

## Backend

The backend is built with FastAPI and can run independently from the Next.js frontend.

### Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:
- `GET /health`
- `GET /api/ai/health`
- `GET /api/ai/providers`
- `POST /api/ai/drone-decision`
- `POST /api/ai/mission-plan`

## Frontend integration

Use the following Next.js commands:

```bash
pnpm install
pnpm dev:backend
pnpm dev
```

Or run both together:

```bash
pnpm dev:full
```

## AI capabilities

- drone safety scoring
- dynamic mission planning
- weather-aware route adjustments
- battery-preservation logic
- OpenAI or Ollama provider support
- mock mode for offline use

## Environment variables

Create `backend/.env` based on `.env.example` and set:

```bash
LLM_PROVIDER=mock
OPENAI_API_KEY=your_key_here
```

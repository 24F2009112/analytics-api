# POST Analytics API

FastAPI service for the course analytics-endpoint exercise.

## Endpoint

`POST /analytics`

Required header:

`X-API-Key: ak_wk7olr880u9mti1s69g9omph`

Example body:

```json
{
  "events": [
    {"user": "alice", "amount": 42.5, "ts": 1700000000},
    {"user": "bob", "amount": -5, "ts": 1700000001},
    {"user": "alice", "amount": 12, "ts": 1700000002}
  ]
}
```

Response fields:

- `email`: `24f2009112@ds.study.iitm.ac.in`
- `total_events`: number of events in the batch
- `unique_users`: count of distinct user values
- `revenue`: sum of positive `amount` values only
- `top_user`: user with the highest combined total of positive amounts; the assignment says test batches have no ties

Missing or incorrect API keys return HTTP 401. CORS is enabled for browser-based grading.

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Deploy on Render

Create a Python web service from this repository.

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Submit the deployed service URL ending in `/analytics`.

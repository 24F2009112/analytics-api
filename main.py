import os
from collections import defaultdict
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Assigned for this course evaluation. Override with ANALYTICS_API_KEY if desired.
API_KEY = os.getenv("ANALYTICS_API_KEY", "ak_wk7olr880u9mti1s69g9omph")
STUDENT_EMAIL = "24f2009112@ds.study.iitm.ac.in"

app = FastAPI(title="POST Analytics API", version="1.0.0")

# The assignment requires the browser-based grader to be able to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int | float


class AnalyticsRequest(BaseModel):
    events: list[Event] = Field(default_factory=list)


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "analytics-api"}


@app.post("/analytics")
def analytics(
    payload: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> dict[str, Any]:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = payload.events
    positive_totals: dict[str, float] = defaultdict(float)
    revenue = 0.0
    users: set[str] = set()

    for event in events:
        users.add(event.user)
        if event.amount > 0:
            revenue += event.amount
            positive_totals[event.user] += event.amount

    # The grader specifies that generated batches have no top-user ties.
    top_user = max(positive_totals, key=positive_totals.get) if positive_totals else None

    return {
        "email": STUDENT_EMAIL,
        "total_events": len(events),
        "unique_users": len(users),
        "revenue": round(revenue, 10),
        "top_user": top_user,
    }

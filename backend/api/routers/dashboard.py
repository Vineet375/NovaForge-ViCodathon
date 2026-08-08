from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

class StatCard(BaseModel):
    title: str
    value: str
    subtitle: str

class ActivityItem(BaseModel):
    id: str
    title: str
    description: str
    time: str
    type: str  # e.g., "success", "info", "warning"

class DashboardResponse(BaseModel):
    stats: List[StatCard]
    activities: List[ActivityItem]

@router.get("", response_model=DashboardResponse)
def get_dashboard_data():
    return DashboardResponse(
        stats=[
            StatCard(title="Completed Interviews", value="12", subtitle="+2 from last month"),
            StatCard(title="Average Score", value="84%", subtitle="+5% improvement"),
            StatCard(title="Questions Answered", value="142", subtitle="Across 6 domains"),
            StatCard(title="Active Session", value="Frontend System Design", subtitle="45 minutes remaining"),
        ],
        activities=[
            ActivityItem(
                id="a1",
                title="Completed System Design Mock",
                description="Scored 85% on distributed systems questions.",
                time="2 hours ago",
                type="success"
            ),
            ActivityItem(
                id="a2",
                title="Generated New Feedback",
                description="AI identified 3 areas for improvement in React state management.",
                time="5 hours ago",
                type="info"
            ),
            ActivityItem(
                id="a3",
                title="Started Algorithm Practice",
                description="Focused on dynamic programming patterns.",
                time="Yesterday",
                type="warning"
            )
        ]
    )

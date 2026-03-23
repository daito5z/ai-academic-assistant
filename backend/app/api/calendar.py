from fastapi import APIRouter
from app.services.calendar_service import CalendarService

router = APIRouter()


@router.get("/calendar")
def get_calendar():

    events = CalendarService.get_upcoming_events()

    return {"events": events}

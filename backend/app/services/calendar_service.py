from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from app.services.time_parser import parse_time_range

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class CalendarService:

    @staticmethod
    def authenticate():

        flow = InstalledAppFlow.from_client_secrets_file(
            "storage/google/credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        service = build("calendar", "v3", credentials=creds)

        return service

    @staticmethod
    def get_events_for_query(query: str):

        service = CalendarService.authenticate()

        start_time, end_time = parse_time_range(query)

        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        formatted_events = []

        for event in events:

            start = event["start"].get("dateTime", event["start"].get("date"))

            formatted_events.append({
                "title": event.get("summary", "No Title"),
                "start": start
            })

        return formatted_events

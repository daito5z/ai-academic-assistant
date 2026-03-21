from fastapi import APIRouter
from app.knowledge.email_ingestor import ingest_emails

router = APIRouter()


@router.post("/sync-emails")
def sync_emails():

    ingest_emails()

    return {"message": "Emails synced successfully"}

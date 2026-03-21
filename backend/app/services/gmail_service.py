from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.utils import parseaddr
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailService:

    @staticmethod
    def authenticate():
        flow = InstalledAppFlow.from_client_secrets_file(
            "storage/google/credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)
        service = build("gmail", "v1", credentials=creds)

        return service

    @staticmethod
    def _extract_body(payload):
        """Recursively extract plain text body"""

        if "parts" in payload:
            for part in payload["parts"]:
                mime_type = part.get("mimeType", "")

                if mime_type == "text/plain":
                    data = part["body"].get("data")
                    if data:
                        return base64.urlsafe_b64decode(data).decode(errors="ignore")

                # Recursively check nested parts
                result = GmailService._extract_body(part)
                if result:
                    return result
        else:
            # Fallback (no parts, direct body)
            data = payload.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode(errors="ignore")

        return ""

    @staticmethod
    def fetch_recent_emails(max_results=20):
        service = GmailService.authenticate()

        results = service.users().messages().list(
            userId="me",
            maxResults=max_results
        ).execute()

        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            message = service.users().messages().get(
                userId="me",
                id=msg["id"]
            ).execute()

            payload = message.get("payload", {})
            headers = payload.get("headers", [])

            # Extract headers
            sender_raw = next(
                (h["value"] for h in headers if h["name"] == "From"),
                ""
            )

            subject = next(
                (h["value"] for h in headers if h["name"] == "Subject"),
                ""
            )

            date_raw = next(
                (h["value"] for h in headers if h["name"] == "Date"),
                ""
            )

            # Parse sender
            sender_name, sender_email = parseaddr(sender_raw)

            # Reliable received time
            internal_ts = int(message.get("internalDate", 0)) / 1000
            received_datetime = datetime.fromtimestamp(internal_ts)

            # Extract body
            body = GmailService._extract_body(payload)

            emails.append({
                "id": msg["id"],
                "sender_name": sender_name,
                "sender_email": sender_email,
                "subject": subject,
                "date_header": date_raw,              # original header
                "received_at": received_datetime,     # reliable timestamp
                "body": body
            })

        return emails

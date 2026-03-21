from app.services.gmail_service import GmailService
from app.services.email_summarizer import EmailSummarizer
from app.knowledge.chunker import chunk_text
from app.knowledge.embeddings import generate_embeddings
from app.knowledge.vector_store import store_embeddings, document_exists


def clean_body(text: str) -> str:
    """Basic cleanup to reduce noise"""
    if not text:
        return ""
    return " ".join(text.split())  # remove extra whitespace


def ingest_emails():

    emails = GmailService.fetch_recent_emails(max_results=5)

    for email in emails:

        message_id = email["id"]

        # 🔴 Skip duplicates
        if document_exists(message_id):
            print(f"Skipping duplicate email: {message_id}")
            continue

        # ✅ Clean body
        body = clean_body(email["body"])

        # ✅ Step 1: Chunk the email body
        chunks = chunk_text(body, max_tokens=300)

        # ✅ Step 2: Limit number of chunks (VERY IMPORTANT)
        chunks = chunks[:3]  # prevent token explosion

        chunk_summaries = []

        # ✅ Step 3: Summarize each chunk
        for chunk in chunks:
            summary_part = EmailSummarizer.summarize_email(
                email["sender_name"] or email["sender_email"],
                email["subject"],
                chunk,
                str(email["received_at"])
            )
            chunk_summaries.append(summary_part)

        # ✅ Step 4: Combine summaries
        combined_summary = " ".join(chunk_summaries)

        # ✅ Step 5: (Optional but powerful) Final refinement pass
        final_summary = EmailSummarizer.combine_summaries(combined_summary)

        # ✅ Step 6: Store embeddings
        summary_chunks = [
            final_summary.strip()] if final_summary.strip() else []
        embeddings = generate_embeddings(summary_chunks)

        store_embeddings(
            summary_chunks,
            embeddings,
            document_name="gmail",
            metadata_extra={
                "source": "gmail",
                "sender_name": email["sender_name"],
                "sender_email": email["sender_email"],
                "subject": email["subject"],
                "received_at": str(email["received_at"]),
                "message_id": message_id
            }
        )

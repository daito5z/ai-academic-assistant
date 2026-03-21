from app.config.settings import settings
from groq import Groq

client = Groq(api_key=settings.groq_api_key)


class EmailSummarizer:

    @staticmethod
    def summarize_email(sender, subject, body, date):

        MAX_INPUT_CHARS = 3000
        body = body[:MAX_INPUT_CHARS]

        prompt = f"""
            Summarize the email clearly.

            Sender: {sender}
            Date: {date}
            Subject: {subject}
            Body: {body}
            """

        messages = [
            {
                "role": "system",
                "content": """
                You are an academic assistant that summarizes emails with sender, topic, key points, deadlines, and actions. Keep it concise and clear.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = client.chat.completions.create(
            model=settings.model_name,
            messages=messages
        )

        return response.choices[0].message.content

    @staticmethod
    def combine_summaries(text):

        MAX_INPUT_CHARS = 3000
        text = text[:MAX_INPUT_CHARS]

        response = client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "Combine and refine into one clear, concise summary."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        return response.choices[0].message.content

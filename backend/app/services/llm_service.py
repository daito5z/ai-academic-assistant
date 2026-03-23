from datetime import datetime
from app.knowledge.retriever import retrieve_context
from app.config.settings import settings
from groq import Groq
from app.knowledge.memory_ingestor import store_interaction
from app.services.session_manager import SessionManager
from app.services.calendar_service import CalendarService


client = Groq(api_key=settings.groq_api_key)


def is_calendar_query(query: str):
    keywords = [
        "schedule", "calendar", "meeting",
        "class", "tomorrow", "today",
        "event", "deadline"
    ]
    return any(word in query.lower() for word in keywords)


def format_events(events):

    formatted = []

    for e in events:
        dt = datetime.fromisoformat(e["start"].replace("Z", ""))
        formatted.append(f"{e['title']} at {dt.strftime('%I:%M %p on %d %b')}")

    return "\n".join(formatted)


class LLMService:

    @staticmethod
    def generate_response(prompt: str, session_id: str):

        if is_calendar_query(prompt):

            print("Detected calendar query")

            events = CalendarService.get_events_for_query(prompt)

            if not events:
                return "You don’t have any upcoming events."

            events_text = format_events(events)

            messages = [
                {
                    "role": "system",
                    "content": """
            You are a smart academic assistant.

            - Answer clearly and naturally
            - Summarize events instead of listing blindly
            - If multiple events, organize them nicely
            """
                },
                {
                    "role": "user",
                    "content": f"""
            Upcoming events:

            {events_text}

            User question:
            {prompt}
            """
                }
            ]

            response = client.chat.completions.create(
                model=settings.model_name,
                messages=messages
            )

            return response.choices[0].message.content

        print(f"Generating response for prompt: {prompt}")

        history = SessionManager.get_history(session_id)

        context_chunks = retrieve_context(prompt)[:4]

        print(
            f"Retrieved {len(context_chunks)} context chunks from vector store.")

        context = "\n\n".join(
            [f"[Source: {chunk}]" for chunk in context_chunks]
        )

        print(f"Constructed context for LLM:\n{context}")

        messages = [
            {
                "role": "system",
                "content": """
                You are a smart, friendly personal academic assistant.
                - Be concise but helpful
                - Sound natural, not robotic
                - If the user asks casually, respond casually
                - If academic, respond clearly and structured
                - Prefer PDF for conceptual questions
                - Prefer email for announcements
                - Prefer memory for past interactions
                - Answer naturally


                Guidelines:
                - Use the provided context if available
                - If context is insufficient, use your own knowledge
                - Do NOT mention "context" or say you couldn't find information
                - Answer naturally like a human assistant
                - Be clear, helpful, and slightly conversational
                """
            },
            {"role": "user", "content": f"Answer the question using the provided context. "
             f"If the answer is not in the context"
             f"Then attempt to answer based on general knowledge.\n\n"
             f"Context:\n{context}\n\nQuestion:\n{prompt}"}
        ]

        messages.extend(history)

        messages.append({
            "role": "user",
            "content": f"""
            Context:
            {context}

            Question:
            {prompt}
            """
        })

        response = client.chat.completions.create(
            model=settings.model_name,
            messages=messages
        )

        print(
            f"Received response from LLM: {response.choices[0].message.content}")

        response_text = response.choices[0].message.content

        SessionManager.add_message(session_id, "user", prompt)
        SessionManager.add_message(session_id, "assistant", response_text)

        store_interaction(prompt, response_text)

        return response_text

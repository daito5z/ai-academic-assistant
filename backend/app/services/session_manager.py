class SessionManager:

    sessions = {}

    @classmethod
    def get_history(cls, session_id):
        return cls.sessions.get(session_id, [])

    @classmethod
    def add_message(cls, session_id, role, content):

        if session_id not in cls.sessions:
            cls.sessions[session_id] = []

        cls.sessions[session_id].append({
            "role": role,
            "content": content
        })

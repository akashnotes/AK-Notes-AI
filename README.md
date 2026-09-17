# AK Notes AI backend
1. Install Python 3.10+.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your OpenAI API key.
4. Run: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Android app's BASE_URL must point to this server.

Keep the API key only on the server, never inside the APK.
Some YouTube videos do not expose usable captions/transcripts; those will return an error.

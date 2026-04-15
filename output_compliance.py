import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)


SYSTEM_PROMPT = """
You are a financial compliance classifier.

Classify the investment message into ONE of these categories:

Approved
Requires Review
Rejected

Rules:
- Reject messages containing phrases like:
  "Guaranteed returns", "Risk-free", "Double your money", "Assured returns".
- Reject unrealistic performance claims.
- Requires Review if the message appears promotional or gives investment advice.
- Approve neutral informational messages like research updates or product announcements.

IMPORTANT:
Return ONLY one word:
Approved
Requires Review
Rejected
"""


def classify_message(message):

    if not message:
        return "Requires Review"

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nMessage:\n{message}\n\nClassification:"
        )

        result = response.text.strip()

        if "Approved" in result:
            return "Approved"

        if "Rejected" in result:
            return "Rejected"

        if "Requires Review" in result:
            return "Requires Review"

        return "Requires Review"

    except Exception as e:
        print("Gemini API error:", e)
        return "Requires Review"
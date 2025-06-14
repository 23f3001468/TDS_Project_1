import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Tuple
import requests
import time

load_dotenv()

AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

# Use absolute path resolution for Render compatibility
BASE_DIR = Path(__file__).resolve().parent
COURSE_FILE = BASE_DIR / "all_course_sections.txt"
DISCOURSE_FILE = BASE_DIR / "tds_discourse_scraped.txt"

# Safe file reading with fallback
try:
    COURSE_TEXT = COURSE_FILE.read_text(encoding="utf-8")[:20000]  # reduced size for speed
except FileNotFoundError:
    COURSE_TEXT = "(Course content file not found.)"

try:
    DISCOURSE_TEXT = DISCOURSE_FILE.read_text(encoding="utf-8")[:10000]
except FileNotFoundError:
    DISCOURSE_TEXT = "(Discourse content file not found.)"

SYSTEM_CONTEXT = (
    "You are a helpful virtual teaching assistant for IIT Madras' Tools in Data Science course.\n"
    "Use the content below to answer the user's question.\n\n"
    "=== COURSE CONTENT ===\n" + COURSE_TEXT +
    "\n\n=== DISCOURSE POSTS ===\n" + DISCOURSE_TEXT
)

def get_answer_and_links(question: str, image: str = None) -> Tuple[str, List[dict]]:
    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_CONTEXT},
            {"role": "user", "content": question}
        ]
    }

    answer = ""
    for attempt in range(2):
        try:
            response = requests.post(AIPROXY_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
            break
        except requests.exceptions.Timeout:
            if attempt == 0:
                print("Timeout occurred. Retrying...")
                time.sleep(2)
            else:
                answer = "Request timed out. Please try again later."
        except Exception as e:
            answer = f"An error occurred: {str(e)}"
            break

    links = [
        {"url": "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34", "text": "TDS Discourse Discussions"},
        {"url": "https://tds.s-anand.net/#/2025-01/", "text": "Course Content Reference"}
    ]

    return answer, links
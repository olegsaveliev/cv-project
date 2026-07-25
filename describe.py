"""
Turn a single camera frame into a one-sentence description via Claude's vision model.

One job, one function: describe(jpeg_bytes) -> str | None.
It is deliberately "fail open" — any problem (no key, network down, bad response,
slow API) returns None so the caller can fall back to the plain YOLO label. The
alert must never be blocked by this call.

Standalone test (Step 3):
    export ANTHROPIC_API_KEY=...        # the service loads .env for you; a shell does not
    python "describe.py" alert.jpg
"""

import os
import sys
import base64
import requests

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = "claude-haiku-4-5"          # vision-capable, cheapest tier, fast
API_URL = "https://api.anthropic.com/v1/messages"

# Haiku 4.5 pricing, per token (check anthropic.com/pricing before quoting).
IN_PRICE = 1e-6                     # $1 per million input tokens
OUT_PRICE = 5e-6                    # $5 per million output tokens

# The prompt is most of the output quality. We tell Claude three things:
# the context (fixed security camera), the format (one plain sentence), and
# what a *notification* actually needs (who/what, doing what, anything unusual).
PROMPT = (
    "This is a single still frame from a fixed home security camera. "
    "In one plain sentence, describe who or what is in view, what they appear "
    "to be doing, and anything they are carrying or anything unusual. "
    "No preamble, no markdown, no hedging — just the sentence. "
    "If the frame is too dark or blurry to read, say so plainly instead of guessing."
)


def describe(jpeg_bytes, timeout=10):
    """Return a one-sentence description of the frame, or None on any failure."""
    if not API_KEY:
        print("describe: ANTHROPIC_API_KEY not set")
        return None
    try:
        b64 = base64.standard_b64encode(jpeg_bytes).decode("utf-8")
        resp = requests.post(
            API_URL,
            headers={
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": 100,          # hard cap on cost and verbosity
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": b64,
                        }},
                        {"type": "text", "text": PROMPT},
                    ],
                }],
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()

        # Log the REAL token counts the API reports, so cost is measured (not
        # estimated) and greppable from the journal (journalctl -u cv-detector).
        u = data.get("usage", {})
        in_tok, out_tok = u.get("input_tokens", 0), u.get("output_tokens", 0)
        cost = in_tok * IN_PRICE + out_tok * OUT_PRICE
        print(f"describe usage: in={in_tok} out={out_tok} cost=${cost:.5f}")

        # With no tools/thinking, the reply is one or more content blocks;
        # grab the first text block rather than assuming it is at index 0.
        sentence = next(b["text"] for b in data["content"] if b["type"] == "text")
        return sentence.strip()
    except Exception as e:
        print(f"describe error: {e}")
        return None


if __name__ == "__main__":
    # Prove it on a still image before touching the live loop.
    path = sys.argv[1] if len(sys.argv) > 1 else "alert.jpg"
    with open(path, "rb") as f:
        result = describe(f.read())
    print(result if result else "(no description — fell back to None)")

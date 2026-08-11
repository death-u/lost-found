import os
import json
from google import genai
from google.genai import types

def analyze_item(uploaded_file):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model = "gemini-3.1-flash-lite"

    # uploaded_file is a Django UploadedFile — read its bytes directly
    image_bytes = uploaded_file.read()

    prompt = """Analyze this lost-and-found item image and respond ONLY with valid JSON
in this exact format, no markdown, no extra text:

{
  "item_type": "string",
  "category":"string",
  "primary_color": "string",
  "secondary_colors": ["array of strings"],
  "material": "string or null",
  "distinguishing_features": ["array of strings"],
  "brand": "string or null",
  "description": "one short sentence"
}"""

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
                types.Part.from_bytes(data=image_bytes, mime_type=uploaded_file.content_type or "image/jpeg"),
            ],
        ),
    ]

    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="MINIMAL"),
        response_mime_type="application/json",
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )

    return json.loads(response.text)
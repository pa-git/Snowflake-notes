import base64
import io
from PIL import Image
import openai

# Use the new client interface
client = openai.OpenAI()  # or use env var

def chat_with_image_path(message, image_path):
    # Load image and encode as base64
    with Image.open(image_path) as image:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

    # Prepare messages
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": message},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_str}"
                    }
                }
            ]
        }
    ]

    # Call GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    return response.choices[0].message.content

# Call it
response = chat_with_image_path("What's in this image?", "sample.PNG")
print(response)

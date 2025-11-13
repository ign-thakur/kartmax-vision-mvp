import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/generate_tags", methods=["POST"])
def generate_tags():
    file = request.files["image"]
    image_bytes = file.read()

    # Step 1: Caption
    caption_prompt = "Describe this product image in one detailed sentence."
    caption_response = genai.GenerativeModel("gemini-2.5-pro").generate_content(
        [caption_prompt, {"mime_type": "image/jpeg", "data": image_bytes}]
    )
    caption = caption_response.text.strip()

    # Step 2: Structured tags
    tag_prompt = f"""
    Based on the caption: "{caption}"
    Extract detailed product attributes in JSON format with these fields:
    category, sub_category, gender, color_primary, color_secondary, pattern, fabric, sleeve_type,
    neck_type, fit_type, length_type, occasion, style, work_type, closure_type, season, wash_care,
    material_finish, trend_tags, keywords (minimum 10).
    Return JSON only.
    """
    tag_response = genai.GenerativeModel("gemini-2.5-pro").generate_content(tag_prompt)
    return jsonify({"caption": caption, "tags": tag_response.text})

if __name__ == "__main__":
    app.run(debug=True)

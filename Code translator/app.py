from flask import Flask, render_template, request
import os
from openai import OpenAI  # Updated import

app = Flask(__name__, static_url_path='/static')


client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

def translate_code(code, source_lang, target_lang):
    """Uses OpenAI API to translate code between languages"""
    prompt = f"Convert this {source_lang} code to {target_lang} while maintaining functionality:\n\n{code}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional code conversion expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Conversion Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    translated_code = error = None
    languages = ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "PHP", "Swift", "Kotlin"]

    if request.method == "POST":
        source_lang = request.form.get("source_lang")
        target_lang = request.form.get("target_lang")
        code_text = request.form.get("code_text", "")
        code_file = request.files.get("code_file")

        # Get code from text input or file upload
        code = code_text
        if code_file and code_file.filename != "":
            code = code_file.read().decode("utf-8")
        
        # Validation checks
        if not code.strip():
            error = "Please provide code through text input or file upload"
        elif source_lang == target_lang:
            error = "Source and target languages must be different"
        else:
            translated_code = translate_code(code, source_lang, target_lang)

    return render_template("index.html", 
                          translated_code=translated_code,
                          error=error,
                          languages=languages)

if __name__ == "__main__":
    app.run(debug=True)
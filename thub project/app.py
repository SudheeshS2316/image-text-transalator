from flask import Flask, render_template, request
import pytesseract
from PIL import Image
from langdetect import detect
import openai

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = 'API KEY'

# Define the translation function
def translate_text(text, target_language):
    prompt = f"Detect the language from the given text and Translate to {target_language}: '{text}'\n\nTranslation:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
        n=1,
        stop=None,
    )
    translation = response.choices[0].text.strip().replace("Translation:", "")
    return translation

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded image file
        image = request.files['image']

        # Read the image using PIL
        image = Image.open(image)

        # Apply OCR to the image
        text = pytesseract.image_to_string(image)

        # Detect the language of the text
        lang = detect(text)

        # Get the target language from the form
        target_language = request.form['target_language']

        # Translate the text
        translated_text = translate_text(text, target_language)

        return render_template('result.html', text=text, lang=lang, translated_text=translated_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Yahan apni Groq wali Key dalo
GROQ_KEY = os.environ.get("GROQ_KEY")
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    product = request.json.get('product', '')
    price = request.json.get('price', '')
    size = request.json.get('size', '')
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-oss-20b",
        "messages": [{"role": "user", "content": f"Ek Pakistani online store ke liye '{product}' ki catchy product description likho Urdu-English mix me. Price: {price} Rs, Size: {size}. Price aur size bhi description me likho. 3-4 lines, emojis ke sath."}]
    }
    
    res = requests.post(url, json=data, headers=headers)
    result = res.json()
    
    try:
        text = result['choices'][0]['message']['content']
        return jsonify({"text": text})
    except:
        return jsonify({"text": f"Error: {result}"})

if __name__ == '__main__':
    app.run(debug=True)
import requests
import nltk
from flask import Flask, request, render_template_string

app = Flask(__name__)

# NLTK setup
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

CITIES = ['london', 'paris', 'tokyo', 'new york', 'berlin']

def get_weather(city="London"):
    try:
        url = f"http://wttr.in/{city}?format=%l:+%t+%C"
        return requests.get(url, timeout=3).text
    except:
        return f"Weather service unavailable"

def extract_city(text):
    try:
        tokens = word_tokenize(text.lower())
        filtered = [w for w in tokens if w not in stopwords.words('english')]
        return next((w for w in filtered if w in CITIES), None)
    except:
        return None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Weather Bot</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 0 auto; padding: 20px; }
        #chatbox { border: 1px solid #ddd; height: 300px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
        form { display: flex; }
        input { flex-grow: 1; padding: 8px; }
        button { padding: 8px 15px; }
    </style>
</head>
<body>
    <h1>Weather Bot</h1>
    <div id="chatbox">
        <div><strong>Bot:</strong> Ask me about weather in London, Paris, Tokyo, etc.</div>
    </div>
    <form action="/chat" method="POST" onsubmit="addUserMessage(this.user_input.value); this.user_input.value=''; return true;">
        <input type="text" name="user_input" placeholder="Type your question..." required>
        <button type="submit">Send</button>
    </form>
    <script>
        function addUserMessage(msg) {
            const chatbox = document.getElementById('chatbox');
            chatbox.innerHTML += `<div><strong>You:</strong> ${msg}</div>`;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def handle_chat():
    user_input = request.form['user_input']
    city = extract_city(user_input) or "London"
    bot_response = get_weather(city)
    
    return f"""
    <div><strong>You:</strong> {user_input}</div>
    <div><strong>Bot:</strong> {bot_response}</div>
    <script>
        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
    </script>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

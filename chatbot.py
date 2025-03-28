from flask import Flask, request, jsonify, render_template
from nltk.chat.util import Chat, reflections
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS

# Define chatbot patterns and responses
pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey!"]
    ],
    [
        r"what is your name?",
        ["I'm a chatbot.", "You can call me bot."]
    ],
    [
        r"bye|goodbye|see you later",
        ["Goodbye!", "See you later!", "Bye!"]
    ],
    # Add more patterns and responses...
]

chatbot = Chat(pairs, reflections)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data['message']
        response = chatbot.respond(user_message)
        if not response:
            response = random.choice(["I'm not sure I understand.", "Could you please rephrase that?"])

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
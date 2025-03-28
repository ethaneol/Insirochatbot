from flask import Flask, request, jsonify, render_template
from nltk.chat.util import Chat, reflections
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
]

chatbot = Chat(pairs, reflections)

button_options = {
    'Main menu': ['giga Birthday Surprise', 'It\'s Raining Data!', 'Free #gigaSurprise', 'gigaBuddy data-only plan', 'Others about promotions', 'Refer-A-Friend'],
    'giga Birthday Surprise': ['Option A', 'Option B', 'Option C'],
    'It\'s Raining Data!': ['Option D', 'Option E'],
    'Free #gigaSurprise': ['Option F', 'Option G', 'Option H'],
    'gigaBuddy data-only plan': ['Option I', 'Option J'],
    'Others about promotions': ['Option K', 'Option L', 'Option M'],
    'Refer-A-Friend': ['Option N', 'Option O']
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/button_action', methods=['POST'])
def button_action():
    data = request.get_json()
    button_value = data['button_value']

    if button_value in button_options:
        return jsonify({
            'response': f'You selected {button_value}.',
            'new_options': button_options.get(button_value, [])
        })
    else:
        return jsonify({'response': 'Unknown button action.', 'new_options': []})


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data['message']
        response = chatbot.respond(user_message)
        if not response:
            response = random.choice(["I'm not sure I understand.", "Could you please rephrase that?"])

        if user_message in button_options:
            return jsonify({
                'response': f'You typed: {user_message}',
                'new_options': button_options.get(user_message, [])
            })

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
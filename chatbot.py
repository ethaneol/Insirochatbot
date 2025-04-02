from flask import Flask, request, jsonify, render_template
from nltk.chat.util import Chat, reflections
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hi bbg!", "Hey!"]
    ],
    [
        r"what is your name?|name?",
        ["I'm a chatbot.", "You can call me Xavier."]
    ],
    [
        r"bye|goodbye|see you",
        ["Goodbye!", "See you later alligator!", "Bye!"]
    ],
]

chatbot = Chat(pairs, reflections)
button_options = {
    'main menu': ['General Enquiries', 'About Us', 'Services', 'Promotions', 'Frequently Asked Questions', 'Join Us'],
    'general enquiries': ['Contact Us', 'Address', 'Hours'],
    'about us': ['Profile Picture', 'Data Usage'],
    'services': ['Promo Info', 'Eligibility', 'How to Claim'],
    'promotions': ['Current Promos', 'Past Promos', 'Future Promos'],
    'frequently asked questions': ['StarHub FAQ', 'Still require more help?'],
    'join us': ['Job Scope', 'Interested?']
}

option_responses = {
    'contact us': 'Email us at <a href="mailto: cso.insiro.com" target="_blank">cso@insiro.com</a> \n '
                  'Contact us at <a href="tel:65 6323 1773" target="_current">+65-6323-1773</a>',

    'address': 'Find us at <a href="https://maps.app.goo.gl/ce1hSqtKcUzyuJak6" target="_blank">49 Tannery Lane</a>' ,

    'hours': 'We are open from 9 AM to 6 PM',

    'profile picture': '<img src="/static/xavier.jpeg" alt="Xavier"> \n <br>'
                       '<p>I’m Xavier! But you can call me baby. Do you have a name you prefer to go by? 😊</p>',

    'data usage': 'Use our StarHub app to view data usage',

    'promo info': 'This promo is for new StarHub broadband users',

    'eligibility': 'You must be 18+ to claim this',

    'how to claim': 'Enter the code at checkout',

    'current promos': 'We have a 20% discount this week',

    'past promos': 'Past promos are listed on our site',

    'future promos': 'We will announce future promos soon',

    'starhub faq': 'Our <a href="https://www.starhub.com/personal/support.html" target="_blank">FAQ</a>',
    'still require more help?': 'Contact us at <br>'
                                ' <a href="tel:65 6323 1773" target="_current">+65-6323-1773</a>',

    'job scope': '<null>',

    'interested?': 'Drop your CV at <br>'
                   '<a href="mailto:normila@insiro.com" target="_blank">normila@insiro.com</a>',
}

@app.route('/')
def index():
    return render_template('index.html', option_responses=option_responses)


@app.route('/button_action', methods=['POST'])
def button_action():
    data = request.get_json()
    button_value = data['button_value'].lower()

    if button_value in option_responses:
        return jsonify({
            'response': option_responses[button_value],
            'new_options': []
        })

    if button_value in button_options:
        return jsonify({
            'response': f'You selected {data["button_value"]}.',
            'new_options': button_options.get(button_value, [])
        })
    else:
        return jsonify({'response': 'Unknown button action.', 'new_options': []})


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data['message'].lower()

        response = chatbot.respond(data['message'])
        if not response:
            response = random.choice(["Why did you redeem it!?", "You are gay"])

        if user_message in option_responses:
            return jsonify({
                'response': option_responses[user_message],
                'new_options': []
            })

        if user_message in button_options:
            return jsonify({
                'response': f'{data["message"]}',
                'new_options': button_options.get(user_message, [])
            })

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
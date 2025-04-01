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
        ["I'm a chatbot.", "You can call me Xavier."]
    ],
    [
        r"bye|goodbye|see you later",
        ["Goodbye!", "See you later!", "Bye!"]
    ],
]

chatbot = Chat(pairs, reflections)

button_options = {
    'main menu': ['giga Birthday Surprise', 'It\'s Raining Data!', 'Free #gigaSurprise', 'gigaBuddy data-only plan', 'Others about promotions', 'Refer-A-Friend'],
    'giga birthday surprise': ['Option A - Contact Us', 'Option B - Address', 'Option C - Hours'],
    'it\'s raining data!': ['Option D - Data Plans', 'Option E - Data Usage'],
    'free #gigasurprise': ['Option F - Promo Info', 'Option G - Eligibility', 'Option H - How to Claim'],
    'gigabuddy data-only plan': ['Option I - Plan Details', 'Option J - Activation'],
    'others about promotions': ['Option K - Current Promos', 'Option L - Past Promos', 'Option M - Future Promos'],
    'refer-a-friend': ['Option N - Referral Link', 'Option O - Referral Rules']
}

option_responses = {
    'option a - contact us': 'Our email is cso@insiro.com',
    'option b - address': 'Our address is 49 Tannery Lane, #03-05 S(347796)',
    'option c - hours': 'We are open from 9 AM to 5 PM',
    'option d - data plans': 'Check our website for data plans',
    'option e - data usage': 'Use our app to view data usage',
    'option f - promo info': 'This promo is for new users',
    'option g - eligibility': 'You must be 18+ to claim this',
    'option h - how to claim': 'Enter the code at checkout',
    'option i - plan details': 'This plan includes unlimited data',
    'option j - activation': 'Visit our store to activate',
    'option k - current promos': 'We have a 20% discount this week',
    'option l - past promos': 'Past promos are listed on our site',
    'option m - future promos': 'We will announce future promos soon',
    'option n - referral link': 'Use this link to refer a friend',
    'option o - referral rules': 'Referral rules are on our FAQ'
}

@app.route('/')
def index():
    return render_template('index.html')


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
            response = random.choice(["I'm not sure I understand.", "You are gay"])

        if user_message in option_responses:
            return jsonify({
                'response': option_responses[user_message],
                'new_options': []
            })

        if user_message in button_options:
            return jsonify({
                'response': f'You typed: {data["message"]}',
                'new_options': button_options.get(user_message, [])
            })

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
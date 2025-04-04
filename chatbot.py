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
        ["Goodbye!", "See you later", "Bye!"]
    ],
    [
        r"thank you",
        ["No need to thank me", "I'm trying to be more humble"]
    ],
    [
        r".*address.*|.*office.*|.*locat(e|ed).*|.*company.*",
        ["Our office is located at <a href='https://maps.app.goo.gl/ce1hsqtkCuzyuJak6' target='_blank' style='color: white'>49 Tannery Lane</a>."]
    ],
    [
        r".*phon(e|es|ed).*|.*numbe(r|rs).*|.*hotline.*|.*contac(t|ted|).*",
        ["Our office hotline is <a href='tel:+65 6323 1773' target='_blank' style='color:white'>+65-6323-1773</a>"]
    ],
    [
        r".*broadband.*|.*wifi.*|.*internet.*|.*network.*|.*lan.*|.*wireless.*|.*network.*",
        ["View Starhub's broadband plans <a href='https://www.starhub.com/personal/broadband.html#plans' target='_blank' style='color: white'>here</a>."]
    ],
    [
        r".*insiro.*",
        ["INSIRO is a world-class internet solutions provider with a specialized team of IT professionals. We are fully committed to deliver excellence in IT services. With a wide range of IT products, INSIRO is dedicated to provide the most comprehensive and customized solutions for our clients."]
    ]
    ]


chatbot = Chat(pairs, reflections)

button_options = {
    'menu': ['General Enquiries', 'About Us', 'Services', 'Promotions', 'Frequently Asked Questions', 'Join Us'],
    'main': ['General Enquiries', 'About Us', 'Services', 'Promotions', 'Frequently Asked Questions', 'Join Us'],
    'home': ['General Enquiries', 'About Us', 'Services', 'Promotions', 'Frequently Asked Questions', 'Join Us'],
    'main menu': ['General Enquiries', 'About Us', 'Services', 'Promotions', 'Frequently Asked Questions', 'Join Us'],
    'general enquiries': ['Contact Us', 'Address', 'Hours'],
    'about us': ['Awards and Recognitions', 'Data Usage'],
    'services': ['Promo Info', 'Eligibility', 'How to Claim'],
    'promotions': ['Current Promos', 'Past Promos', 'Future Promos'],
    'frequently asked questions': ['StarHub FAQ', 'Still require more help?'],
    'join us': ['Job Scope', 'Interested?']
}

main_responses = {
    'main menu': "<span style='font-size: 35px; font-weight: bold;'>Welcome to Insiro!</span> <br><br>"
                 "Hello! I'm the Insiro AI Assistant. What can I help you with today?",
    'menu': "<span style='font-size: 35px; font-weight: bold;'>Welcome to Insiro!</span> <br><br>"
            "Hello! I'm the Insiro AI Assistant. What can I help you with today?",
    'main': "<span style='font-size: 35px; font-weight: bold;'>Welcome to Insiro!</span> <br><br>"
            "Hello! I'm the Insiro AI Assistant. What can I help you with today?",
    'home': "<span style='font-size: 35px; font-weight: bold;'>Welcome to Insiro!</span> <br><br>"
            "Hello! I'm the Insiro AI Assistant. What can I help you with today?",
    'about us': "Incorporated in Singapore in the year 2000, INSIRO Pte Ltd has successfully developed many IT strategies for our clients by understanding the latest consumer"
                " trends and customizing our solutions to meet the specific needs of every customer.",
    'general enquiries': "How can we assist you today?",
    'services': "Here are the services we offer:",
    'promotions': "Check out our latest promotions below!",
    'frequently asked questions': "Here are some common questions we receive.",
    'join us': "Looking for a career with us? See the details below."
}

option_responses = {
    'contact us': 'Email us at <a href="mailto:cso.insiro.com" target="_blank">cso@insiro.com</a> \n'
                  'Contact us at <a href="tel:65 6323 1773" target="_current">+65-6323-1773</a> \n'
                  '<iframe></>',

    'address': 'Find us at <a href="https://maps.app.goo.gl/ce1hSqtKcUzyuJak6" target="_blank">49 Tannery Lane</a>' ,

    'hours': 'We are open from 9 AM to 6 PM',

    'awards and recognitions': '<img src="/static/masterpartner.jpg" alt="Xavier" style="max-width: 80%; border-radius: 5px"> \n <br>'
                       '<p>I’m INSIRO! But you can call me INSIROBOT. Do you have a name you prefer to go by? 😊</p>',

    'data usage': 'Use our StarHub app to view data usage <br><br>'
                  '<a href="https://play.google.com/store/apps/details?id=com.starhub.csselfhelp" alt="Google Play" target="_blank"><img src="/static/gplay.jpg" class="data-usage-image"></a> <br>'
                  '<a href="https://apps.apple.com/sg/app/starhub-app/id470460379" alt="Apple Store" target="_blank"><img src="/static/apple.jpg" class="data-usage-image"></a>',

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
        response_message = main_responses.get(button_value, "Here are the available options:")
        return jsonify({
            'response': response_message,
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
            response = random.choice(["Why did you redeem it!?"])


        if user_message in option_responses:
            return jsonify({
                'response': option_responses[user_message],
                'new_options': []
            })

        if user_message in button_options:
            response_message = main_responses.get(user_message, user_message)
            return jsonify({
                'response': response_message,
                'new_options': button_options.get(user_message, [])
            })

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
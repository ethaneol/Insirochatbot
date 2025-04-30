from flask import Flask, request, jsonify, render_template, send_from_directory, session
from nltk.chat.util import Chat, reflections
import random
from flask_cors import CORS
import bleach
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app) #black balls programs

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

logging.basicConfig(
    filename ='/tmp/logging.txt',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

error_log = logging.getLogger('error_logger')
error_log.setLevel(logging.ERROR)
error_handler = logging.FileHandler('/tmp/error_logging.txt')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
error_handler.setFormatter(error_formatter)
error_log.addHandler(error_handler)

def return_real_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

app.config['SECRET_KEY'] = 'my7nX9evuRn9mgjatSreb1Ts4htlT1O1is1nz0U+gFU='
app.config.update(
    SESSION_COOKIE_HTTPONLY = True,
    SESSION_COOKIE_SECURE = True,
    SESSION_COOKIE_SAMESITE = 'Lax'
)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

pairs = [
    [
        r".*issu(e|es).*|.*proble(m|ms).*|.*troubleshoo(t|ting|ts).*|.*troubl(e|es).*",
        ["Please contact us at <a href='tel:6563231773'>6323 1773</a> for any problems encountered."]
    ],
    [
        r"hi|hello|hey",
        ["Hello!", "Hi!", "Hey!"]
    ],
    [
        r".*name.*",
        ["I'm a chatbot.", "You can call me InsiroBot."]
    ],
    [
        r"bye|goodbye|see you",
        ["Goodbye!", "See you later", "Bye!"]
    ],
    [
        r".*than(k|ks).*",
        ["No need to thank me", "I'm trying to be more humble", "No worries!", "Welcome!"]
    ],
    [
        r".*address.*|.*office.*|.*locat(e|ed|ion).*|.*company.*",
        ["Our office is located at <a href='maps.google.com/05' target='_blank' style='color: white'>49 Tannery Lane</a>"]
    ],
    [
        r".*phon(e|es|ed).*|.*numbe(r|rs).*|.*hotline.*|.*contac(t|ted|).*",
        ["Our office hotline is <a href='tel:65 6323 1773' target='_blank'>63231773</a> \n"]
    ],
    [
        r".*broadband.*|.*wifi.*|.*internet.*|.*network.*|.*lan.*|.*wireless.*",
        ["View Starhub's broadband plans <a href='https://www.starhub.com/personal/broadband.html#plans' target='_blank' style='color: white'>here</a>."]
    ],
    [
        r".*insiro.*",
        ["INSIRO is a world-class internet solutions provider with a specialized team of IT professionals. We are fully committed to deliver excellence in IT services. With a wide range of IT products, INSIRO is dedicated to provide the most comprehensive and customized solutions for our clients."]
    ],
    [
        r".*starhub tv.*|.*homehub.*|.*epl.*|.*premier league.*|.*channe(l|ls).*|.*tv.*|.*bundl(e|es).*",
        ["Here are our <a href='https://www.starhub.com/personal/bundles/homehub-plus/ultraspeed.html' target='_blank'>Homehub TV bundles!</a>(EPL included)"],
    ],
    [
        r"",
        [""]
    ],
    ]


chatbot = Chat(pairs, reflections)

button_options = {
    'menu': ['General Enquiries', 'About Us', 'Services', 'Promotions', 'Frequently Asked Questions', 'Join Us'],
    'main': ['General Enquiries', 'About Us', 'Services', 'Promotions', 'Frequently Asked Questions', 'Join Us'],
    'home': ['General Enquiries', 'About Us', 'Services', 'Promotions', 'Frequently Asked Questions', 'Join Us'],
    'main menu': ['General Enquiries', 'About Us', 'Services', 'Promotions', 'Frequently Asked Questions', 'Join Us'],
    'general enquiries': ['Contact Us', 'Address', 'Hours'],
    'about us': ['Awards and Recognitions', 'Social media contact'],
    'services': ['Promo Info', 'Eligibility', 'How to Claim'],
    'promotions': ['Current Promos', 'Past Promos', 'Future Promos'],
    'frequently asked questions': ['StarHub FAQ', 'Still require more help?'],
    'join us': ['Job Scope', 'Interested?'],
    'we are hiring!': ['Part Time', 'Full Time', 'Interested?']
}

main_responses = {
    'main menu': "<span style='font-size: 35px; font-weight: bold;' class='main-message'>Welcome to Insiro!</span> <br><br>"
                 "Hello! I'm the Insiro AI Assistant. What can I help you with today?",
    'menu': "<span style='font-size: 35px; font-weight: bold;' class='main-message'>Welcome to Insiro!</span> <br><br>"
            "Hello! I'm the Insiro AI Assistant. What can I help you with today?",
    'main': "<span style='font-size: 35px; font-weight: bold;' class='main-message'>Welcome to Insiro!</span> <br><br>"
            "Hello! I'm the Insiro AI Assistant. What can I help you with today?",
    'home': "<span style='font-size: 35px; font-weight: bold;' class='main-message'>Welcome to Insiro!</span> <br><br>"
            "Hello! I'm the Insiro AI Assistant. What can I help you with today?",
    'about us': "Incorporated in Singapore in the year 2000, INSIRO Pte Ltd has successfully developed many IT strategies for our clients by understanding the latest consumer"
                " trends and customizing our solutions to meet the specific needs of every customer.",
    'general enquiries': "How can we assist you today?",
    'services': "Here are the services we offer:",
    'promotions': "Check out our latest promotions below!",
    'frequently asked questions': "Here are some common questions we receive.",
    'join us': "Looking for a career with us? See the details below.",
    'we are hiring!': "More details below!"
}

option_responses = {
    'contact us': 'Email us at <a href="mailto:cso.insiro.com" target="_blank">cso@insiro.com</a> <br> \n'
                  'Contact us at <a href="tel:65 63231773" target="_current">+65 63231773</a> <br><br> \n'
                  '<a href="https://www.instagram.com/insiropteltd/" target="_blank"><img src="/static/instagram.png" class="socmed-icon"></a>'
                  '<a href="https://wa.me/6583780991?text=I%20am%20interested%20in%20your%20broadband%20promotions" target="_blank"><img src="/static/whatsapp.png" class="socmed-icon"></a>'
                  '<a href="https://t.me/StarHubBTO" target="_blank"><img src="/static/telegram.png" class="socmed-icon"></a>'
                  '<a href="https://insiro.com" target="_blank"><img src="/static/internet.png" class="socmed-icon"></a>'
                  '<a href="https://linktr.ee/insiro" target="_blank"><img src="/static/link.png" class="socmed-icon"></a>'
    ,

    'address': 'Find us at <a href="https://maps.app.goo.gl/ce1hSqtKcUzyuJak6" target="_blank">49 Tannery Lane</a>' ,

    'hours': 'Our office is open from 9 to 6pm',

    'awards and recognitions': '<img src="/static/masterpartner.jpg" alt="Xavier" style="max-width: 80%; border-radius: 5px"> \n <br>'
                               '<p>'
                                   '• StarHub Top Performing Reseller for Year 2002 to Year 2009 <br><br>'
                                   '• StarHub Top Channel Partner for Year 2010 to Year 2012 <br><br>'
                                   '• StarHub Top Performing Platinum Partner for Year 2013 to Year 2017 <br><br>'
                                   '• StarHub Top Deal (Core Partner) for Year 2019 <br><br>'
                                   '• Starhub Top Deal (Core Partner) for Q4 of Year 2020 <br><br>'
                                   '• Starhub Top Deal (Core Partner) for Q1 to Q3 of Year 2021'
                               '</p>',

    'social media contact': 'View our social media profiles below!<br> <br>'
                '<a href="https://www.instagram.com/insiropteltd/" target="_blank"><img src="/static/instagram.png" class="socmed-icon"></a>'
                '<a href="https://wa.me/6583780991?text=I%20am%20interested%20in%20your%20broadband%20promotions" target="_blank"><img src="/static/whatsapp.png" class="socmed-icon"></a>'
                '<a href="https://t.me/StarHubBTO" target="_blank"><img src="/static/telegram.png" class="socmed-icon"></a>'
                '<a href="https://insiro.com" target="_blank"><img src="/static/internet.png" class="socmed-icon"></a>'
                '<a href="https://linktr.ee/insiro" target="_blank"><img src="/static/link.png" class="socmed-icon"></a>',


    'promo info': 'View <a href="https://www.starhub.com/personal/broadband.html/#plans" target="_blank">Broadband</a> or <a href="https://www.starhub.com/personal/bundles/homehub-plus/ultraspeed.html" target="_blank">HomeHub</a>',

    'eligibility': 'View <a href="https://www.starhub.com/personal/support/article.html?id=uaIp0zAzAo8LInqU2PmWHA" target="_blank">Eligibility</a>',

    'how to claim': 'Type contact to claim!',

    'current promos': 'View our current promos <a href="https://www.starhub.com/personal/broadband.html/#plans" target="_blank">Here!</a>',

    'past promos': 'View our past promos <a href="https://www.starhub.com/personal/broadband.html" target="_blank">Here!</a>',

    'future promos': 'View our future promos <a href="https://www.starhub.com/personal/broadband.html" target="_blank">Here!</a>',

    'starhub faq': 'Our <a href="https://www.starhub.com/personal/support.html" target="_blank">FAQ</a>',

    'still require more help?': 'Contact us at <br>'
                                ' <a href="tel:65 6323 1773" target="_current">+65-6323-1773</a>',

    'job scope': 'Any cheerful and self motivated individual will do!',

    'interested?': 'Drop your CV at <br>'
                   '<a href="mailto:normila@insiro.com" target="_blank">normila@insiro.com</a>',

    'full time': '<img src="static/join.jpg" style="max-width: 90%;">',

    'part time': 'We are currently hiring part timers to aid us in manning roadshows! <br><br>'
                 'Flexible working hours and choice of pay! <br><br>'
                 'Up to <span style="font-weight: bold">$16/h</span>!!!',
}

@app.after_request
def apply_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src: 'self';"
        "script-src: 'self' https://www.google.com https://www.gstatic.com 'unsafe-inline';"
        "style-src 'self' https://fonts.googleapis.com 'unsafe-inline';"
        "img-src: 'self' data:;"
        "font-src 'self' https://fonts.gstatic.com;;"
        "connect-src: 'self';"
        "frame-src: https://www.google.com https://www.gstatic.com;"
        "object-src: 'none'"
    )
    return response

def secure_headers(response):
    response.headers['X-Frame Options'] = 'DENY'
    response.headers['X-Content Options'] = 'nosniff'
    return response

@app.route('/')
def index():
    csrf_token = generate_csrf()
    return render_template('index.html', option_responses=option_responses)

@app.route('/button_action', methods=['POST'])
def button_action():
    csrf.protect()
    data = request.get_json()
    button_value = data['button_value'].lower()

    logging.info(f"[Button Click] - User Selected: {button_value}")

    # Sanitize button_value (though it's likely already safe, being a button value)
    allowed_tags = ['span', 'a', 'br', 'img', 'p']
    allowed_attributes = {
        'span': ['style', 'class'],
        'a': ['href', 'target', 'style'],
        'img': ['src', 'alt', 'style', 'class'],
        'p': ['style', 'class']
    }
    safe_button_value = bleach.clean(button_value, tags=allowed_tags, attributes=allowed_attributes)

    if safe_button_value in option_responses:
        response = option_responses[safe_button_value]
        safe_response = bleach.clean(response)  # sanitize response
        return jsonify({
            'response': safe_response,
            'new_options': []
        })

    if safe_button_value in button_options:
        response_message = main_responses.get(safe_button_value, "Here are the available options:")
        safe_response_message = bleach.clean(response_message)  # sanitize response
        new_options = button_options.get(safe_button_value, [])
        safe_new_options = [bleach.clean(option) for option in new_options]  # sanitize each new option
        return jsonify({
            'response': safe_response_message,
            'new_options': safe_new_options
        })
    else:
        safe_unknown_response = bleach.clean('Unknown button action.')  # sanitize unknown response.
        return jsonify({'response': safe_unknown_response, 'new_options': []})


@app.route('/chat', methods=['POST'])
@limiter.limit("5 per second")
def chat():
    csrf.protect()
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid JSON or missing "message" field'}), 400

        user_message = data['message'].lower()
        logging.info(f"[Chat Input] - User typed: {user_message}")

        # Sanitize user_message
        allowed_tags = ['span', 'a', 'br', 'img', 'p']
        allowed_attributes = {
            'span': ['style', 'class'],
            'a': ['href', 'target', 'style'],
            'img': ['src', 'alt', 'style', 'class'],
            'p': ['style', 'class']
        }
        safe_user_message = bleach.clean(user_message, tags=allowed_tags, attributes=allowed_attributes)

        response = chatbot.respond(data['message'])
        if not response:
            response = random.choice(["Sorry, I didn't quite get that", "Could you rephrase that?"])
        safe_response = bleach.clean(response)
        logging.info(f"[Chatbot Response] - Replied: {response}")

        if safe_user_message in option_responses:
            return jsonify({
                'response': option_responses[safe_user_message],
                'new_options': []
            })

        if safe_user_message in button_options:
            return jsonify({
                'response': main_responses.get(safe_user_message, safe_user_message),
                'new_options': button_options.get(safe_user_message, [])
            })

        return jsonify({'response': safe_response})

    except Exception as e:
        safe_error = bleach.clean(str(e))  # sanitize error message.
        return jsonify({'error': safe_error}), 500


if __name__ == '__main__':
    app.run(debug=True)
from datetime import datetime
import requests
import json
import re
import time
import argparse
import schedule
import random

#dictionaries and variables
chat_id = "-1001154551109"

zodiac_sign_dict = {'Aries': '1',
                    'Taurus': '2',
                    'Gemini': '3',
                    'Cancer': '4',
                    'Leo': '5',
                    'Virgo': '6',
                    'Libra': '7',
                    'Scorpio': '8',
                    'Sagittarius': '9',
                    'Capricorn': '10',
                    'Aquarius': '11',
                    'Pisces': '12'}

zodiac_unic_dict = {'Aries': '\u2648\ufe0f',
                    'Taurus': '\u2649\ufe0f',
                    'Gemini': '\u264a\ufe0f',
                    'Cancer': '\u264b\ufe0f',
                    'Leo': '\u264c\ufe0f',
                    'Virgo': '\u264d\ufe0f',
                    'Libra': '\u264e\ufe0f',
                    'Scorpio': '\u264f\ufe0f',
                    'Sagittarius': '\u2650\ufe0f',
                    'Capricorn': '\u2651\ufe0f',
                    'Aquarius': '\u2652\ufe0f',
                    'Pisces': '\u2653\ufe0f'}

months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

saved_data = {}
log_path = './logs.txt'

# functions

def get_unicode_zodiac(sign):
    unicode = zodiac_unic_dict[sign]
    return unicode

def admin_notification(msg, bot_token, chat_id):
    try:
        requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}')
    except Exception as e:
        with open(log_path,'a') as log_file:
            log_file.write(f'Error while sending admin notification {e}\n')
            log_file.close()
        

def send_msg(msg, bot_token, chat_id):
    try:
        send = requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}')
    except Exception as e:
        with open(log_path,'a') as log_file:
            log_file.write(f'Error while sending message - {e}\n')
            log_file.close()
    if send:
        return send

def send_animation(msg, bot_token, chat_id):
    try:
        send = requests.get(f'https://api.telegram.org/bot{bot_token}/sendAnimation?chat_id={chat_id}&animation={msg}')
    except Exception as e:
        with open(log_path,'a') as log_file:
            log_file.write(f'Error while sending animation - {e}\n')
            log_file.close()
    if send:
        return send

def find_star_sign(day, month):
    day = int(day)
    if month == 'Dec':
        astro_sign = 'Sagittarius' if (day < 22) else 'Capricorn'
    elif month == 'Jan':
        astro_sign = 'Capricorn' if (day < 21) else 'Aquarius'
    elif month == 'Feb':
        astro_sign = 'Aquarius' if (day < 21) else 'Pisces'
    elif month == 'Mar':
        astro_sign = 'Pisces' if (day < 21) else 'Aries'
    elif month == 'Apr':
        astro_sign = 'Aries' if (day < 21) else 'Taurus'
    elif month == 'May':
        astro_sign = 'Taurus' if (day < 21) else 'Gemini'
    elif month == 'Jun':
        astro_sign = 'Gemini' if (day < 22) else 'Cancer'
    elif month == 'Jul':
        astro_sign = 'Cancer' if (day < 23) else 'Leo'
    elif month == 'Aug':
        astro_sign = 'Leo' if (day < 24) else 'Virgo'
    elif month == 'Sep':
        astro_sign = 'Virgo' if (day < 23) else 'Libra'
    elif month == 'Oct':
        astro_sign = 'Libra' if (day < 24) else 'Scorpio'
    elif month == 'Nov':
        astro_sign = 'Scorpio' if (day < 22) else 'Sagittarius'
    return astro_sign

def print_horoscope(day, month):
    astro_sign = find_star_sign(day, month)
    zodiac_int = zodiac_sign_dict[astro_sign]
    try:
        header_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36 OPR/63.3.3216.58675",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"]
        header = {'user-agent': random.choice(header_list)}
        horo_url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={zodiac_int}" 
        horoscope = requests.get(horo_url, headers = header).text  
        date_now = datetime.today().strftime("%b %-d, %Y")
        if date_now in horoscope:
            start = f'<p><strong>{date_now}</strong> - '
            end = '</p>'
            print_horoscope = (horoscope.split(start))[1].split(end)[0]
            return print_horoscope
        else:
            try:
                horoscope = requests.get(f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-tomorrow.aspx?sign={zodiac_int}").text
                start = f'<p><strong>{date_now}</strong> - '
                end = '</p>'
                print_horoscope = (horoscope.split(start))[1].split(end)[0]
                return print_horoscope
            except Exception as e:
                send_msg(e, args.token, chat_id)
    except Exception as e:
        send_msg(e, args.token, chat_id)

def save_to_file(data):
    file = './horoscopes.json' 
    with open(file, 'w') as f: 
        json.dump(data, f)

def read_from_file():
    file = './horoscopes.json' 
    with open(file, 'r') as f:
        data_opened = json.load(f)
    return data_opened

def update_help(username, text, private_chat_id):
    message = ("Welcome to the Daily Horoscope Bot!"
    "\n\n/subscribe - to sign up to a daily horoscope\n"
    "/horoscope - to get an instant horoscope for today.\n" 
    "/unsubscribe - to unsubscribe if you do not want to receive daily horoscopes any longer.")
    response = send_msg(message, args.token, private_chat_id)
    admin_notification(f'{username} {text} {str(response)}', args.token, chat_id)

def update_unsubscribe(u, private_chat_id):
    username = u['message']['from']['username']
    from_id = u['message']['from']['id']
    first_name = u['message']['from']['first_name']
    if data_dict.get(username, 0):
        if data_dict[username]['subscribed'] == 'true':
            data_dict[username] = {
                'birthday': data_dict[username]['birthday'],
                'from_id': from_id,
                'first_name': first_name,
                'subscribed': 'false' }
            message = ("You have been unsubscribed :( feel free to resubscribe using /subscribe, "
            "indicating your day and month of birth")
            save_to_file(data_dict)
        else:
            message = 'You have already unsubscribed! Feel free to subscribe again using "/subscribe"'
    else:
        message = "You have not subscribed yet! Please use /subscribe, indicating your day and month of birth"
    response = send_msg(message, args.token, private_chat_id)
    admin_notification(f'{username} unsub {str(response)}', args.token, chat_id)

def process_updates(updates):
    for u in updates:
        if 'message' in u.keys():
            if not u['message'].get('text',0):
                continue
            text = u['message']['text']
            private_chat_id = u['message']['from']['id']
            first_name = u['message']['from']['first_name']
            if u['message']['from'].get('username',0):
                username = u['message']['from']['username']
            else:
                username = first_name
            if 'entities' in u['message'].keys():
                if text == "/help" or text == "/start" or text == "/help@HoroscopeDaily_bot" or text == "/start@HoroscopeDaily_bot":
                    update_help(username, text, private_chat_id)
                elif text.startswith("/horoscope") or text.startswith("/subscribe"):
                    saved_data[username] = {
                        'text':text,
                        'private_chat_id':private_chat_id,
                        'month':'',
                        'day':''
                        }
                    keyboard_m(private_chat_id, args.token)
                elif re.match('^\/unsubscribe', text):
                    update_unsubscribe(u, private_chat_id)
            elif text in months:
                if username in saved_data.keys():
                    saved_data[username]['month'] = text
                    month = saved_data[username]['month']
                    keyboard_d(private_chat_id, args.token, month)
            elif re.match('^\d{1,2}$',text) and (username in saved_data.keys()): 
                if int(text) in range(1,32) and saved_data[username]['month'] != '':
                    saved_data[username]['day'] = int(text)
                    day = saved_data[username]['day']
                    month = saved_data[username]['month']
                    birthday = "{} {}".format(month, day)
                    date = datetime.today().strftime("%b %d")
                    zodiac = find_star_sign(day, month)
                    unicode = get_unicode_zodiac(zodiac)
                    horoscope = print_horoscope(day, month)
                    if saved_data[username]['text'] == '/horoscope':
                        if date == birthday:
                            message = f"Happy Birthday {first_name}! Here is your horoscope on this amazing Happy day: \n \n{unicode} {horoscope}"
                            bday_file_id = "CgACAgQAAxkBAAN0YKrAErHbObMeIAO6sXI40VTJU9MAAisCAALHmZVS208xEjswK4gfBA"
                            response_animation = send_animation(bday_file_id, args.token, private_chat_id)
                            admin_notification(response_animation, args.token, chat_id)
                            response = send_msg(message, args.token, private_chat_id)
                            admin_notification(f'{username} {text} {response}', args.token, chat_id)
                        else:
                            horoscope = print_horoscope(day, month)
                            unicode = get_unicode_zodiac(find_star_sign(day, month))
                            first_name = u['message']['from']['first_name']
                            message = f"Dear {first_name}, today's horoscope for {unicode} is: \n \n{horoscope}"
                            response = send_msg(message, args.token, private_chat_id)
                            admin_notification(f'{username} {text} {response}', args.token, chat_id)
                    else:
                        data_dict[username] = {
                            'birthday': birthday,
                            'from_id': private_chat_id,
                            'first_name': first_name,
                            'subscribed': 'true' }
                        if date == birthday:
                            message = (f"Happy Birthday {first_name}! You have been subscribed to our Daily Horoscope! "
                            "To unsubscribe, please use /unsubscribe to silence our bot (don't do that please)")
                            save_to_file(data_dict)
                            response = send_msg(message, args.token, private_chat_id)
                            admin_notification(f'{username} {text} {response}', args.token, chat_id)
                            bday_file_id = "CgACAgQAAxkBAAN0YKrAErHbObMeIAO6sXI40VTJU9MAAisCAALHmZVS208xEjswK4gfBA"
                            response_animation = send_animation(bday_file_id, args.token, private_chat_id)
                            admin_notification(response_animation, args.token, chat_id)
                        else:
                            unicode = get_unicode_zodiac(find_star_sign(day, month))
                            message = (f"{first_name}, you have been subscribed to our Daily Horoscope for {unicode}! "
                            "To unsubscribe, please use /unsubscribe to silence our bot (don't do that please)")
                            save_to_file(data_dict)
                            response = send_msg(message, args.token, private_chat_id) 
                            admin_notification(f'subscriber! {username} {text} {response}', args.token, chat_id)
        elif 'channel_post' in u.keys() and 'animation' not in u['channel_post'].keys():
            pass
        else:
            pass

def scheduled_task(data_dict):
    if len(data_dict.keys()) == 0:
        data_dict = read_from_file()
    else:
        data_dict = data_dict
    for user in data_dict:
        if data_dict[user]['subscribed'] == 'true':
            private_chat_id = data_dict[user]['from_id']
            birthday = data_dict[user]['birthday']
            first_name = data_dict[user]['first_name']
            date = datetime.today().strftime("%b %d")
            month = birthday.split(' ')[0]
            day = birthday.split(' ')[1]
            zodiac = find_star_sign(day, month)
            unicode = get_unicode_zodiac(zodiac)
            horoscope = print_horoscope(day, month)
            if date == birthday:
                message = f"Happy Birthday {first_name}! Here is your horoscope on this amazing Happy day: \n \n{unicode} {horoscope}"
                bday_file_id = "CgACAgQAAxkBAAN0YKrAErHbObMeIAO6sXI40VTJU9MAAisCAALHmZVS208xEjswK4gfBA"
                response_animation = send_animation(bday_file_id, args.token, private_chat_id)
                admin_notification(f'daily bday {first_name}, resp {response_animation}', args.token, chat_id)
            else:
                message = f"Hello {first_name}, this is your daily horoscope! \n \n{unicode} {horoscope}"
            response = send_msg(message, args.token, private_chat_id)
            admin_notification(f'daily sent to {first_name}, response: {response}', args.token, chat_id)
        else:
            continue

def parse_args():
    """
    Parses arguments from command line
    :return: Namespace of parsed params
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', dest='token', required=True, type=str)
    return parser.parse_args()

def build_day_keyboard(month):
    keyboard = []
    sub_keyboard = []
    if month in ['Jan', 'Mar', 'May', 'Jul', 'Aug', 'Oct', 'Dec']:
        for i in range(1,32):
            if len(sub_keyboard) == 7:
                keyboard.append(sub_keyboard)
                sub_keyboard = []
            elif i == 31:
                keyboard.append(sub_keyboard)
            sub_keyboard.append(str(i))
    elif month == 'Feb':
        for i in range(1,30):
            if len(sub_keyboard) == 5:
                keyboard.append(sub_keyboard)
                sub_keyboard = []
            elif i == 29:
                keyboard.append(sub_keyboard)
            sub_keyboard.append(str(i))
    else:
        for i in range(1,31):
            if len(sub_keyboard) == 7:
                keyboard.append(sub_keyboard)
                sub_keyboard = []
            elif i == 30:
                keyboard.append(sub_keyboard)
            sub_keyboard.append(str(i))
    return keyboard

def keyboard_m(chat_id, bot_token):
    reply_markup={"keyboard":[
                                ["Jan", "Feb","Mar"],
                                ["Apr", "May", "Jun"],
                                ["Jul", "Aug", "Sep"],
                                ["Oct", "Nov", "Dec"]    
                                ],
                "resize_keyboard":True,
                "one_time_keyboard":True}
    reply_markup_json = json.dumps(reply_markup)
    text = "Please select your month of birth"
    send = requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}&reply_markup={reply_markup_json}')

def keyboard_d(chat_id, bot_token, month):
    keyboard = build_day_keyboard(month)
    reply_markup={"keyboard":keyboard,
            "resize_keyboard":True,
            "one_time_keyboard":True}
    reply_markup_json = json.dumps(reply_markup)
    text = "Please select your day of birth"
    send = requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}&reply_markup={reply_markup_json}')

# main code

args = parse_args()
    
try:
    json_initial_updates = requests.get('https://api.telegram.org/bot' + args.token + '/getUpdates').text
except Exception as e:
    admin_notification(e, args.token, chat_id)

if not json_initial_updates:
    exit

initial_updates_raw = json.loads(json_initial_updates)
initial_updates = initial_updates_raw['result']
data_dict = read_from_file()
process_updates(initial_updates)

if len(initial_updates) == 0:
    last_processed_update_id = 0
else:
    last_processed_update_id = initial_updates_raw['result'][-1]['update_id']

schedule.every().day.at("02:00").do(scheduled_task, data_dict)

while True:
    time.sleep(1)
    schedule.run_pending()
    newest_update = last_processed_update_id + 1
    try:
        last_json = requests.get(f'https://api.telegram.org/bot{args.token}/getUpdates?offset={newest_update}').text
    except Exception as e:
        send_msg(e, args.token, chat_id)
    if not last_json:
        break
    last = json.loads(last_json)
    if last.get('result', 0):
        updates = last['result']
        last_processed_update_id = last['result'][-1]['update_id']
        process_updates(updates)
    else:
        continue

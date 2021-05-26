from datetime import datetime
import requests
import json
import re
import time
import argparse
import schedule

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

month_dict = { '1': 'January',
               '2': 'February',
               '3': 'March',
               '4': 'April',
               '5': 'May',
               '6': 'June',
               '7': 'July',
               '8': 'August',
               '9': 'September',
               '10': 'October',
               '11': 'November',
               '12': 'December' }

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

# functions

def get_unicode_zodiac(sign):
    unicode = zodiac_unic_dict[sign]
    return unicode

def admin_notification(msg, bot_token, chat_id):
    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}')

def send_msg(msg, bot_token, chat_id):
    send = requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}')
    return send

def send_animation(msg, bot_token, chat_id):
    send = requests.get(f'https://api.telegram.org/bot{bot_token}/sendAnimation?chat_id={chat_id}&animation={msg}')
    return send

def find_star_sign(day, month):
    if month == 'december':
        astro_sign = 'Sagittarius' if (day < 22) else 'Capricorn'
    elif month == 'january':
        astro_sign = 'Capricorn' if (day < 20) else 'Aquarius'
    elif month == 'february':
        astro_sign = 'Aquarius' if (day < 19) else 'Pisces'
    elif month == 'march':
        astro_sign = 'Pisces' if (day < 21) else 'Aries'
    elif month == 'april':
        astro_sign = 'Aries' if (day < 20) else 'Taurus'
    elif month == 'may':
        astro_sign = 'Taurus' if (day < 21) else 'Gemini'
    elif month == 'june':
        astro_sign = 'Gemini' if (day < 21) else 'Cancer'
    elif month == 'july':
        astro_sign = 'Cancer' if (day < 23) else 'Leo'
    elif month == 'august':
        astro_sign = 'Leo' if (day < 23) else 'Virgo'
    elif month == 'september':
        astro_sign = 'Virgo' if (day < 23) else 'Libra'
    elif month == 'october':
        astro_sign = 'Libra' if (day < 23) else 'Scorpio'
    elif month == 'november':
        astro_sign = 'Scorpio' if (day < 22) else 'Sagittarius'
    return astro_sign

def parse_month(input):
    input = (month_dict[input]).lower()
    return input
    
def print_horoscope(day, month):
    astro_sign = find_star_sign(day, month)
    zodiac_int = zodiac_sign_dict[astro_sign]
    try:
        horoscope = requests.get(f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={zodiac_int}").text
        date_now = datetime.today().strftime("%B %d, %Y")
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

def validate_date(day, month):
    if day == '' or month == '':
        return 'Invalid'
    else:
        if int(month) < 1 or int(month) > 13:
            return 'Invalid'   
        else:
            if int(month) in [2]:
                if int(day) < 1 or int(day) > 29:
                    return 'Invalid'
                else:
                    return 'Valid'
            elif int(month) in [1,3,5,7,8,10,12]:
                if int(day) < 1 or int(day) > 31:
                    return 'Invalid'
                else:
                    return 'Valid'
            else:
                if int(day) < 1 or int(day) > 30:
                    return 'Invalid'
                else:
                    return 'Valid'

def process_updates(updates):
    for u in updates:
        if 'message' in u.keys():
            private_chat_id = u['message']['from']['id']
            if 'entities' in u['message'].keys():
                text = u['message']['text']
                if text == "/help" or text == "/start" or text == "/help@HoroscopeDaily_bot" or text == "/start@HoroscopeDaily_bot":
                    message = ("Welcome to the Daily Horoscope Bot!"
                    "\n\n/subscribe dd.mm - to sign up to a daily horoscope, where dd is the day of birth, and mm is the month.\n"
                    "/horoscope dd.mm - where dd is the day and mm the month of your birth, to get an instant horoscope for today.\n" 
                    "/unsubscribe - to unsubscribe if you do not want to receive daily horoscopes any longer.")
                    response = send_msg(message, args.token, private_chat_id)
                    username = u['message']['from']['username']
                    admin_notification(f'{username} help {str(response)}', args.token, chat_id)
                    animation = 'CgACAgIAAxkBAAMqYKpmzsBRcCJBEyuQOpVzv0ip6MAAAjIPAAJqMlhJpySq1pojPO8fBA'
                    response_animation = send_animation(animation, args.token, private_chat_id)
                    admin_notification(response_animation, args.token, chat_id)
                elif text.startswith("/horoscope"):
                    if re.match('^\/horoscope \d{1,2}.\d{1,2}$', text):
                        splitted = text.split('.')
                        stripped_m = splitted[1].lstrip('0')
                        stripped_d = splitted[0].split(' ')[1].lstrip('0')
                        if validate_date(stripped_d,stripped_m) == 'Invalid':
                            message = 'Invalid date!'
                        else:
                            day = int(stripped_d)
                            month = parse_month(stripped_m)
                            horoscope = print_horoscope(day, month)
                            unicode = get_unicode_zodiac(find_star_sign(day, month))
                            first_name = u['message']['from']['first_name']
                            message = f"Dear {first_name}, today's horoscope for {unicode} is: \n \n{horoscope}"
                        username = u['message']['from']['username']
                        response = send_msg(message, args.token, private_chat_id)
                        admin_notification(f'{username} horoscope {str(response)}', args.token, chat_id)
                elif text == "/unsubscribe" or text == "/unsubscribe@HoroscopeDaily_bot":
                    if re.match('^\/unsubscribe', text):
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
                                message = ("You have been unsubscribed :( feel free to resubscribe using /subscribe dd.mm, "
                                "indicating your day and month of birth")
                                save_to_file(data_dict)
                            else:
                                message = 'You have already unsubscribed! Feel free to subscribe again using "/subscribe dd.mm"'
                        else:
                            message = "You have not subscribed yet! Please use /subscribe dd.mm, indicating your day and month of birth"
                        response = send_msg(message, args.token, private_chat_id)
                        admin_notification(f'{username} unsub {str(response)}', args.token, chat_id)
                elif text.startswith("/subscribe"):
                    if re.match('^\/subscribe \d{1,2}.\d{1,2}$', text):
                        splitted = text.split('.')
                        stripped_m = splitted[1].lstrip('0')
                        stripped_d = splitted[0].split(' ')[1].lstrip('0')
                        if validate_date(stripped_d,stripped_m) == 'Invalid':
                            message = 'Invalid date!'
                            response = send_msg(message, args.token, private_chat_id)
                            admin_notification(response, args.token, chat_id)
                        else:
                            day = int(stripped_d)
                            month = parse_month(stripped_m)
                            birthday = stripped_d + '.' + stripped_m
                            username = u['message']['from']['username']
                            from_id = u['message']['from']['id']
                            first_name = u['message']['from']['first_name']
                            data_dict[username] = {
                                'birthday': birthday,
                                'from_id': from_id,
                                'first_name': first_name,
                                'subscribed': 'true' }
                            date_short = datetime.now().strftime("%d.%m")
                            date_splitted = date_short.split('.')
                            stripped_m = date_splitted[1].lstrip('0')
                            stripped_d = date_splitted[0].lstrip('0')
                            date_stripped_splitted = stripped_d + '.' + stripped_m
                            if date_stripped_splitted == birthday:
                                message = (f"Happy Birthday {first_name}! You have been subscribed to our Daily Horoscope! "
                                "To unsubscribe, please use /unsubscribe to silence our bot (don't do that please)")
                                save_to_file(data_dict)
                                response = send_msg(message, args.token, private_chat_id)
                                admin_notification(response, args.token, chat_id)
                                bday_file_id = "CgACAgQAAxkBAAN0YKrAErHbObMeIAO6sXI40VTJU9MAAisCAALHmZVS208xEjswK4gfBA"
                                response_animation = send_animation(bday_file_id, args.token, private_chat_id)
                                admin_notification(response_animation, args.token, chat_id)
                            else:
                                unicode = get_unicode_zodiac(find_star_sign(day, month))
                                message = (f"{first_name}, you have been subscribed to our Daily Horoscope for {unicode}! "
                                "To unsubscribe, please use /unsubscribe to silence our bot (don't do that please)")
                                save_to_file(data_dict)
                                response = send_msg(message, args.token, private_chat_id) 
                                admin_notification(response, args.token, chat_id)
        elif 'channel_post' in u.keys() and 'animation' not in u['channel_post'].keys():
            text = u['channel_post']['text']
            message = f'Somebody wrote: {text}'
            send_msg(message, args.token, chat_id)
        else:
            continue

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
            birthday_splitted = birthday.split('.')
            date_short = datetime.now().strftime("%d.%m")
            date_splitted = date_short.split('.')
            stripped_m = date_splitted[1].lstrip('0')
            stripped_d = date_splitted[0].lstrip('0')
            date_stripped_splitted = stripped_d + '.' + stripped_m
            zodiac = find_star_sign(int(birthday_splitted[0]), parse_month(birthday_splitted[1]))
            unicode = get_unicode_zodiac(zodiac)
            horoscope = print_horoscope(int(birthday_splitted[0]), parse_month(birthday_splitted[1]))
            if date_stripped_splitted == birthday:
                message = f"Happy Birthday {first_name}! Here is your horoscope on this amazing Happy day: \n \n{unicode} {horoscope}"
                bday_file_id = "CgACAgQAAxkBAAN0YKrAErHbObMeIAO6sXI40VTJU9MAAisCAALHmZVS208xEjswK4gfBA"
                response_animation = send_animation(bday_file_id, args.token, private_chat_id)
                admin_notification(response_animation, args.token, chat_id)
            else:
                message = f"Hello {first_name}, this is your daily horoscope! \n \n{unicode} {horoscope}"
            response = send_msg(message, args.token, private_chat_id)
            admin_notification(response, args.token, chat_id)
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

schedule.every().day.at("11:00").do(scheduled_task, data_dict)

while True:
    time.sleep(2)
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
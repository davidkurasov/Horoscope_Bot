from datetime import datetime
import requests
import json
import re
import time

import argparse

def parse_args():
    """
    Parses arguments from command line
    :return: Namespace of parsed params
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', dest='token', required=True, type=str)
    return parser.parse_args()
args = parse_args()
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

def send_msg(msg, bot_token, chat_id):
    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}')

def send_animation(msg, bot_token, chat_id):
    requests.get(f'https://api.telegram.org/bot{bot_token}/sendAnimation?chat_id={chat_id}&animation={msg}')

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
    horoscope = requests.get(f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={zodiac_int}").text
    date_now = datetime.today().strftime("%B %d, %Y")
    if date_now in horoscope:
        start = f'<p><strong>{date_now}</strong> - '
        end = '</p>'
        print_horoscope = (horoscope.split(start))[1].split(end)[0]
        return print_horoscope
    else:
        horoscope = requests.get(f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-tomorrow.aspx?sign={zodiac_int}").text
        start = f'<p><strong>{date_now}</strong> - '
        end = '</p>'
        print_horoscope = (horoscope.split(start))[1].split(end)[0]
        return print_horoscope

def save_to_file(data):
    file = './horoscopes.json' 
    with open(file, 'w') as f: 
        json.dump(data, f)

def read_from_file():
    file = './horoscopes.json' 
    with open(file, 'r') as f:
        data_opened = json.load(f)
    return data_opened

def process_updates(updates):
    for u in updates:
        if 'message' in u.keys():
            private_chat_id = u['message']['chat']['id']
            print(private_chat_id)
            if 'entities' in u['message'].keys():
                text = u['message']['text']
                if text == "/help":
                    message = "This is the help for DaVit Bot! You can sign up to a daily horoscope by sending '/subscribe dd.mm' or unsubscribe by sending /unsubscribe, or type /horoscope dd.mm to get your horoscope for today"
                    send_msg(message, args.token, private_chat_id)
                elif text.startswith("/horoscope"):
                    if re.match('^\/horoscope \d{1,2}.\d{1,2}$', text):
                        splitted = text.split('.')
                        stripped_m = splitted[1].lstrip('0')
                        stripped_d = splitted[0].split(' ')[1].lstrip('0')
                        if int(stripped_d) > 31 or int(stripped_m) > 12:
                            message = 'Invalid!'
                        else:
                            day = int(stripped_d)
                            month = parse_month(stripped_m)
                            horoscope = print_horoscope(day, month)
                            message = horoscope
                        send_msg(message, args.token, private_chat_id)
                elif text == "/unsubscribe":
                    if re.match('^\/unsubscribe', text):
                        username = u['message']['from']['username']
                        from_id = u['message']['from']['id']
                        first_name = u['message']['from']['first_name']
                        if data_dict.get(username, 0):
                            data_dict[username] = {
                                'birthday': data_dict[username]['birthday'],
                                'from_id': from_id,
                                'first_name': first_name,
                                'subscribed': 'false' }
                            message = "You have been unsubscribed :( feel free to resubscribe using /subscribe dd.mm, indicating your day and month of birth"
                            save_to_file(data_dict)
                        else:
                            message = "You have not subscribed yet! Please use /subscribe dd.mm, indicating your day and month of birth"
                        send_msg(message, args.token, private_chat_id)
                elif text.startswith("/subscribe"):
                    if re.match('^\/subscribe \d{1,2}.\d{1,2}$', text):
                        splitted = text.split('.')
                        stripped_m = splitted[1].lstrip('0')
                        stripped_d = splitted[0].split(' ')[1].lstrip('0')
                        if int(stripped_d) > 31 or int(stripped_m) > 12:
                            message = 'Invalid!'
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
                                message = f"Happy Birthday {first_name}! You have been subscribed to our Daily Horoscope! To unsubscribe, please use /unsubscribe to silence our bot (don't do that please)"
                                save_to_file(data_dict)
                                send_msg(message, args.token, private_chat_id)
                                bday_file_id = "CgACAgQAAxkBAAIBoGCmooTfaBZ04NtWdCFtgjeSOoAHAAIrAgACx5mVUmYStZD4uE5-HwQ"
                                print(bday_file_id, args.token, private_chat_id)
                                send_animation(bday_file_id, args.token, private_chat_id)
                            else:
                                message = f"{first_name}, you have been subscribed to our Daily Horoscope! To unsubscribe, please use /unsubscribe to silence our bot (don't do that please)"
                                save_to_file(data_dict)
                                send_msg(message, args.token, private_chat_id) 
        elif 'channel_post' in u.keys() and 'animation' not in u['channel_post'].keys():
            text = u['channel_post']['text']
            message = f'Somebody wrote: {text}'
            send_msg(message, args.token, chat_id)
        else:
            continue
    
json_initial_updates = requests.get('https://api.telegram.org/bot' + args.token + '/getUpdates').text
initial_updates_raw = json.loads(json_initial_updates)

initial_updates = initial_updates_raw['result']

data_dict = read_from_file()

process_updates(initial_updates)

if len(initial_updates) == 0:
    last_processed_update_id = 0
else:
    last_processed_update_id = initial_updates_raw['result'][-1]['update_id']

while True:
    newest_update = last_processed_update_id + 1
    last_json = requests.get(f'https://api.telegram.org/bot{args.token}/getUpdates?offset={newest_update}').text
    last = json.loads(last_json)
    if last.get('result', 0):
        updates = last['result']
        last_processed_update_id = last['result'][-1]['update_id']
        process_updates(updates)
    else:
        continue
    time.sleep(2)




        


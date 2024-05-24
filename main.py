import time
import json
import telebot

# TOKEN DETAILS
TOKEN = "Netflix Cookies"

BOT_TOKEN = "6966902457:AAGx8wxCZWftQft1A-UMPnnKpMz7FetRzs8"
PAYMENT_CHANNEL = "@cookwithd"  # add payment channel here including the '@' sign
OWNER_ID = 5577450357  # write owner's user id here.. get it from @MissRose_Bot by /id
CHANNELS = ["@dailynetflixcookiesfree"]  # add channels to be checked here in the format - ["Channel 1", "Channel 2"]
# you can add as many channels here and also add the '@' sign before channel username
Mini_Withdraw = 3  # remove 0 and add the minimum withdraw you want to set
Per_Refer = 1  # add per refer bonus here

bot = telebot.TeleBot(BOT_TOKEN)

# Function to send announcements/status updates to users
def send_announcement(user_id, message):
    bot.send_message(user_id, message)

# Function to send announcement to all users
def send_announcement_to_all(message):
    data = json.load(open('users.json', 'r'))
    for user_id in data['id'].keys():
        send_announcement(user_id, message)

# Function to check if a user has joined specified channels
def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True

# Function to display menu options to users
def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '💸 Withdraw')
    keyboard.row('📊 Statistics')
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown",
                     reply_markup=keyboard)

# Your existing code...

@bot.message_handler(commands=['start'])
def start(message):
    user = message.chat.id
    msg = message.text
    if msg == '/start':
        user = str(user)
        data = json.load(open('users.json', 'r'))
        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1
        if user not in data['referby']:
            data['referby'][user] = user
        if user not in data['checkin']:
            data['checkin'][user] = 0
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        if user not in data['withd']:
            data['withd'][user] = 0
        if user not in data['id']:
            data['id'][user] = data['total'] + 1
        json.dump(data, open('users.json', 'w'))
        print(data)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            text='🤼‍♂️ Joined', callback_data='check'))
        msg_start = "*🍔 To Use This Bot You Need To Join This Channel - "
        for i in CHANNELS:
            msg_start += f"\n➡️ {i}\n"
        msg_start += "*"
        bot.send_message(user, msg_start,
                         parse_mode="Markdown", reply_markup=markup)
    else:
        # Handle referral link joining
        data = json.load(open('users.json', 'r'))
        user = message.chat.id
        user = str(user)
        refid = message.text.split()[1]
        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1
        if user not in data['referby']:
            data['referby'][user] = refid
        if user not in data['checkin']:
            data['checkin'][user] = 0
        if user not in data['balance']:
            data['balance'][user] = 0
        if user not in data['wallet']:
            data['wallet'][user] = "none"
        if user not in data['withd']:
            data['withd'][user] = 0
        if user not in data['id']:
            data['id'][user] = data['total'] + 1
        json.dump(data, open('users.json', 'w'))
        print(data)
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(
            text='🤼‍♂️ Joined', callback_data='check'))
        msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
        bot.send_message(user, msg_start,
                         parse_mode="Markdown", reply_markup=markups)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    ch = check(call.message.chat.id)
    if call.data == 'check':
        if ch == True:
            data = json.load(open('users.json', 'r'))
            user_id = call.message.chat.id
            user = str(user_id)
            bot.answer_callback_query(
                callback_query_id=call.id, text='✅ You joined Now you can earn Netflix Cookies')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if user not in data['refer']:
                data['refer'][user] = True

                if user not in data['referby']:
                    data['referby'][user] = user
                    json.dump(data, open('users.json', 'w'))
                if int(data['referby'][user]) != user_id:
                    ref_id = data['referby'][user]
                    ref = str(ref_id)
                    if ref not in data['balance']:
                        data['balance'][ref] = 0
                    if ref not in data['referred']:
                        data['referred'][ref] = 0
                    json.dump(data, open('users.json', 'w'))
                    data['balance'][ref] += Per_Refer
                    data['referred'][ref] += 1
                    bot.send_message(
                        ref_id, f"*🏧 New Referral on Level 1, You Got : +{Per_Refer} {TOKEN}*", parse_mode="Markdown")
                    json.dump(data, open('users.json', 'w'))
                    return menu(call.message.chat.id)
                else:
                    json.dump(data, open('users.json', 'w'))
                    return menu(call.message.chat.id)
            else:
                json.dump(data, open('users.json', 'w'))
                menu(call.message.chat.id)
        else:
            bot.answer_callback_query(
                callback_query_id=call.id, text='❌ You not Joined')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='🤼‍♂️ Joined', callback_data='check'))
            msg_start = "*🍔 To Use This Bot You Need To Join This Channel - \n➡️ @ Fill your channels at line: 101 and 157*"
            bot.send_message(call.message.chat.id, msg_start,
                             parse_mode="Markdown", reply_markup=markup)

# Your existing code...

if __name__ == "__main__":
    # Example usage:
    announcement_message = "🚨 Attention! New cookies have been added. Withdraw now!"
    send_announcement_to_all(announcement_message)
    # You can call send_announcement_to_all whenever you need to send an announcement to all users.


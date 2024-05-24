import time
import json
import telebot

##TOKEN DETAILS
TOKEN = "Netflix Cookies"
BOT_TOKEN = "7178545425:AAEiglxEGFiXMSVxQGsoe-T5RWKUbhz046w"
PAYMENT_CHANNEL = "@cookwithd" #add payment channel here including the '@' sign
OWNER_ID = 5577450357 #write owner's user id here
CHANNELS = ["@dailynetflixcookiesfree"] #add channels to be checked here in the format - ["Channel 1", "Channel 2"]
Points_Per_Refer = 1 # Points per refer
Required_Referals_For_Withdraw = 3 # Required referals to withdraw

bot = telebot.TeleBot(BOT_TOKEN)

def check_user_joined(id):
    for channel in CHANNELS:
        check = bot.get_chat_member(channel, id)
        if check.status == 'left':
            return False
    return True

def update_user_data(user, key, default_value):
    data = json.load(open('users.json', 'r'))
    if user not in data[key]:
        data[key][user] = default_value
        json.dump(data, open('users.json', 'w'))
    return data

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🏠 Home')
    keyboard.row('👥 Invite', '💰 Withdraw')
    keyboard.row('🔍 Balance', '📞 Support')
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = str(message.chat.id)
        data = json.load(open('users.json', 'r'))
        data = update_user_data(user, 'referred', 0)
        data = update_user_data(user, 'referby', user)
        data = update_user_data(user, 'balance', 0)
        data = update_user_data(user, 'points', 0)
        json.dump(data, open('users.json', 'w'))
        
        if not check_user_joined(message.chat.id):
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='📢 Join our Channel', url=f"https://t.me/{CHANNELS[0][1:]}"))
            bot.send_message(message.chat.id, "You need to join our channel to use this bot.", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Welcome! You can now use the bot.", parse_mode="Markdown")
            menu(message.chat.id)
    except Exception as e:
        bot.send_message(OWNER_ID, f"Error in start command: {e}")

@bot.message_handler(commands=['check'])
def check(message):
    if check_user_joined(message.chat.id):
        bot.send_message(message.chat.id, "You have joined the channel and can use the bot now.")
        menu(message.chat.id)
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='📢 Join our Channel', url=f"https://t.me/{CHANNELS[0][1:]}"))
        bot.send_message(message.chat.id, "You need to join our channel to use this bot.", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_text(message):
    user = str(message.chat.id)
    data = json.load(open('users.json', 'r'))

    if message.text == '👥 Invite':
        bot_name = bot.get_me().username
        ref_link = f'https://telegram.me/{bot_name}?start={message.chat.id}'
        bot.send_message(message.chat.id, f"Invite your friends using this link:\n{ref_link}\nEarn 1 point per referral. Get 3 points to withdraw 1 Netflix Cookie.")

    elif message.text == '💰 Withdraw':
        if data['points'][user] >= Required_Referals_For_Withdraw:
            data['points'][user] -= Required_Referals_For_Withdraw
            json.dump(data, open('users.json', 'w'))
            bot.send_message(message.chat.id, "Your withdraw request has been sent. Cookies will be Sent 7AM - 10PM (IST)")
            bot.send_message(PAYMENT_CHANNEL, f"User @{message.from_user.username} ({message.chat.id}) has requested a withdrawal. Points: {Required_Referals_For_Withdraw}")
        else:
            bot.send_message(message.chat.id, f"You need {Required_Referals_For_Withdraw} points to withdraw.")

    elif message.text == '🔍 Balance':
        points = data['points'][user]
        bot.send_message(message.chat.id, f"You have {points} points.")

    elif message.text == '📞 Support':
        bot.send_message(message.chat.id, "For support, contact @your_support_contact")

    elif message.text == '🏠 Home':
        menu(message.chat.id)

@bot.message_handler(commands=['referral'])
def referral(message):
    try:
        referrer_id = message.text.split()[1]
        user = str(message.chat.id)
        data = json.load(open('users.json', 'r'))
        
        if user not in data['referred']:
            data['referred'][user] = 0
            data['referby'][user] = referrer_id
            json.dump(data, open('users.json', 'w'))
            
            if referrer_id != user:
                data['points'][referrer_id] += Points_Per_Refer
                json.dump(data, open('users.json', 'w'))
                bot.send_message(referrer_id, f"You have earned {Points_Per_Refer} points for a referral.")
                
        menu(message.chat.id)
    except Exception as e:
        bot.send_message(OWNER_ID, f"Error in referral command: {e}")

if __name__ == '__main__':
    bot.polling(none_stop=True)

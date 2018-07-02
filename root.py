import time, pickle, telepot, json, shutil
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from databases.Menu import Menu
token = '592251535:AAECV51q0myLYpouj7lNs7IH28qSMw4KuU8'
TelegramBot = telepot.Bot(token)

latestId=0
initial_message_sent = False
admins = ["Kirshan", "Arsham"]
image_extensions = ["jpg", "jpeg", "png"]

def send_message(chat_id, message, reply_markup=[]):
    keyboard_buttons = []
    for i in reply_markup:
        keyboard_buttons.append([KeyboardButton(text=i)])
    TelegramBot.sendMessage(chat_id, message, reply_markup = ReplyKeyboardMarkup(keyboard = keyboard_buttons))

while True:
    #receiving messages from telegram
    messages=TelegramBot.getUpdates(offset=latestId)

    #geting the latest ID
    if messages:
        latestId=messages[-1]['update_id']+1
        if initial_message_sent == False:
            send_message(messages[0]['message']['chat']['id'], "Keyboard Buttons Activated", ["Hi", "Buy"])
            initial_message_sent = True
        else:
            for message in messages:
                try:
                    file = dict(TelegramBot.getFile(message["message"]["photo"][-1]["file_id"]))
                    if file["file_path"].split(".")[1] in image_extensions:
                        file_id = file["file_id"]
                        filename = file["file_path"].split("/")[1]
                        final_destination = "static/images/{}".format(filename)
                        TelegramBot.download_file(file_id, final_destination)
                except:
                    current_message = message["message"]["text"]
                    chat_id = message['message']['chat']['id']
                    user_info = message['message']['from']
                    date_info = time.localtime(messages[0]["message"]["date"])
                    current_date = "{}/{}/{}".format(date_info.tm_mday, date_info.tm_mon, date_info.tm_year)
                    menu = Menu("menu.json")
                    menu_items = menu.get_menu(spec_item="name")
                    if current_message == "Hi":
                        send_message(chat_id, "Hi {} Today is {}".format(user_info['first_name'], current_date))
                    elif current_message == "Buy":
                        send_message(chat_id, "What to buy?", menu_items)
        print messages
        print '-----'*10

    try:
        if messages and messages[-1]['message']['text'] == "stop":
            break
    except:
        pass
import telepot
elcar_bot_token='310491662:AAHuhBoA_-8RkG-Xrq5kIKYVvgXMBXCJUKA'
bot = telepot.Bot(elcar_bot_token)
bot.getMe()

"""
{u'username': u'elcar_bot', u'first_name': u'elcBot', u'id': 310491662}
"""
from pprint import pprint
response = bot.getUpdates()
pprint(response)
"""
[{u'message': {u'chat': {u'first_name': u'marco',
                         u'id': 192029425,
                         u'type': u'private',
                         u'username': u'marcoMes'},
               u'date': 1501525076,
               u'from': {u'first_name': u'marco',
                         u'id': 192029425,
                         u'language_code': u'en-GB',
                         u'username': u'marcoMes'},
               u'message_id': 2,
               u'text': u'/'},
  u'update_id': 384918123},
 {u'message': {u'chat': {u'first_name': u'marco',
                         u'id': 192029425,
                         u'type': u'private',
                         u'username': u'marcoMes'},
               u'date': 1501525086,
               u'entities': [{u'length': 5,
                              u'offset': 0,
                              u'type': u'bot_command'}],
               u'from': {u'first_name': u'marco',
                         u'id': 192029425,
                         u'language_code': u'en-GB',
                         u'username': u'marcoMes'},
               u'message_id': 3,
               u'text': u'/help'},
  u'update_id': 384918124}]
"""
bot.getUpdates(offset=4)
"""
[{u'message': {u'date': 1501525076, u'text': u'/', u'from': {u'username': u'marcoMes', u'first_name': u'marco', u'id': 192029425, u'language_code': u'en-GB'}, u'message_id': 2, u'chat': {u'username': u'marcoMes', u'first_name': u'marco', u'type': u'private', u'id': 192029425}}, u'update_id': 384918123}, {u'message': {u'from': {u'username': u'marcoMes', u'first_name': u'marco', u'id': 192029425, u'language_code': u'en-GB'}, u'text': u'/help', u'entities': [{u'length': 5, u'type': u'bot_command', u'offset': 0}], u'chat': {u'username': u'marcoMes', u'first_name': u'marco', u'type': u'private', u'id': 192029425}, u'date': 1501525086, u'message_id': 3}, u'update_id': 384918124}]
"""

from telepot.loop import MessageLoop
def handle(msg):
  pprint(msg)
MessageLoop(bot, handle).run_as_thread()
"""
{u'chat': {u'first_name': u'marco',
           u'id': 192029425,
           u'type': u'private',
           u'username': u'marcoMes'},
 u'date': 1501606960,
 u'from': {u'first_name': u'marco',
           u'id': 192029425,
           u'language_code': u'en-GB',
           u'username': u'marcoMes'},
 u'message_id': 5,
 u'text': u'Azz'}
"""

bot.sendMessage(192029425, 'azzAzzAzzAzz!')
 {u'date': 1501607262, u'text': u'azzAzzAzzAzz!', u'from': {u'username': u'elcar_bot', u'first_name': u'elcBot', u'id': 310491662}, u'message_id': 7, u'chat': {u'username': u'marcoMes', u'first_name': u'marco', u'type': u'private', u'id': 192029425}}

chatId=192029425
bot.sendMessage(chatId, 'rifare!')

import sys
import time
import telepot
from telepot.loop import MessageLoop

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
import logging;logging.basicConfig(level=logging.WARNING,filename='h.txt',filemode='w',
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import os
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, RegexHandler
from keep_alive import keep_alive
import matches
import score
import requests
import time

def show_current(bot, update):
    msg=matches.show_current()
    update.message.reply_text(msg)
    update.message.reply_text('Enter the number of the match you want to see')
    return 0

def hello(bot, update):
    update.message.reply_text(
    'Hello {}'.format(update.message.from_user.first_name))

user_id=set()
def get_match(bot, context):
    print('here')
    num=context.message.text
    print(num)
    match_title = matches.title_match[int(num)-1]
    match_link = matches.link_match[int(num)-1]
    print(f'I got the number. So you want to receive updates of {match_title}')
    context.message.reply_text(f'I got the number. So you want to receive updates of {match_title}')


    global user_id
    user_id.add(context.message.from_user.id)
    print(user_id)
    set_match(match_link, context)
    return 1

want=True
ID=None
URL="https://www.cricbuzz.com/match-api/livematches.json"
last_ball = 0.0

def set_match(ur, update):
    global ID
    ID = ur.split('/')[2]
    
    url = "https://www.cricbuzz.com/match-api/livematches.json"
    global want
    want=True
##    while want:
##        last_ball, msg=score.get_score(url, ID, last_ball)
##        update.message.reply_text(msg)
##        for __ in range(10):
##            time.sleep(1)
    match_json = requests.get(url).json()
    this_match = match_json['matches'][ID]
    match_state = this_match['state']

    if match_state=='preview':
      print('Match yet to start')
      update.message.reply_text('Match yet to start')
      start_time = this_match['start_time']
      start_time_local = time.localtime(int(start_time))

      print(f"Match will begin at local time {start_time_local[3]}:{start_time_local[4]}, {start_time_local[2]}/{start_time_local[1]}/{start_time_local[0]}")
      print((int(start_time)-int(time.time()))//60, end='')
      update.message.reply_text(f"Match will begin at local time {start_time_local[3]}:{start_time_local[4]}, {start_time_local[2]}/{start_time_local[1]}/{start_time_local[0]}\n{(int(start_time)-int(time.time()))//60} minutes remaining")
      
      # update.message.reply_text(f'')
      update.message.reply_text('Please send a request after the match has started\nSend /show_current to view other matches')

    elif match_state=='complete' or match_state=='stump' or match_state=='mom':
      match_status = this_match['status']
      print(match_status)
      update.message.reply_text(match_status)

      cur_score = this_match['score']['batting']['score']
      print(f'Current score: {cur_score}')
      update.message.reply_text(f'Current score: {cur_score}')
      print(f"{this_match['toss']['winner']} won the toss and chose {this_match['toss']['decision']}")
      update.message.reply_text(f"{this_match['toss']['winner']} won the toss and chose {this_match['toss']['decision']}\n...\nSend /show_current to view other matches")

    else:
      print('else')
      toss = this_match['toss']
      update.message.reply_text(f"{toss['winner']} won the toss and chose {toss['decision']}")

      cur_score = this_match['score']['batting']['score']
      print(f'Current score: {cur_score}')
      update.message.reply_text(f'Current score: {cur_score}')
      
      print(f"{this_match['toss']['winner']} won the toss and chose {this_match['toss']['decision']}")
      
      global job_minute
      global j
      job_minute = j.run_repeating(get_score, interval=10, first=0)

job_minute=None

def cancel(update, context):
    update.message.reply_text('cancelled')
    global job_minute
    job_minute.schedule_removal()
    global user_id
    user_id.remove(context.message.from_user.id)

def stop(update, context):
    context.message.reply_text('stopped')
    global user_id
    user_id.remove(context.message.from_user.id)


def get_score(bot, context):
    global ID
    global URL
    global want
    global last_ball
    msg=None
    print("-----")
    print(last_ball, msg)
    print("----")
    last_ball, msg=score.get_score(URL, ID, last_ball)
    print("called")
    if msg:
        global user_id
        for u in user_id:
          bot.send_message(u, msg)

def start(bot, update):
    update.message.reply_text(
    f'''Hello {update.message.from_user.first_name}\nI am @CricUpdateBot bot and I can
        send you a message whenever there is a boundary hit or wicket taken
        in a cricket match.\n
        To begin, send /show_current command and I will list out the current
        matches being played.

        ''')

j=None
def main():
        keep_alive()
        token = os.environ.get("TOKEN")
        updater = Updater(token)

        conv_handler = ConversationHandler(
                entry_points=[CommandHandler('show_current', show_current)],

                states={
                0: [RegexHandler('^[0-9]+$', get_match)]
        ##
        ##            PHOTO: [MessageHandler(Filters.photo, photo),
        ##                    CommandHandler('skip', skip_photo)],
        ##
        ##            LOCATION: [MessageHandler(Filters.location, location),
        ##                       CommandHandler('skip', skip_location)],
        ##
        ##            BIO: [MessageHandler(Filters.text, bio)]
                },

                fallbacks=[CommandHandler('cancel', cancel)],
                allow_reentry=True
        )

        ##updater.dispatcher.add_handler(CommandHandler('current_matches',show_current))
        updater.dispatcher.add_handler(conv_handler)
        global j
        j = updater.job_queue

        updater.dispatcher.add_handler(CommandHandler('start',start))
        # updater.dispatcher.add_handler(CommandHandler('show_current',show_current))
        updater.dispatcher.add_handler(CommandHandler('cancel',cancel))
        updater.dispatcher.add_handler(CommandHandler('stop',stop))
        updater.start_polling()
        updater.idle()
        

if __name__=='__main__':
        main()
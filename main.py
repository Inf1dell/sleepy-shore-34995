from telebot import *
import db

bot = telebot.TeleBot('5805166543:AAH0T_bwnR2bQ19TVJsWoCMLB8b9RBeunNc')


counter = 0
sec = 0

user_counter={}
user_correct={}

all = db.ask
L=[10, 7, 2, 9, 0, 4, 3, 6, 5]
random.shuffle(L)

@bot.message_handler(commands=['start'])
def start_message(message):
    global user_counter, user_correct, my_quiz, L
    # bot.send_message(message.chat.id, "Введите своё имя")
    if str(message.chat.id) in user_counter:
        if(user_counter.get(str(message.chat.id)) < 15):
            bot.send_message(message.chat.id, "Restart")
            user_counter[str(message.chat.id)] = 1
            user_correct[str(message.chat.id)] = 0
            bot.send_photo(message.chat.id, open("img/0.jpg", 'rb'))
            my_quiz = bot.send_poll(message.chat.id, question=db.ask[L[0]], type='quiz', options=db.answers[L[0]],
                          open_period=30,
                          is_anonymous=False, correct_option_id=int(db.correct[L[0]]), )
        else:
            bot.send_message(message.chat.id, "Вы уже прошли тест.")
    else:
        user_counter[str(message.chat.id)] = 1
        user_correct[str(message.chat.id)] = 0
        bot.send_photo(message.chat.id, open("img/0.jpg", 'rb'))
        my_quiz = bot.send_poll(message.chat.id, question=db.ask[L[0]], type='quiz', options=db.answers[L[0]],
                          open_period=30,
                          is_anonymous=False, correct_option_id=int(db.correct[L[0]]), )
@bot.poll_answer_handler()
def get_answer(PollAnswer):
    global user_counter,my_quiz,L
    msg = PollAnswer.user.id
    mun = PollAnswer.user.username
    muf = PollAnswer.user.first_name


    if my_quiz.poll.correct_option_id == PollAnswer.option_ids[0]:
        user_correct[str(msg)]=user_correct.get(str(msg))+1

    if(user_counter.get(str(msg))<9):
        bot.send_photo(msg, open("img/"+str(user_counter.get(str(msg)))+".jpg", 'rb'))
        my_quiz = bot.send_poll(msg, question=db.ask[L[user_counter.get(str(msg))]], type='quiz', options=db.answers[L[user_counter.get(str(msg))]],
                          open_period=30,
                          is_anonymous=False, correct_option_id=int(db.correct[L[user_counter.get(str(msg))]]), )
        user_counter[str(msg)]=user_counter.get(str(msg))+1
    else:
        bot.send_message(msg, 'Правильно: '+str(user_correct.get(str(msg))))
        bot.send_message(msg, 'Участники опроса могут бесплатно посетить музей "Казан арты" г. Арск ул. Сызгановых, 22 и получить памятные подарки.')









if __name__ == "__main__":
    bot.infinity_polling()
    time.sleep(3)
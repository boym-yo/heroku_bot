import telebot
import config 
import datetime as dt
import threading
import schedule

from telebot import types

bot = telebot.TeleBot(config.TOKEN)
count = 0 # количество сиг
counter = 0 # количество стартов
dict = {
    'start_data': 'count'
    } # бд 

@bot.message_handler(commands=['start'])
def welcome(message):

    global counter

    #sticker
    sticker = open('/Users/supreme/Desktop/test_bot/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    #keyboard 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('+1 сижка')
    item2 = types.KeyboardButton('инфа за последние 5 дней')
    markup.add(item1, item2)

    if counter == 0:
        #welcome message

        bot.send_message(message.chat.id, 'Привет, {0.first_name}!\nЯ — <b>{1.first_name}</b>, и я помогу бросить тебе курить сижки ;) Для этого просто кликай по кнопке после каждого покура — а остальное уже за мной 😏'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
        msg = bot.send_message(message.chat.id, f'Начнем с количества сиг в день: напиши максимальное доступное для тебя число сигарет в день')
        bot.register_next_step_handler(msg, max_number)
        counter += 1
    else:
        bot.send_message(message.chat.id, f'Снова приветствуем, {message.from_user.first_name}!\nЕсли хочешь сбросить прогресс или изменить доступное количество сигарет за день, то советуем использовать команды:\n/reset — сброс всех данных\n/change — изменить количество сигарет в день\nУспехов✨', parse_mode='html', reply_markup=markup)
        

def max_number(message):
    global count
    try:
        test = int(message.text)
        if test > 0:
            count = test
            msg = bot.send_message(message.chat.id, f'Окей, запомнили ({count}) 😏')
            #bot.register_next_step_handler(msg, mirror_answer)
            msg
        else:
            msg = bot.send_message(message.chat.id, f'Число должно быть больше нуля, попробуй снова 😉')
            bot.register_next_step_handler(msg, max_number)
    except:
        msg = bot.reply_to(message, f'Где-то есть ошибка, давай попробуем снова 🤔')
        bot.register_next_step_handler(msg, max_number)


@bot.message_handler(commands=['data'])
def send_info(message):
    
    msg = ''
    for key in dict:
       msg += f'\n{key}, {dict[key]}'
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['change'])
def changer(message):
    global count
    bot.send_message(message.chat.id, f'Введи новое количество сиг в день:')
    try:
        test = int(message.text)
        if test > 0:
            count = test
            msg = bot.send_message(message.chat.id, f'Окей, запомнили ({count}) 😏')
            #bot.register_next_step_handler(msg, mirror_answer)
            msg
        else:
            msg = bot.send_message(message.chat.id, f'Число должно быть больше нуля, попробуй снова 😉')
            bot.register_next_step_handler(msg, changer)
    except:
        msg = bot.reply_to(message, f'Где-то есть ошибка, давай попробуем снова 🤔')
        bot.register_next_step_handler(msg, changer)    

@bot.message_handler(commands=['info'])

def info(message):
    bot.send_message(message.chat.id, f'Вся информация о командах есть в меню слева ;)')

@bot.message_handler(commands=['about'])

def about(message):
    bot.send_message(message.chat.id, f'Просто бот, который просто создан с целью помочь бросить курить сижки 💫')

@bot.message_handler(commands=['reset'])
def reset(message):
    global count, counter, dict
    count = 0
    counter = 0
    dict = {'': None}
    bot.send_message(message.chat.id, f'Весь прогресс успешно сброшен 😎')


@bot.message_handler(content_types=['text'])

def mirror_answer(message):
    
    global dict
    global count
    if message.text == '+1 сижка':

        now = dt.datetime.utcnow()
        period = dt.timedelta(hours=3)
        moscow_time = now + period
        f_time = moscow_time.strftime('%d.%m.%Y')

        if f_time == list(dict.keys())[-1]:
            dict[f_time] += 1
        else:
            dict.setdefault(f_time, 1)
        
        if dict[f_time] == 1:
            text = f'Засчитано!\nЗа сегодня ({f_time}) была выкурена {dict[f_time]} сижка 🙀'
        elif 2 <= dict[f_time] <= 4:
            text = f'Засчитано!\nЗа сегодня ({f_time}) было выкурено {dict[f_time]} сижки 🙀'
        else:
            text = f'Засчитано!\nЗа сегодня ({f_time}) было выкурено {dict[f_time]} сижек 🙀'
        
        
        if dict[f_time] == count:
            text += f'\nP.S. На этом пора закругляться на сегодня ;)'
        elif dict[f_time] > count:
            text += f'\nP.S. Уже борщишь, пирожочек 😠'
        msg = bot.send_message(message.chat.id, text)

    elif message.text == 'инфа за последние 5 дней':

        dictlength = len(list(dict.keys()))
        output = f''

        if dictlength >= 5:
            for i in reversed(range(1,6)):
                output += f'{list(dict.keys())[-i]} — {list(dict.values())[-i]}\n'
        else:
            for i in reversed(range(1, (dictlength+1))):
                output += f'{list(dict.keys())[-i]} — {list(dict.values())[-i]}\n'

        msg = bot.send_message(message.chat.id, output)
    else:
        msg = bot.send_message(message.chat.id, 'Попробуй другой запрос :)')
    #bot.register_next_step_handler(msg, mirror_answer)
    msg
    


# RUN

bot.polling(none_stop=True)



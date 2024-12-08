import telebot
import random
from secr import secrets
from telebot import types
import requests, json
from secr import head

headers = head
token=secrets.get('bot_api_token')
bot=telebot.TeleBot(token)
states={}

@bot.message_handler(commands=['start'])
def start_message(message):
    global states
    iduser=message.from_user.id
    states[iduser] = {'country':None, 'content_type':'', 'ganres':[], 'year':None, 'length':None, 'rating':''}
    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button=types.KeyboardButton("Начать поиск")
    random_button=types.KeyboardButton("Случайный фильм")
    markup.row(yes_button)
    markup.row(random_button)
    bot.send_message(message.chat.id, text="Привет! Я Telegram-бот, который поможет выбрать фильм на вечер👾".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, what_type)

@bot.message_handler(content_types=['text'])
def what_type(message):
    if isRestart(message):
        start_message(message)
    else:
        global idc_button, strtover_button
        if (message.text=="Начать поиск"):
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            movie_button=types.KeyboardButton("Фильм")
            cartoon_button=types.KeyboardButton("Мультфильм")
            anime_button=types.KeyboardButton("Аниме")
            idc_button=types.KeyboardButton("Всё равно")
            strtover_button=types.KeyboardButton("Начать поиск заново")
            markup.row(movie_button, cartoon_button, anime_button)
            markup.row(idc_button)
            bot.send_message(message.chat.id, text="Что ищем?".format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, rus_or_not)
        if (message.text=="Случайный фильм"):
            randomm(message)

def isRestart(message):
    if message.text=='/start' or message.text=='Начать поиск заново':
        return True

def randomm(message):
    if isRestart(message):
        start_message(message)
    else:
        query={
            'page': 1,
            'limit': 1,
            'notNullFields': ['name', 'year', 'shortDescription', 'poster.url'], 
            'selectFields': ['name', 'year', 'shortDescription', 'poster.url']
        }
        bot.send_message(message.chat.id, text="Идёт поиск🔍")
        response=requests.get('https://api.kinopoisk.dev/v1.4/movie/random', params=query, headers=headers)
        namee=response.json()['name']
        year=response.json()['year']
        descriptionn=response.json()['shortDescription']
        poster=response.json()['poster']['previewUrl']
        link_params=types.LinkPreviewOptions(
                url=poster,
                is_disabled=False, 
                prefer_large_media=True, 
                prefer_small_media=True, 
                show_above_text=True
            )
        mes_text=f'Возможно, тебе понравится "{namee}" ({year}). \nОписание: {descriptionn}'
        bot.send_message(message.chat.id, text=mes_text.format(message.from_user), link_preview_options=link_params)

def rus_or_not(message):
    if isRestart(message):
        start_message(message)
    else:
        global idc_button, states
        iduser=message.from_user.id 
        if (message.text=="Аниме"):
            states[iduser]['content_type']='anime'
            get_ganre(message)
        else:
            if (message.text=="Мультфильм"):
                states[iduser]['content_type']='cartoon'
            if (message.text=="Фильм"):
                states[iduser]['content_type']='movie'
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            rus_button=types.KeyboardButton("Российский")
            foreign_button=types.KeyboardButton("Зарубежный")
            idc_button=types.KeyboardButton("Всё равно")
            markup.row(rus_button, foreign_button, idc_button)
            bot.send_message(message.chat.id, text="Российский или зарубежный?".format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, get_country)

def get_country(message):
    if isRestart(message):
        start_message(message)
    else:
        if (message.text=="Зарубежный"):
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            usa_button=types.KeyboardButton("США")
            france_button=types.KeyboardButton("Франция")
            britain_button=types.KeyboardButton("Великобритания")
            sk_button=types.KeyboardButton("Корея Южная")
            spain_button=types.KeyboardButton("Испания")
            germ_button=types.KeyboardButton("Германия")
            italy_button=types.KeyboardButton("Италия")
            japan_button=types.KeyboardButton("Япония")
            canada_button=types.KeyboardButton("Канада")
            markup.row(idc_button)
            markup.row(usa_button, france_button, britain_button)
            markup.row(germ_button, spain_button, italy_button)
            markup.row(japan_button, canada_button, sk_button)
            bot.send_message(message.chat.id, text="Какая страна?".format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, get_ganre)
        elif (message.text=="Российский"):
            get_ganre(message)

def get_ganre(message):
    if isRestart(message):
        start_message(message)
    else:
        global states, idc_button
        iduser=message.from_user.id
        if (message.text =='Всё равно'):
            states[iduser]['country']=['!Россия', '!СССР']
        elif message.text == "Российский":
            states[iduser]['country']=['Россия', 'СССР']
        elif message.text == "Аниме":
            states[iduser]['country']=None
        else:
            states[iduser]['country']=message.text
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        bi_button=types.KeyboardButton("Биография")
        bo_button=types.KeyboardButton("Боевик")
        we_button=types.KeyboardButton("Вестерн")
        de_button=types.KeyboardButton("Детектив")
        doc_button=types.KeyboardButton("Документальный")
        dr_button=types.KeyboardButton("Драма")
        com_button=types.KeyboardButton("Комедия")
        crim_button=types.KeyboardButton("Криминал")
        melo_button=types.KeyboardButton("Мелодрама")
        mus_button=types.KeyboardButton("Мюзикл")
        adven_button=types.KeyboardButton("Приключения")
        fam_button=types.KeyboardButton("Семейный")
        thrill_button=types.KeyboardButton("Триллер")
        horr_button=types.KeyboardButton("Ужасы")
        fant_button=types.KeyboardButton("Фантастика")
        fan_button=types.KeyboardButton("Фэнтези") 
        markup.row(idc_button)
        markup.row(bi_button, bo_button, we_button, de_button)
        markup.row(doc_button, dr_button, com_button, fam_button)
        markup.row(crim_button, melo_button, mus_button, adven_button)
        markup.row(thrill_button, horr_button, fan_button, fant_button)
        bot.send_message(message.chat.id, text="Какой жанр?".format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, more_ganres)
    
def more_ganres(message):
    if isRestart(message):
        start_message(message)
    else:
        global states
        iduser=message.from_user.id
        if (message.text=="Всё равно") or (message.text=="Нет"):
            get_year(message)
        else:
            states[iduser]['ganres'].append('+' + message.text.lower())
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            bi_button=types.KeyboardButton("Биография")
            bo_button=types.KeyboardButton("Боевик")
            we_button=types.KeyboardButton("Вестерн")
            de_button=types.KeyboardButton("Детектив")
            doc_button=types.KeyboardButton("Документальный")
            dr_button=types.KeyboardButton("Драма")
            com_button=types.KeyboardButton("Комедия")
            crim_button=types.KeyboardButton("Криминал")
            melo_button=types.KeyboardButton("Мелодрама")
            mus_button=types.KeyboardButton("Мюзикл")
            adven_button=types.KeyboardButton("Приключения")
            fam_button=types.KeyboardButton("Семейный")
            thrill_button=types.KeyboardButton("Триллер")
            horr_button=types.KeyboardButton("Ужасы")
            fant_button=types.KeyboardButton("Фантастика")
            fan_button=types.KeyboardButton("Фэнтези") #17
            no_button=types.KeyboardButton("Нет")
            markup.row(no_button)
            markup.row(bi_button, bo_button, we_button, de_button)
            markup.row(doc_button, dr_button, com_button, fam_button)
            markup.row(crim_button, melo_button, mus_button, adven_button)
            markup.row(thrill_button, horr_button, fan_button, fant_button)
            bot.send_message(message.chat.id, text="Добавить ещё жанр?".format(message.from_user), reply_markup=markup)
            bot.register_next_step_handler(message, more_ganres)
        
def get_year(message):
    if isRestart(message):
        start_message(message)
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        a_button=types.KeyboardButton("2020-2024")
        b_button=types.KeyboardButton("2010-2020")
        c_button=types.KeyboardButton("2000-2010")
        d_button=types.KeyboardButton("1990-2000")
        e_button=types.KeyboardButton("1980-1990")
        f_button=types.KeyboardButton("1930-1980")
        markup.row(idc_button)
        markup.row(a_button, b_button, c_button)
        markup.row(d_button, e_button, f_button)
        bot.send_message(message.chat.id, text="Какие года? (выберете интервал или напишите год)".format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, get_length)

def get_length(message):
    if isRestart(message):
        start_message(message)
    else:
        global states
        iduser=message.from_user.id
        if message.text != 'Всё равно': 
            states[iduser]['year']=message.text
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        a_button=types.KeyboardButton("Не более часа")
        b_button=types.KeyboardButton("Час-два")
        c_button=types.KeyboardButton("Два-три часа")
        markup.row(idc_button)
        markup.row(a_button, b_button, c_button)
        bot.send_message(message.chat.id, text="Какая длительность?".format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, get_rating)

def get_rating(message):
    if isRestart(message):
        start_message(message)
    else:
        global states
        iduser=message.from_user.id
        if message.text != 'Всё равно':
            if message.text == 'Не более часа':
                states[iduser]['length']='1-60'
            elif message.text == 'Час-два':
                states[iduser]['length']='61-120'  
            elif message.text == 'Два-три часа':
                states[iduser]['length']='121-200'
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        g_button=types.KeyboardButton("G")
        gp_button=types.KeyboardButton("GP")
        pg_button=types.KeyboardButton("PG")
        pg13_button=types.KeyboardButton("PG-13")
        r_button=types.KeyboardButton("R")
        nc_button=types.KeyboardButton("NC-17")
        markup.row(idc_button)
        markup.row(g_button, gp_button, pg_button)
        markup.row(pg13_button, r_button, nc_button)
        bot.send_message(message.chat.id, text="Какой рейтинг MPAA?".format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, get_sort)

def get_sort(message):
    if isRestart(message):
        start_message(message)
    else:
        global states
        iduser=message.from_user.id
        if message.text != 'Всё равно':
            states[iduser]['rating']=message.text
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes_button=types.KeyboardButton("Да")
        no_button=types.KeyboardButton("Нет")
        markup.row(yes_button, no_button)
        bot.send_message(message.chat.id, text="Сортировать по рейтингу?".format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, result)


def result(message):
    if isRestart(message):
        start_message(message)
    else:
        global states
        iduser=message.from_user.id
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        again_button=types.KeyboardButton("Другой вариант")
        strtover_button=types.KeyboardButton("Начать поиск заново")
        bot.send_message(message.chat.id, text="Идёт поиск🔍")
        query={
            'page': 1,
            'limit': 100,
            'notNullFields': ['name', 'year', 'shortDescription', 'countries.name', 'rating.kp', 'poster.url', 'movieLength'],
            'sortField': 'rating.kp',
            'sortType': -1,
            'rating.kp': '1-10',
            'selectFields': ['name', 'year', 'shortDescription', 'poster'], 
            'type':states[iduser]['content_type'],
            'countries.name':states[iduser]['country'],
            'genres.name':states[iduser]['ganres'],
            'year':states[iduser]['year'],
            'movieLength':states[iduser]['length'],
            'ratingMPAA':states[iduser]['rating'],
            'isSeries':False
        }
        print('запрос', iduser)
        response=requests.get('https://api.kinopoisk.dev/v1.4/movie', params=query, headers=headers)
        print(query)
        states[iduser]['movies']=response.json()['docs']
        print(len(states[iduser]['movies']))
        if len(states[iduser]['movies'])==0:
            markup.row(strtover_button)
            bot.send_message(message.chat.id, text="Подходящих фильмов нет😞", reply_markup=markup)
            bot.register_next_step_handler(message, next)
        if len(states[iduser]['movies'])>0:
            markup.row(again_button, strtover_button)
            if message.text=='Да':
                num=0
            if message.text=='Нет':
                num=random.randrange(0, len(states[iduser]['movies']))
            namee=states[iduser]['movies'][num]['name']
            year=states[iduser]['movies'][num]['year']
            descriptionn=states[iduser]['movies'][num]['shortDescription']
            poster=states[iduser]['movies'][num]['poster']['previewUrl']
            link_params=types.LinkPreviewOptions(
                    url=poster,
                    is_disabled=False, 
                    prefer_large_media=True, 
                    prefer_small_media=True, 
                    show_above_text=True
                )
            mes_text=f'Возможно, тебе понравится "{namee}" ({year}). \nОписание: {descriptionn}'
            bot.send_message(message.chat.id, text=mes_text.format(message.from_user), link_preview_options=link_params, reply_markup=markup)
            states[iduser]['movies'].pop(num)
            if message.text=='Да':
                bot.register_next_step_handler(message, next)
            if message.text=='Нет':
                bot.register_next_step_handler(message, next_rn)
    
        
def next(message):
    if isRestart(message):
        start_message(message)
    else:
        global states
        iduser=message.from_user.id
        if (message.text=="Начать поиск заново"):
            start_message(message)
        elif (message.text=="Другой вариант"):
            if len(states[iduser]['movies']) > 0:
                namee=states[iduser]['movies'][0]['name']
                year=states[iduser]['movies'][0]['year']
                descriptionn=states[iduser]['movies'][0]['shortDescription']
                poster=states[iduser]['movies'][0]['poster']['previewUrl']
                link_params=types.LinkPreviewOptions(
                        url=poster,
                        is_disabled=False, 
                        prefer_large_media=True, 
                        prefer_small_media=True, 
                        show_above_text=True
                    )
                mes_text=f'Возможно, тебе понравится "{namee}" ({year}). \nОписание: {descriptionn}'
                bot.send_message(message.chat.id, text=mes_text.format(message.from_user), link_preview_options=link_params)
                states[iduser]['movies'].pop(0)
            if len(states[iduser]['movies']) == 0:
                bot.send_message(message.chat.id, text="Больше нет подходящих фильмов")
            bot.register_next_step_handler(message, next) 

def next_rn(message):
    if isRestart(message):
        start_message(message)
    else:
        global states
        iduser=message.from_user.id
        if (message.text=="Начать поиск заново"):
            start_message(message)
        elif (message.text=="Другой вариант"):
            if len(states[iduser]['movies']) > 0:
                num=random.randrange(0, len(states[iduser]['movies']))
                namee=states[iduser]['movies'][num]['name']
                year=states[iduser]['movies'][num]['year']
                descriptionn=states[iduser]['movies'][num]['shortDescription']
                poster=states[iduser]['movies'][num]['poster']['previewUrl']
                link_params=types.LinkPreviewOptions(
                        url=poster,
                        is_disabled=False, 
                        prefer_large_media=True, 
                        prefer_small_media=True, 
                        show_above_text=True
                    )
                mes_text=f'Возможно, тебе понравится "{namee}" ({year}). \nОписание: {descriptionn}'
                bot.send_message(message.chat.id, text=mes_text.format(message.from_user), link_preview_options=link_params)
                states[iduser]['movies'].pop(num)
            if len(states[iduser]['movies']) < 1:
                bot.send_message(message.chat.id, text="Больше нет подходящих фильмов")
            bot.register_next_step_handler(message, next)   

bot.polling(none_stop=True, interval=0)
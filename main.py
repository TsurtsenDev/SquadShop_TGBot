import telebot
from telebot import types
from telebot.types import Message, WebAppInfo
import webbrowser
import sqlite3
import asyncio
import sqlite3
import database

telebot.TeleBot("7057179821:AAEjvdjmucsJgMuVAJFo8t5FD5837yK67HY")

botname = "SkySquad"

admin_ids = ['6866142004, ']  # Список chat_id администраторов бота

chat_reviews = -1002086738096  # ID чата для отзывов

orders = {}  # Словарь для хранения заказов пользователей
price = {}  # Словарь для хранения цен
help_request = {}  #Словарь для хранения запросов помощи
owners = {'5111998837'}  # Словарь для хранения chat_id владельцев
price_gold = 1.5  # Цена голды (1 штука)
golds = {}  # Словарь для хранения количества голды



@bot.message_handler(commands=['start', 'menu'])
def start(message):
  markup = types.InlineKeyboardMarkup()
  b1 = types.InlineKeyboardButton('Каталог', callback_data='catalog')
  markup.row(b1)
  b2 = types.InlineKeyboardButton('Информация', callback_data='info')
  b3 = types.InlineKeyboardButton('Помощь', callback_data='help')
  markup.row(b2, b3)
  b4 = types.InlineKeyboardButton('Профиль', callback_data='profil')
  markup.row(b4)
  b5 = types.InlineKeyboardButton('Поддержка', callback_data='support')
  b6 = types.InlineKeyboardButton('Отзывы', callback_data='review')
  markup.row(b5, b6)
  bot.send_message(
      message.chat.id,
      'SkySquad-интернет-магазин информационных/игровых товаров!💻',
      reply_markup=markup)

#Заказы
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(callback):
  if callback.data == 'python':
    chat_id = callback.message.chat.id
    bot.send_message(
        chat_id,
        'Вы выбрали категорию Python | bot. Эта категоия предназначена для создания ботов на Python для telegram или discord.'
    )
    bot.send_message(chat_id, "Введите ваш заказ:")
    bot.register_next_step_handler(callback.message, process_order)
  elif callback.data == 'mounting':
    chat_id = callback.message.chat.id
    bot.send_message(
        chat_id,
        'Вы выбрали категорию Монтаж. Эта категория включает в себя монтаж фото и видео.'
    )
    bot.register_next_step_handler(callback.message, process_order)
  elif callback.data == 'catalog':
    chat_id = callback.message.chat.id
    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Игры', callback_data='games')
    markup.row(b1)
    b2 = types.InlineKeyboardButton('Python | bot', callback_data='python')
    b3 = types.InlineKeyboardButton('Монтаж', callback_data='mounting')
    markup.row(b2, b3)
    bot.send_message(chat_id,
                     "Выбеите пожалуйста категорию услуги!📜",
                     reply_markup=markup)
  elif callback.data == 'done_order':
    chat_id = callback.message.chat.id
    username = callback.from_user.username
    bot.send_message(chat_id, "Отчёт о заказе отправлен глав. администратору!")
    for admin_id in owners:
      bot.send_message(
          admin_id,
          f"Запрос выполнен!\nОператор: @{username}\nЗапрос: {orders[chat_id]}\nЦена: {price[chat_id]}\n "
      )
  elif callback.data == 'done_help':
    chat_id = callback.message.chat.id
    username = callback.from_user.username
    bot.send_message(chat_id, "Отчёт о заказе отправлен глав. администратору!")
    for admin_id in owners:
      bot.send_message(
          admin_id,
          f"Запрос выполнен!\nОператор: @{username}\nЗапрос: {orders[chat_id]}\n "
      )
  elif callback.data == 'info':
    chat_id = callback.message.chat.id
    bot.send_message(
        chat_id,
        "Информация о нас:\nSquadLand-интернет-магазин информационных товаров!\n \nWeb-сайт: squadland.fo.team\nTelegram-канал: https://t.me/squadlandruss"
    )
  elif callback.data == 'help':
    chat_id = callback.message.chat.id
    bot.send_message(chat_id, "Напишите пожалуйста ваш запрос.")
    bot.register_next_step_handler(callback.message, process_help)
  elif callback.data == 'games':
    chat_id = callback.message.chat.id
    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Minecraft', callback_data='minecraft')
    b2 = types.InlineKeyboardButton('Standoff 2', callback_data='standoff')
    markup.row(b1, b2)
    bot.send_message(chat_id,
                     "Вы выбрали категорию игровой услуги.🎮",
                     reply_markup=markup)
  elif callback.data == 'standoff':
    chat_id = callback.message.chat.id
    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Купить голду💰', callback_data='buy_gold')
    b2 = types.InlineKeyboardButton('Калькулятор',
                                    callback_data='calculator_gold')
    markup.row(b1, b2)
    bot.send_message(chat_id,
                     "Мы предоствляем голду в игре Standoff 2!💰",
                     reply_markup=markup)
  elif callback.data == 'buy_gold':
    chat_id = callback.message.chat.id
    bot.send_message(chat_id, "Введите количество голды.💰")
    bot.register_next_step_handler(callback.message, process_gold)
  elif callback.data == 'calculator_gold':
    chat_id = callback.message.chat.id
    bot.send_message(chat_id, "Введите количество голды.💰")
    bot.register_next_step_handler(callback.message, process_calculator_gold)
  elif callback.data == 'done_gold':
    chat_id = callback.message.chat.id
    username = callback.from_user.username
    bot.send_message(chat_id, "Отчёт о заказе отправлен глав. администратору!")
    for admin_id in owners:
      bot.send_message(
          admin_id,
          f"Запрос выполнен!\nОператор: @{username}\nГолды: {golds[chat_id]}\nЦена: {golds[chat_id] * price_gold} ₽\n "
      )
  elif callback.data == 'minecraft':
    chat_id = callback.message.chat.id
    bot.send_message(chat_id, "В данной категории пока что нету товаров. :(")
  elif callback.data == 'review':
    chat_id = callback.message.chat.id
    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Отзывы',
                                    url='https://t.me/+iVqDsaTC20wwODFi')
    b2 = types.InlineKeyboardButton('написать отзыв',
                                    callback_data='review_write')
    markup.row(b1, b2)
    bot.send_message(chat_id,
                     "Вы можете прочитать отзывы нашего магазина!",
                     reply_markup=markup)
  elif callback.data == 'review_write':
    chat_id = callback.message.chat.id
    bot.send_message(chat_id, "Введите ваш отзыв.")
    bot.register_next_step_handler(callback.message, send_reviews)

# Обработка заказа
def process_order(message):
  chat_id = message.chat.id
  order = message.text
  orders[chat_id] = order
  bot.send_message(chat_id, "Введите цену заказа:")
  bot.register_next_step_handler(message, process_price)


# Обработка цены заказа
def process_price(message):
  chat_id = message.chat.id
  markup = types.InlineKeyboardMarkup()
  b1 = types.InlineKeyboardButton(
      'Оплата',
      web_app=WebAppInfo(
          url='https://www.tinkoff.ru/rm/okishev.maksim15/JbPyG41200'))
  markup.row(b1)
  try:
    price[chat_id] = float(message.text)
    send_order_to_admins(chat_id)
    bot.send_message(chat_id,
                     "Ваш заказ и цена успешно отправлены.",
                     reply_markup=markup)
  except ValueError:
    bot.send_message(
        chat_id,
        "Пожалуйста, введите корректное числовое значение для цены.",
        reply_markup=markup)
    bot.register_next_step_handler(message, process_price)


# Отправка заказа администраторам
def send_order_to_admins(chat_id):
  markup = types.InlineKeyboardMarkup()
  b1 = types.InlineKeyboardButton('Готово', callback_data='done_order')
  markup.row(b1)
  username = bot.get_chat(chat_id).username
  order_message = f"Новый заказ!\nПользователь: @{username}\nЗаказ:{orders[chat_id]}\nЦена: {price.get(chat_id, 'не указана')} ₽\n "
  bot.send_message(
      chat_id,
      "Ваш заказ отправлен!\nПожадуйсьа ожидайте ответа от администратора.")
  for admin_id in admin_ids:
    bot.send_message(admin_id, order_message, reply_markup=markup)


# Обработка запроса на помощь
def process_help(message):
  chat_id = message.chat.id
  markup = types.InlineKeyboardMarkup()
  b1 = types.InlineKeyboardButton('Готово', callback_data='done_help')
  markup.row(b1)
  help_request = message.text
  username = bot.get_chat(chat_id).username
  help_message = f"Новый запрос на помощь!\nПользователь: @{username}\nЗапрос: {help_request}"
  bot.send_message(
      chat_id,
      "Ваш запрос успешно отправлен.\nМы ответим вам в течении 24 часов.")
  for admin_id in admin_ids:
    bot.send_message(admin_id, help_message, reply_markup=markup)


# Обработка заказа на голду в Standoff 2
def process_gold(message):
  chat_id = message.chat.id
  gold = int(message.text)
  golds[chat_id] = gold
  username = bot.get_chat(chat_id).username
  markup = types.InlineKeyboardMarkup()
  b1 = types.InlineKeyboardButton('Готово', callback_data='done_gold')
  markup.row(b1)
  markup2 = types.InlineKeyboardMarkup()
  b2 = types.InlineKeyboardButton(
      'Оплата',
      web_app=WebAppInfo(
          url='https://www.tinkoff.ru/rm/okishev.maksim15/JbPyG41200'))
  markup2.row(b2)
  gold_user = f"Ваш заказ на голду!\nКолличество голды: {gold}\nЦена: {gold * price_gold} ₽\n "
  gold_message = f"Новый заказ на голду!\nПользователь: @{username}\nКолличество голды: {gold}\nЦена: {gold * price_gold} ₽\n "
  bot.send_message(
      chat_id,
      "Ваш заказ отправлен!\nПожадуйсьа ожидайте ответа от администратора.")
  bot.send_message(chat_id, gold_user, reply_markup=markup2)
  for admin_id in admin_ids:
    bot.send_message(admin_id, gold_message, reply_markup=markup)


# Калькулятор голды в Standoff 2


def process_calculator_gold(message):
  chat_id = message.chat.id
  try:
    gold = int(message.text)
    bot.send_message(chat_id,
                     f"Цена за {gold} голды составляет {gold*price_gold} ₽")
  except ValueError:
    bot.send_message(
        chat_id, "Пожалуйста, введите корректное числовое значение для голды.")
    bot.register_next_step_handler(message, process_calculator_gold)


@bot.message_handler(content_types=['text'])
def handle_text(message):
  if message.from_user.id in admin_ids:
    # Если сообщение отправлено администратором, пересылаем его пользователю
    for user_id in admin_ids:
      if user_id != message.from_user.id:
        bot.send_message(
            user_id,
            f"Администратор {message.from_user.first_name} ({message.from_user.id}): {message.text}"
        )
  else:
    # Если сообщение отправлено пользователем, пересылаем его администраторам
    for admin_id in admin_ids:
      bot.send_message(
          admin_id,
          f"Пользователь {message.from_user.first_name} (@{message.from_user.username}): {message.text}"
      )


def send_reviews(message):
  review = message.text
  bot.send_message(chat_reviews, review)
  bot.send_message(message.chat.id, "Спасибо за отзыв!")


def profil(message):
  bot.send_message(
      callback.message.chat.id,
      f"Ваш профиль:\n \nИмя: {callback.from_user.username}\nID: {callback.from_user.id}\n \nРеферальная система\n \nСсылка: https://t.me/{botname}?start={callback.from_user.id}\nРеферылов: "
  )


bot.polling()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# создаю статичную reply клавитатуры
button_weather = KeyboardButton(text='Получить прогноз!')
button_help = KeyboardButton(text='Помогите...')
button_restart = KeyboardButton(text='Перезапустить')

reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_weather], [button_help], [button_restart]],
    resize_keyboard=True
)

# создаю инлайн клавиатуру для выбора кол-ва дней прогноза
button_1_day = InlineKeyboardButton(text='1 День', callback_data='1')
button_3_days = InlineKeyboardButton(text='3 Дня', callback_data='3')
button_5_days = InlineKeyboardButton(text='5 Дней', callback_data='5')

inline_keyboard_cnt_days = InlineKeyboardMarkup(
    inline_keyboard=[[button_1_day], [button_3_days], [button_5_days]]
)

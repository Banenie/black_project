from aiogram import Bot, Dispatcher, types, F
import logging
import asyncio

from API_TOKEN import API_TOKEN

from markups import reply_keyboard, inline_keyboard_cnt_days

from from_server import weather_from_server

from graph_making import graph_making

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Создаём бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# словарь для хранения информации о пользователе (когда заново запускашь бота надо прописать команду /start, чтобы сохранилась айдишка)
dict_of_users = {}


### --- ОБРАБОТЧИК start и кнопки Перезапустить ---
@dp.message(F.text.in_(['/start', 'Перезапустить']))
async def start_command(message: types.Message):
    dict_of_users[f'{message.chat.id}'] = False

    text = 'Добро пожаловать в бота, который поможет тебе узнать погоду на предстоящее путешествие!\n'\
        'Вот все команды, которые помогут тебе пользоваться ботом:\n'\
        '/start - перезапускает бота, если что-то пошло не так\n'\
        '/help - помогает тебе вспомнить все команды\n'\
        '/weather - узнает погоду на твое путешествие\n'\
        'Также они продублированы у тебя на клавиатуре\n'\
        'Желаем приятного пользовательского опыта)'

    await message.answer(
        text, 
        reply_markup=reply_keyboard
    )


### --- ОБРАБОТЧИК help и кнопки Помогите ---
@dp.message(F.text.in_(['/help', 'Помогите...']))
async def help_command(message: types.Message):
    text = 'Рад помочь!\n'\
        'Вот все мои команды:\n'\
        '/start - перезапускает бота, если что-то пошло не так\n'\
        '/help - помогает тебе вспомнить все команды\n'\
        '/weather - узнает погоду на твое путешествие\n'\
        'Также они продублированы у тебя на клавиатуре'

    await message.answer(text)


### --- ОБРАБОТЧИК weather и кнопки Получить прогноз! ---
@dp.message(F.text.in_(['/weather', 'Получить прогноз!']))
async def help_command(message: types.Message):
    text = 'Введите через пробел все города, в которых хотите побывать (включая город отправления)'

    dict_of_users[f'{message.chat.id}'] = True

    await message.answer(text)


### --- НЕОБРАБОТАННЫЕ СООБЩЕНИЯ + Прием городов, если флаг ---
@dp.message()
async def handle_message(message: types.Message):
    if dict_of_users[f'{message.chat.id}'] == True:
        dict_of_users[f'{message.chat.id}'] = False

        dict_of_users[f'{message.chat.id}_cities'] = message.text

        text = 'Отлично, теперь выбери на сколько дней прогноз тебе нужен?'

        await message.answer(text, reply_markup=inline_keyboard_cnt_days)

    else:
        await message.answer('Извините, я не понял ваш запрос. Попробуйте использовать команды или кнопки.')


### --- CALLBACK-ЗАПРОСЫ ---
@dp.callback_query(F.data.in_(['1', '3', '5']))
async def vote_callback(callback: types.CallbackQuery):
    #удаляю сообщение с инлайн клавиатурой, чтобы нельяз было на нее нажимать
    await callback.message.delete()
    cnt_days = int(callback.data)

    cities = dict_of_users[f'{callback.message.chat.id}_cities'].split(' ')

    if len(cities) <= 1:
        text = 'Вы ввели недостаточное количество городов, попробуйте снова (введите команду /weather или получите прогноз кнопкой)'
        await callback.message.answer(text)
        return

    # читаю данные с сервера
    try:
        weather_data = []
        verdicts = []
        for city in cities:
            data = weather_from_server(city)

            if data['weather_data'][0]['Humidity'] == -1:
                text = 'Что-то не так с сервером или вы неверно ввели город, попробуйте снова (введите команду /weather или получите прогноз кнопкой)'
                await callback.message.answer(text)
                return 
            
            weather_data.append(data['weather_data'])
            verdicts.append(data['verdict'])

    except Exception as e:
        print(e)
        text = 'Что-то не так с сервером, попробуйте снова (введите команду /weather или получите прогноз кнопкой)'
        await callback.message.answer(text)
        return 

    # выношу финальный вывод о поездке
    if all(verdict == 'Погода блеск, катись куда хочешь!' for verdict in verdicts):
        verdict = 'Погода блеск, катись куда хочешь!'
    else:
        verdict = 'Тебе следует остаться дома'
    

    # создаю большое сообщение со всеми прогнозами
    text = f'Вот ваш {cnt_days} дневный прогноз!\n'\
        f'Бот считает, что "{verdict}"\n\n'
    
    for city in range(len(cities)):
        text += f'**{cities[city]}**\n'
        for day in range(cnt_days):
            text += f'      День {day + 1}\n'
            for metric, value in weather_data[city][day].items():
                text += f'          {metric}: {value}\n'
        text += '\n'
    
    await callback.message.answer(text)

    # Далее отправка графиков
    text = 'Вот тебе еще немного графиков'

    graph_making(weather_data, cities, cnt_days, callback.message.chat.id)

    group = []
    for metric in ['Temperature', 'WindSpeed', 'RainProbability', 'Humidity']:
        group.append(types.InputMediaPhoto(media=types.FSInputFile(f'graphs/{callback.message.chat.id}_{metric}.png', 'rb')))
    
    await callback.message.answer(text)
    await callback.message.answer_media_group(group)

    # финальное сообщение с инструкциями
    text = 'Спасибо, что пользуешься нашим ботом) Чтобы получить прогноз снова введи команду /weather или получи прогноз кнопкой'
    await callback.message.answer(text)


### --- ЗАПУСК БОТА ---
if __name__ == '__main__':
    async def main():
        # Запускаем polling
        await dp.start_polling(bot)

    asyncio.run(main())

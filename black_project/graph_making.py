import datetime

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


# функция создает графики с помощью seaborn, также сохраняет графики в папку graphs
def graph_making(weather_data, cities, cnt_days, chat_id):
    today = datetime.datetime.now().date()

    # тут создается удобный датафрейм (еще с красного проекта)
    df = pd.DataFrame({
        'City': cities * int(cnt_days),
        'Day': [today + datetime.timedelta(i // len(cities)) for i in range(len(cities) * int(cnt_days))],
        'Temperature': [i[idx // len(cities)]['Temperature'] for idx, i in enumerate(weather_data * int(cnt_days))],
        'WindSpeed': [i[idx // len(cities)]['WindSpeed'] for idx, i in enumerate(weather_data * int(cnt_days))],
        'RainProbability': [i[idx // len(cities)]['RainProbability'] for idx, i in enumerate(weather_data * int(cnt_days))],
        'Humidity': [i[idx // len(cities)]['Humidity'] for idx, i in enumerate(weather_data * int(cnt_days))]
    })

    # создаю сами графики и сохраняю
    for metric in ['Temperature', 'WindSpeed', 'RainProbability', 'Humidity']:
        sns.lineplot(df, x='Day', y=metric, hue='City')
        plt.xticks([today + datetime.timedelta(i) for i in range(int(cnt_days))])
        plt.savefig(f'graphs/{chat_id}_{metric}.png')
        plt.clf()


        # px.line(df, 'Day', metric, color='City').update_layout(xaxis={
        #                 'tickmode': 'array',
        #                 'tickvals': [today + datetime.timedelta(i) for i in range(int(cnt_days))],
        #                 'ticktext': [str(today + datetime.timedelta(i)) for i in range(int(cnt_days))]
        #             }).write_image(file=f'graphs/{chat_id}_{metric}.png', engine='orca', width=10)
        # не работает(

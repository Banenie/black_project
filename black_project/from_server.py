import requests

# Отправляем GET-запрос
def weather_from_server(city):
    data = {'city': city}
    
    try:
        r = requests.get('http://127.0.0.1:8050/api', params=data)
    except requests.ConnectionError:
        print('Не удается получить доступ к серверу')
    except requests.Timeout:
        print('Сервер слишком долго отвечает')
    except Exception as e:
        print(e)
        
    return r.json()

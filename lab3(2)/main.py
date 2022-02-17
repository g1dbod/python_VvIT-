import requests

s_city = "Moscow,RU"
appid = "6c12efc7fc1c5f2979b1ba1e784341c3"

res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                    params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()

print("Город:", s_city)
print("Погодные условия:", data['weather'][0]['description'])
print("Температура:", data['main']['temp'])
print("Минимальная температура:", data['main']['temp_min'])
print("Максимальная температура", data['main']['temp_max'])
print("Скорость ветра: ", data['wind']['speed'])
print("Видимость: ", data['visibility'])

res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                    params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("\nПрогноз погоды на неделю:")
for i in data['list']:
    print(f"Дата < {i['dt_txt']} >\n"
          f"Темпиратура< {i['main']['temp']} >\n"
          f"Погодные условия < {i['weather'][0]['description']} >\n"
          f"Скорость ветра < {i['wind']['speed']} >\n"
          f"Видимость < {i['visibility']} >")
    print("____________________________")


import random
import pyowm
import requests

import vk_api
from pyowm.exceptions.api_response_error import NotFoundError
from vk_api.longpoll import VkLongPoll, VkEventType

def write_msg(user_id, message):
    vk.method('messages.send', {'peer_id': user_id, 'message': message, 'random_id': int(random.random()*1000000) })


# API-ключ созданный ранее
token = "токен"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            if event.text == "Minecraft" or event.text == "minecraft":
                res = requests.get("https://api.mcsrvstat.us/2/178.57.30.163:25565")
                data = res.json()
                print(data)
                if data['online']:
                    write_msg(event.user_id, "На сервере " + str(data['ip']) + ":" + str(data['port']) + " онлайн " + str(data['players']['online']) + " человек:")
                    players = ""
                    for name in data['players']['list']:
                        players += name + ", "
                    write_msg(event.user_id, players)
                else:
                    write_msg(event.user_id, "Сервер сейчас выключен")
            else:
                owm = pyowm.OWM('9fcfddae77f7d9ad006b4206eac0ffa6')
                place = event.text
                try:
                    observation = owm.weather_at_place(place)
                    w = observation.get_weather()

                    temp = w.get_temperature('celsius')["temp"]

                    write_msg(event.user_id, "В городе " + place + " Сейчас " + w.get_detailed_status())
                    write_msg(event.user_id, "Температура сейчас в районе " + str(temp))

                    print("В городе " + place + " Сейчас " + w.get_detailed_status())
                    print("Температура сейчас в районе " + str(temp))

                    if temp < 10:
                        write_msg(event.user_id, "Сейчас копэц холодно ")
                    elif temp < 20:
                        write_msg(event.user_id, "Сейчас довольно холодно, одевайся потеплей ")
                except NotFoundError:
                        write_msg(event.user_id, "Географию в школе учить надо")

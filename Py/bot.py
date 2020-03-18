import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
from bot_token import get_token
from vk_api import VkUpload
vk_session = vk_api.VkApi(token=get_token())
vk = vk_session.get_api()
upload = VkUpload(vk_session)
longpoll = VkLongPoll(vk_session)
keyboard_st = []
buttons_dict = {
    'Кнопочки': {'Актив': 'positive', 'Заявки': 'negative', 'add_line': '', 'Статус аккаунта': 'negative',
                 'HELP': 'positive'},
    'Актив': {'Общага': 'primary', 'Институт': 'negative', 'add_line': '', 'Назад': 'default'},
    'Общага': {'Участие': 'primary', 'add_line': '', 'Назад': 'default'},
    'Участие': {'1 мероприяятие': 'positive', '2 мероприятие': 'positive',
                '3 мероприятие': 'positive', '4 мероприятие': 'positive', 'add_line': '',
                'К общаге': 'default', 'Вперёд по листу': 'default'},
    'Институт': {'НПП': 'negative', 'Назад': 'default'},
    'НПП': {'Информация': 'primary', 'Прошедшие мероприятия': 'primary', 'Участие': 'primary',
            'add_line': '', 'Назад': 'default'}
    }


# Отправка клавиатуры
def send_k(keyboard, message):
    vk.message.send(
        user_id=event.user_id,
        message=message,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )


# Загрузка кнопок клавиатуры
def keyboard_down(keyboards):
    keyboard = VkKeyboard()
    for key in keyboards:
        # Если попался триггер 'add_line' создаём новую строчку,на которой можно размещать кнопки
        if key == 'add_line':
            keyboard.add_line()
        else:
            keyboard.add_button(key, keyboards[key])
    return keyboard


# Создание новой клавиатуры
def create_new_keyboard(name):
    keyboard = keyboard_down(buttons_dict[name])
    keyboard_st.append(keyboard)
    send_k(keyboard, name)


# Возвращение на предыдущую клавиатуру
def back():
    keyboard_st.pop()
    return keyboard_st[-1]


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request in buttons_dict:
                create_new_keyboard(request)
            elif request == 'Назад' or request == 'К общаге':
                back()

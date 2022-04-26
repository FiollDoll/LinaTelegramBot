import random
import time
import pandas as pd
import telebot

###
# Версия 0.4
# Прототип переделан 19.04.22
# Задачи:
###

# Токен
bot = telebot.TeleBot('')

newTexts = False  # Создание нового слова


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if newTexts != True:  # если не равно тру, то просто разговор
        talk(message)
    else:  # если равно тру - то записываем слово
        Test(message)


# Разговор
def talk(message):
    while True:  # Чтобы работало даже после ввода
        global df
        global word
        word = message.text.lower()
        replacer()
        df = pd.DataFrame({
            "word": word,
        }, index=[0])

        file = open("Lina.csv", "r", encoding="utf-8")  # Поиск отправленного слова
        filelines = file.readlines()  # Чтение строк
        # Условие - есть в файле строка или нет
        for fileline in filelines:  # Ищем в каждой строке
            if word in fileline.strip('\n').split(','):
                fileQuestion = open(f"question/{word.lower()}.csv", "r", encoding="utf-8")  # открываем ответы
                total = random.choice(fileQuestion.readlines())  # Ответ от бота
                bot.send_message(message.chat.id, total)  # Отправляем ответ
                time.sleep(1)
                break  # Окончить цикл поиска
        # Если нету строки
        else:
            global newTexts
            bot.send_message(message.chat.id, "Как мне отвечать на это?")
            newTexts = True
            break
        break


# Начало
def Test(message):
    global newTexts
    global word
    replacer()
    df.to_csv("Lina.csv", mode="a", index=False, header=False)  # Добавление в pd
    question = message.text  # Как отвечать
    newTexts = False  # Конец
    fileQuestion = open(f"question/{word.lower()}.csv", "a", encoding="utf-8")  # Ответы
    fileQuestion.write(question)
    fileQuestion.close()


def replacer():
    global word
    print(word)
    word = word.replace(" ", "_")  # Пробел
    word = word.replace("?", "")
    word = word.replace('"', "")
    word = word.replace("!", "")
    word = word.replace(",", "")
    print(word)


while True:
    bot.polling(none_stop=True)

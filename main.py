import telebot
import json

Token = "6653545667:AAFi0ShzkqFDINwGBcPMVAqTSgCgOds4Ds0"
bot = telebot.TeleBot(Token)
try:
    with open("user_data.json", "r", encoding="utf-8") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}

  
@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это твой бот.Скоро я буду крутым!")
  
@bot.message_handler(commands=["learn"])
def handle_learn(message):
    try:
        user_words = user_data.get(str(message.chat.id),{})
        words_number = int(message.text.split()[1])
    except ValueError:
        bot.send_message(message.chat.id, "Используйте функцию /learn чтобы учиться")
    except IndexError:
        bot.send_message(message.chat.id, "Используйте функцию /learn чтобы учиться")
        
def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
      word=random.choise(list(user_words.keys()))
      translation = user_words[word]
      bot.send_message(chat_id, f"Напиши перевод слова '{word}'.")

      bot.register_next_step_handler_by_chat_id(chat_id, check_translation)
    
def check_translation(message, expected_translation, words_left):
    user_translation = message.text.strip().lower()
    if user_translation=expected_translation.lower():
        bot.send_message(message.chat.id, "Молодец, всё верно!!!")
    else:
        bot.send_message(message.chat.id, f"Ой, тут ошибка. Вот правильный перевод: {expected_translation}")
    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left)
    
  
@bot.message_handler(commands=["help"])
def handle_help(message):
  bot.send_message(message.chat.id, "Чтобы начать учиться используй команду /learn")

@bot.message_handler(commands=["addword"])
def handle_addword(message):
    global user_data
    chat_id = message.chat.id
    user_dict = user_data.get(chat_id,{})
    try:
        words = message.text.split()[1:]
        if len(words)==2:
          word, translation = words[0].lower(), words[1].lower()
          user_dict[word] = translation
          user_data[chat_id] = user_dict
          with open("user_data.json", "w", encoding="utf-8") as file:
                 json.dump(user_data, file, ensure_ascii=False, indent=4)
          bot.send_message(chat_id, f"Слово '{word}' успешно добавлено!")
        else:
          bot.send_message(chat_id, "Проверьте, что ваше сообщение удовлетворяет форматуЖ Слово - Перевод.")
    except Exception as e:
      bot.send_message(chat_id, "Произошла ошибка при обработке команды. Попробуйте ещё раз.")



@bot.message_handler(func= lambda message: True)
def handle_all(message):
  if message.text.lower() == "как тебя зовут?":
    bot.send_message(message.chat.id, "Я настоящий англичанин Джеймс!")
    
  if message.text.lower() == "как дела?":
    bot.send_message(message.chat.id, "Всё супер, давай учиться!")
    
  if message.text.lower() == "когда отдохнем?":
    bot.send_message(message.chat.id, "Не жалей сил! Скоро перерыв for tea at five o'clock!")


if __name__ == "__main__":
    bot.polling(none_stop=True)

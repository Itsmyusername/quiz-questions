import logging
from random import choice

from environs import Env
from telegram import Update, ReplyKeyboardMarkup, Bot
from telegram.ext import Updater, CallbackContext, MessageHandler, CommandHandler, Filters, ConversationHandler

from quiz_handlers import assemble_questionnaire
from telegram_logging import TelegramLogsHandler

ANSWERING = 0

logger = logging.getLogger()


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = [
        ["Новый вопрос", "Сдаться"],
        ["Мой счёт"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_markdown_v2(
        fr"Привет, {user.mention_markdown_v2()}\! Сыграем в викторину?",
        reply_markup=reply_markup
    )


def send_question(update: Update, context: CallbackContext):
    questionnaire = context.bot_data["questionnaire"]
    question, answer = choice(questionnaire)
    update.message.reply_text(question)
    context.chat_data["current_quiz"] = question, answer

    return ANSWERING


def check_answer(update: Update, context: CallbackContext):
    question, answer = context.chat_data["current_quiz"]
    user_answer = update.message.text
    if user_answer.lower() == answer.split(".", maxsplit=1)[0].lower():
        text = "Вы угадали! Нажмите на \"Новый вопрос\"!"
        update.message.reply_text(text)
        return ConversationHandler.END
    else:
        text = "Неправильно. Попробуйте ещё раз?"
        update.message.reply_text(text)


def give_up(update: Update, context: CallbackContext):
    question, answer = context.chat_data["current_quiz"]
    update.message.reply_text(f"Правильный ответ: {answer}")
    return send_question(update, context)


def main():
    env = Env()
    env.read_env()

    bot_token = env.str("TELEGRAM_BOT_TOKEN")

    logger_bot = Bot(token=env.str("TELEGRAM_LOGGING_BOT_TOKEN"))
    chat_id = env.str("TELEGRAM_USER_ID")

    logger.setLevel(env.str("LOGGING_LEVEL", logging.WARNING))
    logger.addHandler(TelegramLogsHandler(logger_bot, "Telegram Quiz Bot", chat_id))

    logger.info("Telegram bot started")

    updater = Updater(token=bot_token)
    dp = updater.dispatcher
    with open(env.str("QUIZ_FILE_PATH", "QA/example.txt"), encoding="KOI8-R") as file:
        text = file.read()
    dp.bot_data["questionnaire"] = assemble_questionnaire(text)
    dp.update_persistence()
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex(r"^Новый вопрос$"), send_question))
    dp.add_handler(MessageHandler(Filters.regex(r"^Сдаться$"), give_up))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

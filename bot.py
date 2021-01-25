import pyshorteners
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton


INPUT_URL = 0


def start(update, context):

    update.message.reply_text(
        text='Hola, bienvenido, qué deseas hacer?',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Acortar URL', callback_data='url')],
        ])
    )


def qr_command_handler(update, context):

    update.message.reply_text('Envíame el texto para generarte un código QR.')

    return INPUT_URL


def url_callback_handler(update, context):

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Envíame un enlace para acortarlo.'
    )

    return INPUT_URL


def input_url(update, context):

    url = update.message.text
    chat = update.message.chat

    s = pyshorteners.Shortener()
    short = s.chilpit.short(url)

    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )

    chat.send_message(
        text=short
    )

    return ConversationHandler.END


if __name__ == '__main__':

    updater = Updater(token='YOUR_TOKEN', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern='url', callback=url_callback_handler)
        ],

        states={
            INPUT_URL: [MessageHandler(Filters.text, input_url)]
        },

        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()

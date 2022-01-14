from telegram.ext import Updater, CommandHandler

def start(update,context):
    update.message.reply_text ('Hola, humano')


if __name__== '__main__': #la funcion empezaria por aqui
    #updater: para saber las peticiones que va recibiendo el bot de parte del usuario
    updater = Updater(token='5058818013:AAGkn-UNjkngHrVn8fbuQjUmZ145G7YWKBw', use_context=True)#la nueva API de python pide la variable use_context
    #dispatcher: se encarga de nviar las acciones, lo que entra por updater pasa por el dispatcher
    dp=updater.dispatcher
    #add handler: handler es una funcion para ejecutar

    dp.add_handler(CommandHandler('start', start))


    updater.start_polling()# para que el bot se quede en un ciclo infinito escuchando
    updater.idle()


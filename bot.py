import os

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ChatAction
import qrcode
#estados
STATE_0_TEXT2QR=0
#funciones
def start(update,context):

    update.message.reply_text ('Hola, bienvenido al bot para generar Código QR\n\n Use /qr para generar código')

def qr_code_command_handler(update, context):

    update.message.reply_text('Envie el texto que desea cifrar en Código QR')

    return STATE_0_TEXT2QR

def input_text (update,context):

    text=update.message.text
    #print(text)#prueba
    filename=generate_code_qr(text)

    chat=update.message.chat

    send_code_qr(filename,chat)
    return ConversationHandler.END

def generate_code_qr(text):

    filename= text+'.jpg'

    img= qrcode.make(text)

    img.save(filename)#crea el fichero con ese nombre

    return filename

def send_code_qr(filename,chat):

    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )

    chat.send_photo(
        photo=open(filename,'rb')# rb: lectura del archivo
    )

    os.unlink(filename)# eliminar archivo

if __name__== '__main__': #la funcion empezaria por aqui
    #updater: para saber las peticiones que va recibiendo el bot de parte del usuario
    updater = Updater(token='5058818013:AAGkn-UNjkngHrVn8fbuQjUmZ145G7YWKBw', use_context=True)#la nueva API de python pide la variable use_context
    #dispatcher: se encarga de nviar las acciones, lo que entra por updater pasa por el dispatcher
    dp=updater.dispatcher
    #add handler: handler es una funcion para ejecutar

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_code_command_handler)
        ],

        states={
            STATE_0_TEXT2QR: [MessageHandler(Filters.text, input_text)]# filtros de texto, videos, imagenes, input_text es una nueva funcion
        },

        fallbacks=[]

    ))
    #Idea: cuando se presione la tecla flecha arriba ir al historial anterior y permitir su ejecucion


    updater.start_polling()# para que el bot se quede en un ciclo infinito escuchando
    updater.idle()


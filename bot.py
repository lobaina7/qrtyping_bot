import os
#from telegram import MessageEntity
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import qrcode
#estados
STATE_0_TEXT2QR=0
#STATE_0_LINK2QR=0
#funciones
def start(update,context):
#   button1=InlineKeyboardButton (
#          text='Generar QR',#el boton se llama Generar QR
#           callback_data='qr'# y cuando se da clic manda el pattern: qr
#  )
    update.message.reply_text (
        text= 'Hola, bienvenido al bot para generar Código QR\n\n Use /qr para generar código',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton (text='Generar QR', callback_data='qr')]])#el boton se llama Generar QRy cuando se da clic manda el pattern: qr
    )
def qr_code_command_handler(update, context):

    update.message.reply_text('Envie el texto que desea cifrar en Código QR')

    return STATE_0_TEXT2QR

def input_text (update,context):

    text=update.message.text
    #print(text)#prueba
    chat = update.message.chat

   # entities = update.message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.URL, MessageEntity.TEXT_LINK, MessageEntity.HASHTAG])
   # print(entities)

    filename=generate_code_qr(text,chat)

    send_code_qr(filename,chat)
    return ConversationHandler.END

def generate_code_qr(text, chat):

    filename= 'code'+str(chat.id)+'.jpg'# text+'.jpg'

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

# funciones de boton
def qr_callback_handler(update,context):

    query=update.callback_query
    query.answer()#manda una respuesta sin nada
    query.edit_message_text(
        text= 'Envie el texto que desea cifrar en Código QR'
    )
    return STATE_0_TEXT2QR

if __name__== '__main__': #la funcion empezaria por aqui
    #updater: para saber las peticiones que va recibiendo el bot de parte del usuario
    updater = Updater(token='5058818013:AAGkn-UNjkngHrVn8fbuQjUmZ145G7YWKBw', use_context=True)#la nueva API de python pide la variable use_context
    #dispatcher: se encarga de nviar las acciones, lo que entra por updater pasa por el dispatcher
    dp=updater.dispatcher
    #add handler: handler es una funcion para ejecutar

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_code_command_handler), #para comandos /
            CallbackQueryHandler(pattern='qr', callback= qr_callback_handler)# para botones callback
        ],

        states={
            STATE_0_TEXT2QR: [MessageHandler(Filters.text | ( Filters.entity("url") | Filters.entity("text_link") | Filters.entity("hashtag")),
                              input_text)],# filtros de texto, videos, imagenes, input_text es una nueva funcion
        },###probar hastash

        fallbacks=[]

    ))
    #Idea: cuando se presione la tecla flecha arriba ir al historial anterior y permitir su ejecucion


    updater.start_polling()# inicia el bot
    updater.idle()# para que el bot se quede en un ciclo infinito escuchando


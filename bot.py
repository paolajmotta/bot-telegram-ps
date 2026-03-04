import telebot
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

SEU_ID_AFILIADO = "40151652"

def gerar_link_afiliado(link):
    if "?" in link:
        return link + f"&matt_tool={40151652}"
    else:
        return link + f"?matt_tool={40151652}"

@bot.message_handler(func=lambda message: True)
def responder(message):
    if message.text and "mercadolivre.com" in message.text:
        link_afiliado = gerar_link_afiliado(message.text)
        bot.reply_to(message, f"🛍️ Aqui está seu link de afiliada:\n{link_afiliado}")

bot.polling()

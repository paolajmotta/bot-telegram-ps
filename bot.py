import telebot
import os
import re

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

SEU_ID_AFILIADO = "40151652"

def gerar_link_afiliado(link):
    # Remove qualquer matt_tool existente
    link = re.sub(r'matt_tool=\d+', '', link)

    # Remove && ou ?& que possam sobrar
    link = link.replace("&&", "&").replace("?&", "?")

    if "?" in link:
        return link + f"&matt_tool={SEU_ID_AFILIADO}"
    else:
        return link + f"?matt_tool={SEU_ID_AFILIADO}"

@bot.message_handler(func=lambda message: True)
def responder(message):
    if message.text and "mercadolivre.com" in message.text:
        link_afiliado = gerar_link_afiliado(message.text)
        bot.reply_to(message, f"🛍️ Aqui está seu link com possível desconto! :\n{link_afiliado}")

bot.polling()

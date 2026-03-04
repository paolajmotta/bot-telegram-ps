import telebot
import os
import re

TOKEN = "8231233902:AAHmYI4ypaxPALt5hf_0jD56JT8ixxc6QCY"
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

SEU_ID_AFILIADO = "40151652"

def gerar_link_afiliado(link):
    # Remove tudo depois do #
    link = link.split("#")[0]

    # Remove qualquer matt_tool existente
    link = re.sub(r'matt_tool=\d+', '', link)

    # Remove & ou ? sobrando no final
    link = re.sub(r'[&?]+$', '', link)

    # Remove && duplicado
    link = link.replace("&&", "&")

    if "?" in link:
        return link + f"&matt_tool={SEU_ID_AFILIADO}"
    else:
        return link + f"?matt_tool={SEU_ID_AFILIADO}"


@bot.message_handler(func=lambda message: True)
def responder(message):
    if message.text and "mercadolivre.com" in message.text:
        link_afiliado = gerar_link_afiliado(message.text)
        bot.reply_to(
    message,
    f"""🛍️ LINK COM POSSÍVEL DESCONTO LIBERADO!

🔥 Pode estar com oferta ativa
🚚 Veja se tem frete grátis na sua região

👉 {link_afiliado}

Corre antes que o preço mude 👀"""
)

bot.polling()

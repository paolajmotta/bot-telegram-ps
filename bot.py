import telebot
import os
import re
import requests
import threading
import time
import random

# ===== CONFIG =====
TOKEN = os.getenv("TOKEN")
GRUPO_LINKS = -1003875043661
CANAL_OFERTAS = -1003758218142
SEU_ID_AFILIADO = "40151652"

bot = telebot.TeleBot(TOKEN)

# ===== GERAR LINK AFILIADO =====
def gerar_link_afiliado(link):

    url_match = re.search(r'https?://[^\s]+', link)
    if not url_match:
        return None

    link = url_match.group(0)
    link = link.split("#")[0]
    link = re.sub(r'matt_tool=\d+', '', link)
    link = re.sub(r'[&?]+$', '', link)
    link = link.replace("&&", "&")

    if "?" in link:
        return f"{link}&matt_tool={SEU_ID_AFILIADO}"
    else:
        return f"{link}?matt_tool={SEU_ID_AFILIADO}"

# ===== RESPONDER LINKS NO GRUPO =====
@bot.message_handler(func=lambda message: True)
def responder(message):

    chat_id = message.chat.id

    if chat_id == GRUPO_LINKS:
        if message.text and ("mercadolivre.com" in message.text or "meli.la" in message.text):

            link_afiliado = gerar_link_afiliado(message.text)

            if link_afiliado:
                try:
                    bot.delete_message(chat_id, message.message_id)
                except:
                    pass

                bot.send_message(
                    chat_id,
                    f"""🛍️ LINK COM POSSÍVEL DESCONTO!

👉 {link_afiliado}"""
                )

# ===== OFERTAS AUTOMÁTICAS =====
produtos_enviados = set()

def buscar_ofertas():

    url = "https://api.mercadolibre.com/sites/MLB/search?sort=price_asc&limit=20"

    try:
        response = requests.get(url)
        dados = response.json()
        produtos = dados.get("results", [])

        ofertas_validas = [
            p for p in produtos if p["id"] not in produtos_enviados
        ]

        if not ofertas_validas:
            return

        produto = random.choice(ofertas_validas)
        produtos_enviados.add(produto["id"])

        titulo = produto["title"]
        preco = produto["price"]
        link = produto["permalink"] + f"?matt_tool={SEU_ID_AFILIADO}"

        mensagem = f"""🔥 OFERTA 24H

{titulo}

💰 R${preco}

👉 {link}
"""

        bot.send_message(CANAL_OFERTAS, mensagem)

    except Exception as e:
        print("Erro:", e)

def postar_automatico():
    while True:
        buscar_ofertas()
        time.sleep(1800)

threading.Thread(target=postar_automatico).start()

bot.polling(none_stop=True)

print("BOT INICIADO")
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

    if message.chat.id == GRUPO_LINKS:
        if message.text and ("mercadolivre.com" in message.text or "meli.la" in message.text):

            link_afiliado = gerar_link_afiliado(message.text)

            if link_afiliado:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except:
                    pass

                bot.send_message(
                    message.chat.id,
                    f"""🛍️ LINK COM POSSÍVEL DESCONTO!

👉 {link_afiliado}"""
                )

# ===== OFERTAS AUTOMÁTICAS =====
produtos_enviados = set()

def buscar_ofertas():

    url = "https://api.mercadolibre.com/sites/MLB/search?q=desconto&sort=discount_percentage&limit=20"

    try:
        response = requests.get(url, timeout=10)
        dados = response.json()
        produtos = dados.get("results", [])

        ofertas_validas = [
            p for p in produtos
            if p["id"] not in produtos_enviados
            and p.get("original_price")  # garante que tem desconto real
        ]

        if not ofertas_validas:
            return

        produto = random.choice(ofertas_validas)
        produtos_enviados.add(produto["id"])

        titulo = produto["title"]
        preco = produto["price"]
        preco_antigo = produto.get("original_price")
        link = f'{produto["permalink"]}?matt_tool={SEU_ID_AFILIADO}'

        mensagem = f"""🔥 OFERTA 24H

{titulo}

💰 De: R${preco_antigo}
🔥 Por: R${preco}

👉 {link}
"""

        bot.send_message(CANAL_OFERTAS, mensagem)

    except Exception as e:
        print("Erro ao buscar oferta:", e)

def postar_automatico():
    while True:
        buscar_ofertas()
        time.sleep(10)  # 30 minutos

thread = threading.Thread(target=postar_automatico)
thread.daemon = True
thread.start()

bot.polling(none_stop=True)

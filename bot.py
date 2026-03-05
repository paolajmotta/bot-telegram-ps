import telebot
import os
import re
import requests
import threading
import time
import random

# ===== CONFIG =====
set ML_ACCESS_TOKEN=030423-8d65c87288APP_USR-1467792281449758-6443731d3fbf0ca3877e4e-554817674
ML_ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")

headers_ml = {
    "Authorization": f"Bearer {ML_ACCESS_TOKEN}"
}
TOKEN = os.getenv("TOKEN")
GRUPO_LINKS = -1003875043661
CANAL_OFERTAS = -1003758218142
SEU_ID_AFILIADO = "40151652"
set ML_ACCESS_TOKEN=SEU_ACCESS_TOKEN

bot = telebot.TeleBot(TOKEN)

print("BOT INICIANDO...")

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

    print("Buscando ofertas...")

    url = "https://api.mercadolibre.com/sites/MLB/search?q=desconto&sort=discount_percentage&limit=20"

    try:
        response = requests.get(url, headers=headers_ml, timeout=10)

        print("Status API:", response.status_code)

        if response.status_code != 200:
            print("Erro na API")
            print(response.text)
            return

        dados = response.json()
        produtos = dados.get("results", [])

        ofertas_validas = [
            p for p in produtos
            if p.get("original_price")
            and p["id"] not in produtos_enviados
            and p["original_price"] > p["price"]
        ]

        if not ofertas_validas:
            return

        produto = random.choice(ofertas_validas)
        produtos_enviados.add(produto["id"])

        titulo = produto["title"]
        preco = produto["price"]
        preco_antigo = produto["original_price"]
        link = f'{produto["permalink"]}?matt_tool={SEU_ID_AFILIADO}'

        mensagem = f"""🔥 OFERTA 24H

{titulo}

💰 De: R${preco_antigo}
🔥 Por: R${preco}

👉 {link}
"""

        bot.send_message(CANAL_OFERTAS, mensagem)
        print("Oferta enviada")

    except Exception as e:
        print("Erro:", e)
def postar_automatico():
    while True:
        buscar_ofertas()
        time.sleep(30)  # 30 segundos para teste (depois você pode aumentar)

# ===== MENSAGEM INICIAL =====
def mensagem_inicial():
    time.sleep(5)
    try:
        bot.send_message(CANAL_OFERTAS, "Canal online e pronto para ofertas")
        print("Mensagem inicial enviada")
    except Exception as e:
        print("Erro ao enviar mensagem inicial:", e)

# ===== INICIAR THREADS =====
threading.Thread(target=postar_automatico, daemon=True).start()
threading.Thread(target=mensagem_inicial, daemon=True).start()

print("BOT INICIADO")

# ===== INICIAR POLLING =====
bot.polling(none_stop=True)

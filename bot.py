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
        response = requests.get(url, timeout=10)
        print("Status API:", response.status_code)

        if response.status_code != 200:
            print("Erro na API")
            return

        dados = response.json()
        produtos = dados.get("results", [])

        print("Produtos encontrados:", len(produtos))

        ofertas_validas = [
            p for p in produtos
            if p.get("original_price")
            and p["id"] not in produtos_enviados
            and p["original_price"] > p["price"]
        ]

        print("Ofertas válidas:", len(ofertas_validas))

        if not ofertas_validas:
            print("Nenhuma oferta válida encontrada")
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
        print("Oferta enviada com sucesso")

    except Exception as e:
        print("Erro ao buscar oferta:", e)

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

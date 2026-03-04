import telebot
import os
import re

# ===== CONFIGURAÇÕES =====
TOKEN = os.getenv("TOKEN")  # Defina na Railway
GRUPO_LINKS = -100XXXXXXXXXX  # COLOQUE AQUI O ID DO GRUPO
SEU_ID_AFILIADO = "40151652"

bot = telebot.TeleBot(TOKEN)


# ===== FUNÇÃO PARA GERAR LINK AFILIADO =====
def gerar_link_afiliado(link):

    # Pega apenas a URL se vier texto junto
    url_match = re.search(r'https?://[^\s]+', link)
    if not url_match:
        return None

    link = url_match.group(0)

    # Remove fragmento (#...)
    link = link.split("#")[0]

    # Remove matt_tool existente
    link = re.sub(r'matt_tool=\d+', '', link)

    # Remove & ou ? sobrando no final
    link = re.sub(r'[&?]+$', '', link)

    # Remove && duplicado
    link = link.replace("&&", "&")

    # Adiciona seu ID afiliado
    if "?" in link:
        return f"{link}&matt_tool={SEU_ID_AFILIADO}"
    else:
        return f"{link}?matt_tool={SEU_ID_AFILIADO}"


# ===== HANDLER PRINCIPAL =====
@bot.message_handler(func=lambda message: True)
def responder(message):

    chat_id = message.chat.id

    # Só funciona no grupo definido
    if chat_id != GRUPO_LINKS:
        return

    if message.text and (
        "mercadolivre.com" in message.text or
        "meli.la" in message.text
    ):

        link_afiliado = gerar_link_afiliado(message.text)

        if link_afiliado:
            try:
                # Apaga mensagem original
                bot.delete_message(chat_id, message.message_id)
            except:
                pass  # Caso não tenha permissão

            bot.send_message(
                chat_id,
                f"""🛍️ LINK COM POSSÍVEL DESCONTO LIBERADO!

🔥 Pode estar com oferta ativa
🚚 Veja se tem frete grátis na sua região

👉 {link_afiliado}

Corre antes que o preço mude 👀"""
            )


# ===== LOOP =====
bot.polling(none_stop=True)

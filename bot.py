
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# CoinGecko fiyat API
def get_price(symbol):
    symbol = symbol.lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if symbol in data:
            return f"💰 {symbol.upper()} fiyatı: ${data[symbol]['usd']}"
        else:
            return f"❌ '{symbol}' için fiyat bilgisi bulunamadı."
    return "⚠️ API hatası!"

# Binance linki
def get_binance_link(symbol):
    sym = symbol.upper()
    return f"https://www.binance.com/en/trade/{sym}_USDT?ref=CPA_00DKIURIG5"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Merhaba! Ben HangiKripto Bot.\n\n"
        "💱 Fiyat öğrenmek için: /price bitcoin\n"
        "🛒 Nereden alabileceğini öğrenmek için: /where bitcoin\n"
        "Binance affiliate desteklidir."
    )

# /price komutu
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Lütfen coin ID'si girin. Örnek: /price bitcoin")
        return
    symbol = context.args[0]
    result = get_price(symbol)
    await update.message.reply_text(result)

# /where komutu
async def where(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Lütfen coin ID'si girin. Örnek: /where bitcoin")
        return
    symbol = context.args[0]
    link = get_binance_link(symbol)
    await update.message.reply_text(
        f"🔍 {symbol.upper()} şu anda Binance'te işlem görüyor:\n{link}"
    )

# Botu çalıştır
if __name__ == "__main__":
    app = ApplicationBuilder().token("7923386605:AAG7S8h3kb1Wt3UEWhhcb0NIfjPERPjxqhg").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("where", where))

    print("🤖 Bot çalışıyor: HangiKripto")
    app.run_polling()

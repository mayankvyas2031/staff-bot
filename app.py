import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

print("Loading Google Sheet...")

url = "https://docs.google.com/spreadsheets/d/1za1-tM5Bq2VSpYRaznRSZDyaMrzjzImBY57fbp_RQSY/export?format=csv"

data = pd.read_csv(url)
data.columns = data.columns.str.lower()

print("Data loaded successfully")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip().lower()

    result = data[
        data['name'].str.lower().str.contains(query, na=False) |
        (data['id'].astype(str) == query)
    ]

    if not result.empty:
        row = result.iloc[0]

        reply = f"""Name: {row['name']}
ID: {row['id']}
Designation: {row['designation']}
CLI: {row['cli']}
HQ: {row['hq']}
Mobile: {row['mobile']}"""
    else:
        reply = "No record found."

    await update.message.reply_text(reply)

print("Starting bot...")

app = ApplicationBuilder().token("YOUR_NEW_TOKEN").build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

app.run_polling()
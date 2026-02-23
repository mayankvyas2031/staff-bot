import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Load CSV
data = pd.read_csv("staff.csv")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip().lower()

    result = data[
        data['name'].str.lower().str.contains(query, na=False) |
        (data['id'].astype(str) == query)
    ]

    if not result.empty:
        row = result.iloc[0]
        reply = f"""
Name: {row['name']}
ID: {row['id']}
Designation: {row['designation']}
CLI: {row['cli']}
HQ: {row['hq']}
Mobile: {row['mobile']}
"""
    else:
        reply = "No record found."

    await update.message.reply_text(reply)

app = ApplicationBuilder().token("8794553685:AAGrr8YTykhyXVMUwYh_44YaUDrxF5LiHv8").build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
app.run_polling()

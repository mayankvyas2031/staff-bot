import pandas as pd
import os
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
        reply = (
            f"Name: {row['NAME']}\n"
            f"ID: {row['ID']}\n"
            f"Designation: {row['Designation']}\n"
            f"CLI: {row['NCLI']}\n"
            f"HQ: {row['HQ']}\n"
            f"Mobile: {row['Mobile']}"
        )
    else:
        reply = "No record found."

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.run_polling()

if __name__ == "__main__":
    main()

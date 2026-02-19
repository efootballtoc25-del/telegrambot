import os
from datetime import timedelta, timezone
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ===== CONFIG =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 5015499341  # <-- put your Telegram user ID here

# ===== STATES =====
(
    TODAY_ADD,
    TODAY_DETAIL,
    DETAIL_REMAIN,
    TODAY_RETURN,
    RETURN_REMAIN,
    TODAY_CUT,
    CUT_REMAIN,
    CUT_REASON,
    ACC_OPEN,
    SUPPORT_NAME,
    SUPPORT_AMOUNT
) = range(11)

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Daily Marketing Report\n\nဒီနေ့ဘယ်နှစ်ယောက်အပ်လဲ (နံပါတ်ပဲထည့်):"
    )
    return TODAY_ADD

# ===== CANCEL =====
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END

# ===== NUMERIC INPUT VALIDATION =====
async def numeric_input(update: Update, context: ContextTypes.DEFAULT_TYPE, key: str, next_state: int, prompt: str):
    text = update.message.text.strip()
    try:
        context.user_data[key] = int(text) if key != "support_amount" else float(text)
    except ValueError:
        await update.message.reply_text(f"⚠ နံပါတ်ပဲထည့်ပါ: {prompt}")
        return next_state
    await update.message.reply_text(prompt)
    return next_state

# ===== TODAY ADD HANDLER =====
async def today_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await numeric_input(
        update, context, "today_add", TODAY_DETAIL, "ဒီနေ့ detail ဘယ်နှစ်ယောက်ပြောလဲ (နံပါတ်ပဲထည့်):"
    )

async def today_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await numeric_input(
        update, context, "today_detail", DETAIL_REMAIN, "Detail ဘယ်နှစ်ယောက်ကျန်လဲ ဒီနေ့ (နံပါတ်ပဲထည့်):"
    )

async def detail_remain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await numeric_input(
        update, context, "detail_remain", TODAY_RETURN, "ဒီနေ့ return ဘယ်နှစ်ယောက်ပြန်လဲ (နံပါတ်ပဲထည့်):"
    )

async def today_return(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await numeric_input(
        update, context, "today_return", RETURN_REMAIN, "Return ဘယ်နှစ်ယောက်ကျန်လဲ ဒီနေ့ (နံပါတ်ပဲထည့်):"
    )

async def return_remain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await numeric_input(
        update, context, "return_remain", TODAY_CUT, "ဒီနေ့ဘယ်နှစ်ယောက်ဖြတ်လဲ (နံပါတ်ပဲထည့်):"
    )

async def today_cut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await numeric_input(
        update, context, "today_cut", CUT_REMAIN, "ဘယ်နှစ်ယောက်ဖြတ်ဖို့ကျန်သေးလဲ (နံပါတ်ပဲထည့်):"
    )

async def cut_remain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        cut_remaining = int(text)
        context.user_data["cut_remain"] = cut_remaining
    except ValueError:
        await update.message.reply_text("⚠ နံပါတ်ပဲထည့်ပါ:")
        return CUT_REMAIN

    if cut_remaining > 0:
        await update.message.reply_text(
            "⚠ ဖြတ်ဖို့ကျန်နေသေးတယ် ဘာလို့ကျန်နေသေးတာလဲ.\n"
            "Customer name နဲ့တခါတည်းရေးပါ:"
        )
        return CUT_REASON
    else:
        context.user_data["cut_reason"] = "N/A"
        await update.message.reply_text("ဒီနေ့အကောင့်ပွင့်လား? (Y/N):")
        return ACC_OPEN

# ===== CUT REASON =====
async def cut_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cut_reason"] = update.message.text
    await update.message.reply_text("ဒီနေ့အကောင့်ပွင့်လား? (Y/N):")
    return ACC_OPEN

# ===== ACC OPEN =====
async def acc_open(update: Update, context: ContextTypes.DEFAULT_TYPE):
    acc_value = update.message.text.strip().upper()
    context.user_data["acc_open"] = acc_value
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "No Username"

    # Myanmar Time (UTC+06:30)
    myanmar_timezone = timezone(timedelta(hours=6, minutes=30))
    context.user_data["formatted_time"] = update.message.date.astimezone(myanmar_timezone).strftime("%Y-%m-%d %H:%M:%S")

    # Warn if remaining details or returns exist
    if int(context.user_data.get("detail_remain", 0)) > 0 or int(context.user_data.get("return_remain", 0)) > 0:
        await update.message.reply_text(
            f"⚠ ကျန်နေသေးတဲ့ကောင်များ:\n"
            f"Detail: {context.user_data.get('detail_remain')}\n"
            f"Return: {context.user_data.get('return_remain')}"
        )

    if acc_value == "Y":
        gif_url = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHdvemFveGtzZTUxcWRsZ2J2eXRpMnQ4bGc0Z2E4azc3bW9mZGtwcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1JTy9isIm0u0OqePP1/giphy.gif"
        await update.message.reply_animation(animation=gif_url, caption="🎉 အကောင့်ပွင့်သွားပြီ!")
        await update.message.reply_text("ရှာပေးတဲ့ support နာမည်ပြောပါ:")
        return SUPPORT_NAME
    else:
        gif_noacc = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExenY5MWl5djlidTl2b3U3aDQ1ZDVsYmdlbnJoMmYzN2h0eWNrM3o0bSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tZJagIk8GhR1NLNl7w/giphy.gif"
        await update.message.reply_animation(animation=gif_noacc, caption="အကောင့်မပွင့်သေးပါ")
        return await send_summary(update, context)

# ===== SUPPORT NAME & AMOUNT =====
async def support_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["support_name"] = update.message.text
    await update.message.reply_text("ဘယ်လောက်နဲ့ပွင့်တာလဲ:")
    return SUPPORT_AMOUNT

async def support_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        context.user_data["support_amount"] = float(text)
    except ValueError:
        await update.message.reply_text("⚠ Amount ကိုမှန်ထည့်ပါ:")
        return SUPPORT_AMOUNT
    return await send_summary(update, context)

# ===== SEND SUMMARY =====
async def send_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "No Username"

    summary = f"""
📊 Daily Marketing Report

👤 Staff: {user.full_name}
👤 Username: {username}
📅 Date & Time (UTC+06:30): {context.user_data['formatted_time']}

Today Add: {context.user_data.get('today_add')}
Today Detail: {context.user_data.get('today_detail')}
Detail Remaining: {context.user_data.get('detail_remain')}
Today Return: {context.user_data.get('today_return')}
Return Remaining: {context.user_data.get('return_remain')}
Today Cut: {context.user_data.get('today_cut')}
Cut Remaining: {context.user_data.get('cut_remain')}
Cut Reason: {context.user_data.get('cut_reason')}
Acc Open: {context.user_data.get('acc_open')}
"""

    if context.user_data.get("acc_open") == "Y":
        summary += f"Support Name: {context.user_data.get('support_name')}\n"
        summary += f"Open Amount: {context.user_data.get('support_amount')}\n"

    await context.bot.send_message(chat_id=OWNER_ID, text=summary)
    await update.message.reply_text("✅ ဒီနေ့တစ်ရက်ကုန်သွားပြီ!")

    return ConversationHandler.END

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TODAY_ADD: [MessageHandler(filters.TEXT & ~filters.COMMAND, today_add)],
            TODAY_DETAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, today_detail)],
            DETAIL_REMAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, detail_remain)],
            TODAY_RETURN: [MessageHandler(filters.TEXT & ~filters.COMMAND, today_return)],
            RETURN_REMAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, return_remain)],
            TODAY_CUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, today_cut)],
            CUT_REMAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, cut_remain)],
            CUT_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, cut_reason)],
            ACC_OPEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, acc_open)],
            SUPPORT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, support_name)],
            SUPPORT_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, support_amount)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from datetime import timedelta, timezone


# ===== CONFIG =====
#BOT_TOKEN = "8412305691:AAGZTvfoUa-97Xr4jiWlVZGFz0b_cCYLVUs"
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
    await update.message.reply_text("📊 Daily Marketing Report\n\nဒီနေ့ဘယ်နှစ်ယောက်အပ်လဲ (နံပါတ်ပဲထည့်):")
    return TODAY_ADD

# ===== NUMERIC INPUT VALIDATION =====
async def today_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        context.user_data["today_add"] = int(text)
    except ValueError:
        await update.message.reply_text("⚠ နံပါတ်ပဲထည့်လို့ပြောနေတယ် ဒါကျမမြင်ဘူး ပြန်ထည့်:")
        return TODAY_ADD
    await update.message.reply_text("ဒီနေ့ detail ဘယ်နှစ်ယောက်ပြောလဲ (နံပါတ်ပဲထည့်):")
    return TODAY_DETAIL

async def today_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        context.user_data["today_detail"] = int(text)
    except ValueError:
        await update.message.reply_text("⚠ နံပါတ်ပဲထည့်လို့ပြောနေတယ် ဒါကျမမြင်ဘူး ပြန်ထည့်:")
        return TODAY_DETAIL
    await update.message.reply_text("Detail ဘယ်နှစ်ယောက်ကျန်လဲ ဒီနေ့ (နံပါတ်ပဲထည့်):")
    return DETAIL_REMAIN

async def detail_remain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        context.user_data["detail_remain"] = int(text)
    except ValueError:
        await update.message.reply_text("⚠ နံပါတ်ပဲထည့်လို့ပြောနေတယ် ဒါကျမမြင်ဘူး ပြန်ထည့်:")
        return DETAIL_REMAIN
    await update.message.reply_text("ဒီနေ့ return ဘယ်နှစ်ယောက်ပြန်လဲ (နံပါတ်ပဲထည့်):")
    return TODAY_RETURN

async def today_return(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        context.user_data["today_return"] = int(text)
    except ValueError:
        await update.message.reply_text("⚠ နံပါတ်ပဲထည့်လို့ပြောနေတယ် ဒါကျမမြင်ဘူး ပြန်ထည့်:")
        return TODAY_RETURN
    await update.message.reply_text("Return ဘယ်နှစ်ယောက်ကျန်လဲ ဒီနေ့ (နံပါတ်ပဲထည့်):")
    return RETURN_REMAIN

async def return_remain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        context.user_data["return_remain"] = int(text)
    except ValueError:
        await update.message.reply_text("⚠ နံပါတ်ပဲထည့်လို့ပြောနေတယ် ဒါကျမမြင်ဘူး ပြန်ထည့်:")
        return RETURN_REMAIN
    await update.message.reply_text("ဒီနေ့ဘယ်နှစ်ယောက်ဖြတ်လဲ (နံပါတ်ပဲထည့်):")
    return TODAY_CUT

async def today_cut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        context.user_data["today_cut"] = int(text)
    except ValueError:
        await update.message.reply_text("⚠ နံပါတ်ပဲထည့်လို့ပြောနေတယ် ဒါကျမမြင်ဘူး ပြန်ထည့်:")
        return TODAY_CUT
    await update.message.reply_text("ဘယ်နှစ်ယောက်ဖြတ်ဖို့ကျန်သေးလဲ (နံပါတ်ပဲထည့်):")
    return CUT_REMAIN

async def cut_remain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        cut_remaining = int(text)
        context.user_data["cut_remain"] = cut_remaining
    except ValueError:
        await update.message.reply_text("⚠ နံပါတ်ပဲထည့်လို့ပြောနေတယ် ဒါကျမမြင်ဘူး ပြန်ထည့်:")
        return CUT_REMAIN

    if cut_remaining > 0:
        await update.message.reply_text(
            "⚠ ဖြတ်ဖို့ကျန်နေသေးတယ် ဘာလို့ကျန်နေသေးတာလဲ.\nဖြတ်ဖို့ကျန်နေသေးတဲ့အကြောင်းရင်း customer name နဲ့တခါတည်းရေး:"
        )
        return CUT_REASON
    else:
        context.user_data["cut_reason"] = "N/A"
        await update.message.reply_text("ဒီနေ့အကောင့်ပွင့်လား?ပွင့်ရင် Y မပွင့်ရင် N (Y/N):")
        return ACC_OPEN

# ===== CUT REASON (TEXT ONLY) =====
async def cut_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cut_reason"] = update.message.text
    await update.message.reply_text("ဒီနေ့အကောင့်ပွင့်လား?ပွင့်ရင် Y မပွင့်ရင် N (Y/N):")
    return ACC_OPEN

# ===== ACC OPEN LOGIC =====
async def acc_open(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["acc_open"] = update.message.text.strip().upper()
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "No Username"

    # Myanmar Time (UTC+06:30)
    myanmar_timezone = timezone(timedelta(hours=6, minutes=30))
    message_time_myanmar = update.message.date.astimezone(myanmar_timezone)
    context.user_data["formatted_time"] = message_time_myanmar.strftime("%Y-%m-%d %H:%M:%S")

    # Numeric values
    detail_remaining = int(context.user_data["detail_remain"])
    return_remaining = int(context.user_data["return_remain"])

    # ===== WARNING MESSAGE =====
    if detail_remaining > 0 or return_remaining > 0:
        warning_message = (
            "⚠ မနက်ဖြန်ခုကျန်နေတဲ့ကောင်တွေအကုန်ပြီးအောင်ပြောရမယ်\n"
            f"Detail ကျန်တဲ့ကောင်အရေအတွက်: {detail_remaining}\n"
            f"Return ကျန်တဲ့ကောင်အရေအတွက်: {return_remaining}"
        )
        await update.message.reply_text(warning_message)

    acc_open_value = context.user_data["acc_open"]

    if acc_open_value == "Y":
        # GIF congratulate
        gif_url = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHdvemFveGtzZTUxcWRsZ2J2eXRpMnQ4bGc0Z2E4azc3bW9mZGtwcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1JTy9isIm0u0OqePP1/giphy.gif"
        await update.message.reply_animation(animation=gif_url, caption="🎉 အကောင့်ပွင့်သွားပီ ပိုက်ဆံဝင်ဖို့ပဲကျန်တော့တယ်")
        # Ask support name next
        await update.message.reply_text("ရှာပေးတဲ့ support နာမည်ပြောပြပါဦး:")
        return SUPPORT_NAME
    elif acc_open_value == "N":
        gif_noacc = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExenY5MWl5djlidTl2b3U3aDQ1ZDVsYmdlbnJoMmYzN2h0eWNrM3o0bSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tZJagIk8GhR1NLNl7w/giphy.gif"
        # Myanmar text
        await update.message.reply_animation(animation=gif_noacc, caption="ခုထိအကောင့်ကမပွင့်သေးဘူး ထည့်ပေးတဲ့ support တွေကိုအားနာဦး")
        # Finish and send summary
        return await send_summary(update, context)

# ===== SUPPORT NAME =====
async def support_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["support_name"] = update.message.text
    await update.message.reply_text("ဘယ်လောက်နဲ့ပွင့်တာတုန်း:")
    return SUPPORT_AMOUNT

# ===== SUPPORT AMOUNT =====
async def support_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        context.user_data["support_amount"] = float(text)  # allow decimal
    except ValueError:
        await update.message.reply_text("⚠ ဘယ်လောက်နဲ့ပွင့်တာလဲမေးနေတာကို amount ကိုမှန်အောင်ထည့်လေ:")
        return SUPPORT_AMOUNT
    return await send_summary(update, context)

# ===== SEND SUMMARY FUNCTION =====
async def send_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "No Username"

    detail_remaining = int(context.user_data["detail_remain"])
    return_remaining = int(context.user_data["return_remain"])

    summary = f"""
📊 Daily Marketing Report

👤 Staff: {user.full_name}
👤 Username: {username}
📅 Date & Time (UTC+06:30): {context.user_data['formatted_time']}

Today Add: {context.user_data['today_add']}
Today Detail: {context.user_data['today_detail']}
Detail Remaining: {detail_remaining}
Today Return: {context.user_data['today_return']}
Return Remaining: {return_remaining}
Today Cut: {context.user_data['today_cut']}
Cut Remaining: {context.user_data['cut_remain']}
Cut Reason: {context.user_data['cut_reason']}
Acc Open: {context.user_data['acc_open']}
"""

    # Add support info if Acc Open = Y
    if context.user_data["acc_open"] == "Y":
        summary += f"Support Name: {context.user_data['support_name']}\n"
        summary += f"Open Amount: {context.user_data['support_amount']}\n"

    await context.bot.send_message(chat_id=OWNER_ID, text=summary)
    await update.message.reply_text("✅ ဒီနေ့တစ်ရက်တော့ကုန်သွားပြန်ပီပေါ့ မင်းကံကောင်းပါဇီ!")

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
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

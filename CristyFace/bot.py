import os
import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
)
from telegram.error import TelegramError
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ChatJoinRequestHandler, ContextTypes
)

# Set these in your environment before starting the bot.
BOT_TOKEN = os.getenv("BOT_TOKEN", "8812723309:AAF1Rxwva_8UJrKPCR5uPHrI1OqZsG941oU")  # Replace with your new token
# Numeric channel ID, usually looks like -1001234567890.
# The bot must be an administrator in this channel.
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
CHANNEL_INVITE_URL = "https://t.me/+IxVXx6qkPEpjZTYy"
NEW_VPN_URL = "https://t.me/vpnslark_bot?start=7894051808"
PHOTO_PATH = os.path.join(os.path.dirname(__file__), "welcome.jpg")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def subscription_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Подписаться на канал", url=CHANNEL_INVITE_URL)],
        [InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")],
    ])

def new_vpn_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 НОВЫЙ ВПН", url=NEW_VPN_URL)]
    ])

async def is_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if CHANNEL_ID == 0:
        logger.error("CHANNEL_ID is not configured.")
        return False
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator") or (
            member.status == "restricted" and getattr(member, "is_member", False)
        )
    except TelegramError:
        logger.exception("Could not check membership. Is the bot an admin in the channel?")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not update.message:
        return

    caption = (
        "👑 <b>CristyVPN</b>\n\n"
        "Мы переехали на новый канал и обновили VPN-сервис.\n"
        "1. Подпишись на канал.\n"
        "2. Нажми «Я подписался» — я проверю подписку.\n"
        "3. Получи ссылку на новый VPN."
    )
    try:
        with open(PHOTO_PATH, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                parse_mode="HTML",
                reply_markup=subscription_keyboard(),
            )
    except OSError:
        await update.message.reply_text(
            caption, parse_mode="HTML", reply_markup=subscription_keyboard()
        )

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    if await is_subscribed(query.from_user.id, context):
        text = (
            "✅ <b>Подписка подтверждена!</b>\n\n"
            "CristyVPN переехал. Чтобы продолжить пользоваться VPN, "
            "перейди в нашего нового бота по кнопке ниже."
        )
        await query.message.reply_text(
            text, parse_mode="HTML", reply_markup=new_vpn_keyboard()
        )
    else:
        await query.message.reply_text(
            "Пока не вижу подписку на канал. Подпишись по кнопке ниже, "
            "затем снова нажми «Я подписался».",
            reply_markup=subscription_keyboard(),
        )

async def approve_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    if not request:
        return
    if CHANNEL_ID and request.chat.id != CHANNEL_ID:
        return
    try:
        await context.bot.approve_chat_join_request(
            chat_id=request.chat.id,
            user_id=request.from_user.id,
        )
        logger.info("Approved join request from user %s", request.from_user.id)
    except TelegramError:
        logger.exception("Failed to approve join request")

def main():
    if not BOT_TOKEN or BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
        raise SystemExit("Set BOT_TOKEN to the token from @BotFather.")
    if CHANNEL_ID == 0:
        raise SystemExit(
            "Set CHANNEL_ID to your channel's numeric ID (for example -1001234567890)."
        )
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern="^check_subscription$"))
    # Automatically approves join requests in the configured channel.
    app.add_handler(ChatJoinRequestHandler(approve_join_request))
    logger.info("CristyVPN migration bot started.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

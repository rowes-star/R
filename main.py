import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Constants for ConversationHandler states
SET_GOOGLE_ACCOUNT, SET_PASSWORD, SET_KEY, SET_SUBJECT, SET_EMAILS, SET_SLEEP, SET_SEND_COUNT, SET_UPLOAD_IMAGE, CLEAR_UPLOAD_IMAGE, START_SENDING = range(10)

# Global variables to store user data and SMTP server details
user_data = {}
smtp_server = "your_smtp_server_address"
smtp_port = 587
smtp_username = "your_smtp_username"
smtp_password = "your_smtp_password"
sender_email = "your_sender_email"
receiver_email = "your_receiver_email"

# ...

# Function to start the bot
def start(update: Update, context: CallbackContext):
    user_data.clear()

    keyboard = [
        [InlineKeyboardButton("تعيين حساب قوقل", callback_data=str(SET_GOOGLE_ACCOUNT)),
         InlineKeyboardButton("تعيين باسورد", callback_data=str(SET_PASSWORD))],
        [InlineKeyboardButton("تعيين كليشه", callback_data=str(SET_KEY)),
         InlineKeyboardButton("تعيين موضوع", callback_data=str(SET_SUBJECT))],
        [InlineKeyboardButton("عرض معلومات", callback_data=str(SET_EMAILS)),
         InlineKeyboardButton("مسح معلوماتك", callback_data=str(SET_SLEEP))],
        [InlineKeyboardButton("تعيين ايميلات", callback_data=str(SET_SEND_COUNT)),
         InlineKeyboardButton("تعيين السليب", callback_data=str(SET_UPLOAD_IMAGE))],
        [InlineKeyboardButton("عدد الارسال", callback_data=str(CLEAR_UPLOAD_IMAGE)),
         InlineKeyboardButton("تعيين صوره الرفع", callback_data=str(START_SENDING))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("اهلا بك في بوت رفع خارجي (صلخ بالنعال)", reply_markup=reply_markup)

# ...

# Function to handle inline keyboard button presses
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    user_data['user_id'] = user_id

    # Handle different button presses
    if query.data == str(SET_GOOGLE_ACCOUNT):
        context.bot.send_message(user_id, "اختر حساب قوقل.")
        return SET_GOOGLE_ACCOUNT
    elif query.data == str(SET_PASSWORD):
        context.bot.send_message(user_id, "قم بإدخال رمز حساب قوقل الخاص بك.")
        return SET_PASSWORD
    elif query.data == str(SET_KEY):
        context.bot.send_message(user_id, "أدخل كلمة المرور للبلاغ.")
        return SET_KEY
    elif query.data == str(SET_SUBJECT):
        context.bot.send_message(user_id, "أدخل موضوع البلاغ.")
        return SET_SUBJECT
    elif query.data == str(SET_EMAILS):
        context.bot.send_message(user_id, "حدد الأيميلات التي تريد إرسال البلاغ إليها.")
        return SET_EMAILS
    elif query.data == str(SET_SLEEP):
        context.bot.send_message(user_id, "اختر فترة السكون بين البلاغات.")
        return SET_SLEEP
    elif query.data == str(SET_SEND_COUNT):
        context.bot.send_message(user_id, "حدد عدد مرات الإرسال.")
        return SET_SEND_COUNT
    elif query.data == str(SET_UPLOAD_IMAGE):
        context.bot.send_message(user_id, "أرسل صورة لتضاف إلى البلاغ.")
        return SET_UPLOAD_IMAGE
    elif query.data == str(CLEAR_UPLOAD_IMAGE):
        user_data.pop('image', None)
        context.bot.send_message(user_id, "تم مسح الصورة المرفقة.")
        return SET_UPLOAD_IMAGE
    elif query.data == str(START_SENDING):
        start_sending(update, context)
        return ConversationHandler.END

# ...

# Start the bot
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

states={
        SET_GOOGLE_ACCOUNT: [CallbackQueryHandler(button_handler)],
        SET_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, set_password)],
        SET_KEY: [MessageHandler(Filters.text & ~Filters.command, set_key)],
        SET_SUBJECT: [MessageHandler(Filters.text & ~Filters.command, set_subject)],
        SET_EMAILS: [MessageHandler(Filters.text & ~Filters.command, set_emails)],
        SET_SLEEP: [MessageHandler(Filters.text & ~Filters.command, set_sleep)],
        SET_SEND_COUNT: [MessageHandler(Filters.text & ~Filters.command, set_send_count)],
        SET_UPLOAD_IMAGE: [MessageHandler(Filters.photo & ~Filters.command, set_upload_image)],
        CLEAR_UPLOAD_IMAGE: [CallbackQueryHandler(button_handler)],
        START_SENDING: [CallbackQueryHandler(button_handler)]
    },
    fallbacks=[
        CommandHandler('allow_user', allow_user, pass_args=True),
        CommandHandler('show_allowed_users', show_allowed_users)
    ]
)

dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Constants for ConversationHandler states
SET_GOOGLE_ACCOUNT, SET_PASSWORD, SET_KEY, SET_SUBJECT, SET_EMAILS, SET_SLEEP, SET_SEND_COUNT, SET_UPLOAD_IMAGE, CLEAR_UPLOAD_IMAGE, START_SENDING = range(10)

# Global variables to store user data and SMTP server details
user_data = {}
smtp_server = "your_smtp_server_address"
smtp_port = 587
smtp_username = "your_smtp_username"
smtp_password = "your_smtp_password"
sender_email = "your_sender_email"
receiver_email = "your_receiver_email"
authorized_user_ids = {123, 456, 789}  # Replace with your authorized user IDs

# Function to check if the user is authorized
def is_authorized(user_id):
    return user_id in authorized_user_ids

    user_id = update.message.from_user.id
    if not is_authorized(user_id):
        update.message.reply_text("أنت غير مسموح لك باستخدام هذا البوت.")
        return
# Function to start the bot
def start(update: Update, context: CallbackContext):
    user_data.clear()

    keyboard = [
        [InlineKeyboardButton("تعيين حساب قوقل", callback_data=str(SET_GOOGLE_ACCOUNT)),
         InlineKeyboardButton("تعيين باسورد", callback_data=str(SET_PASSWORD))],
        [InlineKeyboardButton("تعيين كليشه", callback_data=str(SET_KEY)),
         InlineKeyboardButton("تعيين موضوع", callback_data=str(SET_SUBJECT))],
        [InlineKeyboardButton("عرض معلومات", callback_data=str(SET_EMAILS)),
         InlineKeyboardButton("مسح معلوماتك", callback_data=str(SET_SLEEP))],
        [InlineKeyboardButton("تعيين ايميلات", callback_data=str(SET_SEND_COUNT)),
         InlineKeyboardButton("تعيين السليب", callback_data=str(SET_UPLOAD_IMAGE))],
        [InlineKeyboardButton("عدد الارسال", callback_data=str(CLEAR_UPLOAD_IMAGE)),
         InlineKeyboardButton("تعيين صوره الرفع", callback_data=str(START_SENDING))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("اهلا بك في بوت رفع خارجي (صلخ بالنعال)", reply_markup=reply_markup)

# Function to handle inline keyboard button presses
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    user_data['user_id'] = user_id

    # Handle different button presses
    if query.data == str(SET_GOOGLE_ACCOUNT):
        context.bot.send_message(user_id, "اختر حساب قوقل.")
        return SET_GOOGLE_ACCOUNT
    elif query.data == str(SET_PASSWORD):
        context.bot.send_message(user_id, "قم بإدخال رمز حساب قوقل الخاص بك.")

return SET_PASSWORD
    elif query.data == str(SET_KEY):
        context.bot.send_message(user_id, "أدخل كلمة المرور للبلاغ.")
        return SET_KEY
    elif query.data == str(SET_SUBJECT):
        context.bot.send_message(user_id, "أدخل موضوع البلاغ.")
        return SET_SUBJECT
    elif query.data == str(SET_EMAILS):
        context.bot.send_message(user_id, "حدد الأيميلات التي تريد إرسال البلاغ إليها.")
        return SET_EMAILS
    elif query.data == str(SET_SLEEP):
        context.bot.send_message(user_id, "اختر فترة السكون بين البلاغات.")
        return SET_SLEEP
    elif query.data == str(SET_SEND_COUNT):
        context.bot.send_message(user_id, "حدد عدد مرات الإرسال.")
        return SET_SEND_COUNT
    elif query.data == str(SET_UPLOAD_IMAGE):
        context.bot.send_message(user_id, "أرسل صورة لتضاف إلى البلاغ.")
        return SET_UPLOAD_IMAGE
    elif query.data == str(CLEAR_UPLOAD_IMAGE):
        user_data.pop('image', None)
        context.bot.send_message(user_id, "تم مسح الصورة المرفقة.")
        return SET_UPLOAD_IMAGE
    elif query.data == str(START_SENDING):
        start_sending(update, context)
        return ConversationHandler.END

# Function to handle text input for setting password
def set_password(update: Update, context: CallbackContext):
    user_data['password'] = update.message.text
    update.message.reply_text("تم تعيين الرمز بنجاح.")
    return SET_KEY

# Function to handle text input for setting key
def set_key(update: Update, context: CallbackContext):
    user_data
# ...

# Function to handle text input for setting key
def set_key(update: Update, context: CallbackContext):
    user_data['key'] = update.message.text
    update.message.reply_text("تم تعيين كلمة المرور بنجاح.")
    return SET_SUBJECT

# Function to handle text input for setting subject
def set_subject(update: Update, context: CallbackContext):
    user_data['subject'] = update.message.text
    update.message.reply_text("تم تعيين موضوع البلاغ بنجاح.")
    return SET_EMAILS

# Function to handle text input for setting emails
def set_emails(update: Update, context: CallbackContext):
    user_data['emails'] = update.message.text
    update.message.reply_text("تم تعيين الأيميلات بنجاح.")
    return SET_SLEEP

# Function to handle text input for setting sleep duration
def set_sleep(update: Update, context: CallbackContext):
    user_data['sleep'] = update.message.text
    update.message.reply_text("تم تعيين فترة السكون بنجاح.")
    return SET_SEND_COUNT

# Function to handle text input for setting send count
def set_send_count(update: Update, context: CallbackContext):
    user_data['send_count'] = update.message.text
    update.message.reply_text("تم تعيين عدد مرات الإرسال بنجاح.")
    return SET_UPLOAD_IMAGE

# Function to handle photo input for setting upload image
def set_upload_image(update: Update, context: CallbackContext):
    user_data['image'] = update.message.photo[-1].file_id
    update.message.reply_text("تم تحميل الصورة بنجاح.")
    return SET_UPLOAD_IMAGE

# Function to start sending reports
def start_sending(update: Update, context: CallbackContext):
    user_id = user_data['user_id']
    report_data = user_data  # Use the user_data dictionary or any other data you want to send

    try:
        # Set up the message content
        subject = "Report Submission"
        body = str(report_data)
        message = f"Subject: {subject}\n\n{body}"

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message)

        context.bot.send_message(user_id, "تم بدء الإرسال...")
    except Exception as e:
        context.bot.send_message(user_id, f"حدث خطأ أثناء محاولة الإرسال: {str(e)}")

# ...
# ...

# Function to handle text input for setting upload image
def set_upload_image(update: Update, context: CallbackContext):
    user_data['image'] = update.message.photo[-1].file_id
    update.message.reply_text("تم تحميل الصورة بنجاح.")
    return START_SENDING

# Function to clear uploaded image
def clear_upload_image(update: Update, context: CallbackContext):
    user_data.pop('image', None)
    update.message.reply_text("تم مسح الصورة المرفقة.")
    return SET_UPLOAD_IMAGE

# Function to start sending reports
def start_sending(update: Update, context: CallbackContext):
    user_id = user_data['user_id']
    report_data = user_data  # Use the user_data dictionary or any other data you want to send

    try:
        # Set up the message content
        subject = "Report Submission"
        body = str(report_data)
        message = f"Subject: {subject}\n\n{body}"

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message)

        context.bot.send_message(user_id, "تم بدء الإرسال...")
    except Exception as e:
        context.bot.send_message(user_id, f"حدث خطأ أثناء محاولة الإرسال: {str(e)}")

# ...

# Add the missing handlers
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, set_subject))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, set_emails))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, set_sleep))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, set_send_count))
dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, set_upload_image))
dispatcher.add_handler(CallbackQueryHandler(clear_upload_image))
dispatcher.add_handler(CallbackQueryHandler(button_handler))

# Start the bot
updater.start_polling()
updater.idle()
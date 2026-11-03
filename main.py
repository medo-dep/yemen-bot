# -*- coding: utf-8 -*-
"""
بوت المناهج الدراسية اليمنية (الصف الأول الأساسي - الثالث الثانوي)
نسخة مخصصة للاستضافة السحابية 24/7 على منصة Render
الميزات:
- خادم ويب مصغر (Flask) لإبقاء البوت مستيقظاً 24/7 على خوادم Render.
- دعم كامل للمحادثات الخاصة وللقناة (نشر الفهرس والمقررات تلقائياً في القناة).
- تصفح المواد لكل صف بشكل منفصل وتحميل الكتب مباشرة.
- عبارات تشجيع ودعاء بالتوفيق لكل طالب.
"""

import os
import time
import threading
from flask import Flask
import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand
)

# 1. إعدادات البوت والبيئة
BOT_TOKEN = os.environ.get("BOT_TOKEN", "9069922168:AAGkOezeiktVlvURpzP4Nq5cI3I5NlPQrRY")
PORT = int(os.environ.get("PORT", 8080))

# رابط مجلد المناهج اليمنية الجديد على Google Drive
DRIVE_FOLDER_URL = "https://drive.google.com/drive/folders/1n3liyuAtGuJHby8k2LWCq-1y1hwYvtSe?usp=sharing"

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

# 2. خادم الويب لإبقاء البوت حياً (Keep-Alive)
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 بوت المناهج اليمنية يعمل بنجاح 24/7 على سحابة Render!"

def run_web_server():
    app.run(host="0.0.0.0", port=PORT)

# 3. بيانات الصفوف والمواد الدراسية
GRADES_DATA = {
    "grade1": {
        "title": "الصف الأول الأساسي",
        "hashtag": "#الصف_الأول",
        "books": [
            "القرآن وعلومه والتربية الإسلامية - الجزء الأول",
            "القرآن وعلومه والتربية الإسلامية - الجزء الثاني",
            "القراءة - الجزء الأول",
            "القراءة - الجزء الثاني",
            "الرياضيات - الجزء الأول",
            "الرياضيات - الجزء الثاني",
            "العلوم - الجزء الأول",
            "العلوم - الجزء الثاني",
            "اللغة الإنجليزية (Course Book)",
            "اللغة الإنجليزية (Work Book)",
        ]
    },
    "grade2": {
        "title": "الصف الثاني الأساسي",
        "hashtag": "#الصف_الثاني",
        "books": [
            "القرآن الكريم والتربية الإسلامية - الجزء الأول",
            "القرآن الكريم والتربية الإسلامية - الجزء الثاني",
            "القراءة والحساب - الجزء الأول",
            "القراءة والحساب - الجزء الثاني",
            "العلوم والتربية الصحية - الجزء الأول",
            "العلوم والتربية الصحية - الجزء الثاني",
        ]
    },
    "grade3": {
        "title": "الصف الثالث الأساسي",
        "hashtag": "#الصف_الثالث",
        "books": [
            "القرآن الكريم والتربية الإسلامية - الجزء الأول",
            "القرآن الكريم والتربية الإسلامية - الجزء الثاني",
            "القراءة - الجزء الأول",
            "القراءة - الجزء الثاني",
            "الرياضيات - الجزء الأول",
            "الرياضيات - الجزء الثاني",
            "العلوم - الجزء الأول",
            "العلوم - الجزء الثاني",
        ]
    },
    "grade4": {
        "title": "الصف الرابع الأساسي",
        "hashtag": "#الصف_الرابع",
        "books": [
            "القرآن الكريم والتربية الإسلامية - الجزء الأول",
            "القرآن الكريم والتربية الإسلامية - الجزء الثاني",
            "اللغة العربية - الجزء الأول",
            "اللغة العربية - الجزء الثاني",
            "الرياضيات - الجزء الأول",
            "الرياضيات - الجزء الثاني",
            "العلوم - الجزء الأول",
            "العلوم - الجزء الثاني",
            "الاجتماعيات - الكتاب كاملاً",
        ]
    },
    "grade5": {
        "title": "الصف الخامس الأساسي",
        "hashtag": "#الصف_الخامس",
        "books": [
            "التربية الإسلامية - الجزء الأول",
            "التربية الإسلامية - الجزء الثاني",
            "اللغة العربية - الجزء الأول",
            "اللغة العربية - الجزء الثاني",
            "الرياضيات - الجزء الأول",
            "الرياضيات - الجزء الثاني",
            "العلوم - الجزء الأول",
            "العلوم - الجزء الثاني",
            "الاجتماعيات - الجزء الأول",
            "الاجتماعيات - الجزء الثاني",
        ]
    },
    "grade6": {
        "title": "الصف السادس الأساسي",
        "hashtag": "#الصف_السادس",
        "books": [
            "التربية الإسلامية - الجزء الأول",
            "التربية الإسلامية - الجزء الثاني",
            "اللغة العربية - الجزء الأول",
            "اللغة العربية - الجزء الثاني",
            "الرياضيات - الجزء الأول",
            "الرياضيات - الجزء الثاني",
            "العلوم - الجزء الأول",
            "العلوم - الجزء الثاني",
            "الاجتماعيات - الجزء الأول",
            "الاجتماعيات - الجزء الثاني",
        ]
    },
    "grade7": {
        "title": "الصف السابع الأساسي",
        "hashtag": "#الصف_السابع",
        "books": [
            "التربية الإسلامية - الجزء الأول",
            "التربية الإسلامية - الجزء الثاني",
            "اللغة العربية - الجزء الأول",
            "اللغة العربية - الجزء الثاني",
            "الرياضيات - الجزء الأول",
            "الرياضيات - الجزء الثاني",
            "العلوم - الجزء الأول",
            "العلوم - الجزء الثاني",
            "التاريخ - الجزء الأول",
            "التاريخ - الجزء الثاني",
            "الجغرافيا - الكتاب كاملاً",
            "التربية الوطنية - الكتاب كاملاً",
            "اللغة الإنجليزية (Course Book)",
            "اللغة الإنجليزية (Work Book)",
        ]
    },
    "grade8": {
        "title": "الصف الثامن الأساسي",
        "hashtag": "#الصف_الثامن",
        "books": [
            "التربية الإسلامية - الجزء الأول",
            "التربية الإسلامية - الجزء الثاني",
            "اللغة العربية - الجزء الأول",
            "اللغة العربية - الجزء الثاني",
            "الرياضيات - الجزء الأول",
            "الرياضيات - الجزء الثاني",
            "العلوم - الجزء الأول",
            "العلوم - الجزء الثاني",
            "التاريخ - الجزء الأول",
            "التاريخ - الجزء الثاني",
            "الجغرافيا - الكتاب كاملاً",
            "التربية الوطنية - الكتاب كاملاً",
            "اللغة الإنجليزية (Course Book)",
            "اللغة الإنجليزية (Work Book)",
        ]
    },
    "grade9": {
        "title": "الصف التاسع الأساسي",
        "hashtag": "#الصف_التاسع",
        "books": [
            "التربية الإسلامية - الجزء الأول",
            "التربية الإسلامية - الجزء الثاني",
            "اللغة العربية - الجزء الأول",
            "اللغة العربية - الجزء الثاني",
            "الرياضيات - الجزء الأول",
            "الرياضيات - الجزء الثاني",
            "العلوم - الجزء الأول",
            "العلوم - الجزء الثاني",
            "التاريخ - الجزء الأول",
            "التاريخ - الجزء الثاني",
            "الجغرافيا - الكتاب كاملاً",
            "التربية الوطنية - الكتاب كاملاً",
            "اللغة الإنجليزية (Course Book)",
            "اللغة الإنجليزية (Work Book)",
        ]
    },
    "grade10": {
        "title": "الصف الأول الثانوي",
        "hashtag": "#الأول_الثانوي",
        "books": [
            "التربية الإسلامية - الجزء الأول",
            "التربية الإسلامية - الجزء الثاني",
            "اللغة العربية (نحو وصرف) - الجزء الأول",
            "اللغة العربية (نحو وصرف) - الجزء الثاني",
            "اللغة العربية (أدب ونصوص)",
            "الرياضيات - الجزء الأول",
            "الرياضيات - الجزء الثاني",
            "الفيزياء - الكتاب كاملاً",
            "الكيمياء - الكتاب كاملاً",
            "الأحياء - الكتاب كاملاً",
            "التاريخ - الكتاب كاملاً",
            "الجغرافيا - الكتاب كاملاً",
            "المجتمع اليمني - الكتاب كاملاً",
            "اللغة الإنجليزية (Course Book)",
            "اللغة الإنجليزية (Work Book)",
        ]
    },
    "grade11": {
        "title": "الصف الثاني الثانوي",
        "hashtag": "#الثاني_الثانوي",
        "books": [
            "التربية الإسلامية (فقه وحديث)",
            "التربية الإسلامية (سيرة وعقيدة)",
            "اللغة العربية (نحو وصرف)",
            "اللغة العربية (أدب ونصوص)",
            "اللغة العربية (قراءة ونقد)",
            "الرياضيات (علمي)",
            "الرياضيات (أدبي)",
            "الفيزياء (علمي)",
            "الكيمياء (علمي)",
            "الأحياء (علمي)",
            "التاريخ (أدبي)",
            "الجغرافيا (أدبي)",
            "اللغة الإنجليزية (Course Book)",
            "اللغة الإنجليزية (Work Book)",
        ]
    },
    "grade12": {
        "title": "الصف الثالث الثانوي",
        "hashtag": "#الثالث_الثانوي",
        "books": [
            "التربية الإسلامية (فقه وحديث) - الجزء الأول",
            "التربية الإسلامية (فقه وحديث) - الجزء الثاني",
            "التربية الإسلامية (القرآن وعلومه)",
            "اللغة العربية (أدب ونصوص ونقد)",
            "اللغة العربية (قراءة وتعبير)",
            "اللغة العربية (نحو وصرف)",
            "الرياضيات (علمي) - التفاضل والتكامل والجبر",
            "الرياضيات (أدبي)",
            "الفيزياء (علمي)",
            "الكيمياء (علمي)",
            "الأحياء (علمي)",
            "التاريخ (أدبي)",
            "الجغرافيا (أدبي)",
            "مبادئ الفلسفة (أدبي)",
            "اللغة الإنجليزية (Course Book)",
            "اللغة الإنجليزية (Work Book)",
        ]
    }
}

CLOSING_MESSAGE = (
    "\n\n📚 **نتمنى لكم مذاكرة ممتعة ودوام التوفيق والنجاح.**\n"
    "🇾🇪 **اجتهدوا في طلب العلم، فأنتم أمل المستقبل.**"
)

# 4. لوحات المفاتيح التفاعلية
def get_grades_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(f"📁 {info['title']}", callback_data=f"g_{key}")
        for key, info in GRADES_DATA.items()
    ]
    markup.add(*buttons)
    return markup

def get_books_keyboard(grade_key):
    info = GRADES_DATA[grade_key]
    markup = InlineKeyboardMarkup(row_width=1)
    
    for idx, book_title in enumerate(info["books"]):
        display_title = book_title if len(book_title) <= 35 else book_title[:32] + "..."
        markup.add(
            InlineKeyboardButton(
                f"📖 {display_title}",
                callback_data=f"b_{grade_key}_{idx}"
            )
        )
    
    markup.add(
        InlineKeyboardButton(
            f"📥 فتح مجلد {info['title']} بالدرايف",
            url=DRIVE_FOLDER_URL
        )
    )
    markup.add(
        InlineKeyboardButton(
            "🔙 العودة لقائمة الصفوف",
            callback_data="back_main"
        )
    )
    return markup

# 5. معالجات الرسائل في المحادثة الخاصة
@bot.message_handler(commands=["start"])
def handle_start(message):
    welcome_text = (
        "مرحباً بك في **بوت المناهج الدراسية اليمنية كاملة** 🇾🇪📚\n\n"
        "اختر المرحلة الدراسية لعرض قائمة المواد والكتب واختيار الكتاب المطلوب:"
    )
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_grades_keyboard()
    )

@bot.message_handler(commands=[f"grade{i}" for i in range(1, 13)])
def handle_direct_grade_command(message):
    cmd = message.text.split()[0].replace("/", "").split("@")[0]
    if cmd in GRADES_DATA:
        info = GRADES_DATA[cmd]
        bot.send_message(
            message.chat.id,
            f"📂 **كتب ومقررات {info['title']}:**\nاختر الكتاب المطلوب:",
            parse_mode="Markdown",
            reply_markup=get_books_keyboard(cmd)
        )

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    data = call.data

    if data == "back_main":
        bot.edit_message_text(
            "مرحباً بك في **بوت المناهج الدراسية اليمنية كاملة** 🇾🇪📚\n\n"
            "اختر المرحلة الدراسية لعرض قائمة المواد والكتب:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_grades_keyboard()
        )
        bot.answer_callback_query(call.id)
        return

    if data.startswith("g_"):
        grade_key = data.replace("g_", "")
        if grade_key in GRADES_DATA:
            info = GRADES_DATA[grade_key]
            text = (
                f"📂 **كتب ومقررات {info['title']}**\n"
                f"📊 عدد الكتب المتوفرة: {len(info['books'])} كتاباً\n\n"
                f"اختر الكتاب المطلوب لتحميله مباشرة:"
            )
            bot.edit_message_text(
                text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                parse_mode="Markdown",
                reply_markup=get_books_keyboard(grade_key)
            )
            bot.answer_callback_query(call.id)
            return

    if data.startswith("b_"):
        parts = data.split("_")
        if len(parts) >= 3:
            grade_key = parts[1]
            book_idx = int(parts[2])
            info = GRADES_DATA.get(grade_key)
            if info and book_idx < len(info["books"]):
                book_name = info["books"][book_idx]
                bot.answer_callback_query(call.id, f"جاري تجهيز {book_name}...")
                
                download_markup = InlineKeyboardMarkup(row_width=1)
                download_markup.add(
                    InlineKeyboardButton(
                        "📥 اضغط هنا للتحميل المباشر (PDF)",
                        url=DRIVE_FOLDER_URL
                    )
                )
                
                msg_text = (
                    f"📘 **كتاب: {book_name}**\n"
                    f"📂 المرحلة: {info['title']}\n"
                    f"🏷 {info['hashtag']} | #المناهج_اليمنية\n\n"
                    f"اضغط على الزر أدناه لفتح وتحميل الكتاب بصيغة PDF فوراً من درايف:"
                    f"{CLOSING_MESSAGE}"
                )
                bot.send_message(
                    call.message.chat.id,
                    msg_text,
                    parse_mode="Markdown",
                    reply_markup=download_markup
                )
            return

# 6. معالجات منشورات ورسائل القناة
@bot.channel_post_handler(func=lambda message: True)
def handle_channel_post(message):
    chat_id = message.chat.id
    text = (message.text or "").strip()
    print(f"📢 منشور جديد في القناة: {text}")

    if text in ["رفع", "فرز", "/upload_all", "/start"]:
        bot.send_message(
            chat_id,
            "🚀 **جاري نشر وفهرسة المناهج الدراسية اليمنية في القناة...**",
            parse_mode="Markdown"
        )
        
        for grade_key, info in GRADES_DATA.items():
            books_list = "\n".join([f"• 📖 {b}" for b in info["books"]])
            msg_text = (
                f"══════════════════════\n"
                f"📚 **{info['title']}**\n"
                f"══════════════════════\n\n"
                f"📋 **قائمة المقررات والكتب:**\n"
                f"{books_list}\n\n"
                f"🏷 {info['hashtag']} | #المناهج_اليمنية"
                f"{CLOSING_MESSAGE}"
            )
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    f"📥 فتح وتحميل كتب {info['title']}",
                    url=DRIVE_FOLDER_URL
                )
            )
            bot.send_message(chat_id, msg_text, parse_mode="Markdown", reply_markup=markup)
            time.sleep(1.5)

        bot.send_message(
            chat_id,
            "🎉 **تم الانتهاء من نشر وفهرسة جميع المناهج اليمنية في القناة بنجاح!**",
            parse_mode="Markdown"
        )

# 7. بدء تشغيل الخادم والبوت
if __name__ == "__main__":
    print("🚀 جاري تشغيل خادم الويب المصغر على المنفذ", PORT)
    threading.Thread(target=run_web_server, daemon=True).start()

    print("🤖 بوت المناهج اليمنية يعمل الآن على خوادم Render...")
    bot.infinity_polling(timeout=30, long_polling_timeout=30)

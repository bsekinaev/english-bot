from telegram import Update, ReplyKeyboardMarkup
from config import Config
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import database as db
from datetime import datetime

# Клавиатура
reply_keyboard = [
    ['Новое слово', 'Статистика'],
    ['Повторить слова', 'Я запомнил']
]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.register_user(user.id, user.username, user.first_name, user.last_name)
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я помогу тебе учить английские слова.\n\n"
        "Нажми 'Новое слово' чтобы получить слово для изучения.",
        reply_markup=markup
    )

async def send_daily_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    word_data = db.get_random_word(user_id)
    
    if word_data:
        word_id, word, translation, example = word_data
        context.user_data['last_word_id'] = word_id
        
        await update.message.reply_text(
            f"📖 Слово для изучения:\n\n"
            f"<b>{word}</b> - {translation}\n"
            f"<i>Пример:</i> {example}",
            parse_mode="HTML",
            reply_markup=markup
        )
    else:
        await update.message.reply_text("Пока нет слов для изучения!")

async def handle_word_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    if text == 'Я запомнил':
        word_id = context.user_data.get('last_word_id')
        if word_id:
            db.mark_word_as_learned(user_id, word_id)
            await update.message.reply_text("✅ Отлично! Я напомню об этом слове позже.")
        else:
            await update.message.reply_text("Сначала получите слово для изучения.")
    elif text == 'Новое слово':
        await send_daily_word(update, context)
    elif text == 'Статистика':
        stats = db.get_user_stats(user_id)
        await update.message.reply_text(
            f"📊 Ваша статистика:\n"
            f"Выучено слов: {stats['total_words']}\n"
            f"Правильных ответов: {stats['correct_answers']}\n"
            f"Точность: {stats['accuracy']}%"
        )
    elif text == 'Повторить слова':
        words = db.get_words_to_review(user_id)
        if words:
            await update.message.reply_text(
                "📚 Слова для повторения:\n" + 
                "\n".join([f"{w[0]} - {w[1]}" for w in words])
            )
        else:
            await update.message.reply_text("🎉 Пока нет слов для повторения!")

def main():
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_word_response))
    
    application.run_polling()

if __name__ == '__main__':
    main()

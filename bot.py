from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os
import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse
import uvicorn

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Настройки вебхука
# Безопасное получение токена только из переменных окружения
TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", 8000))
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL", "") + "/webhook"

# Создаем приложение Telegram
application = Application.builder().token(TOKEN).build()

# ===== ОБРАБОТЧИКИ КОМАНД =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start с кнопкой перезапуска"""
    user = update.effective_user
    user_name = user.full_name or "пользователь"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Перезапустить бота", callback_data="/start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_html(
        f"🚀 Привет, {user_name}!\n"
        "Я Средний Научный Бот канала <b>Республика Информация</b>, Фёдор Семёныч!🤖\n\n"
        "Используйте команды:\n"
        "/books - доступ к книжной библиотеке\n"
        "/help - помощь по боту\n"
        "/profile - ваш профиль\n\n"
        "📢 Основной канал: @republic_inform",
        reply_markup=reply_markup
    )

async def books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /books с HTML-ссылками"""
    response_text = (
        "📚 <b>Книжный раздел Республика</b>\n\n"
        "• <a href='https://disk.yandex.ru/d/BX1xA5UCNxz3YA'>Основная библиотека</a> - 5000+ книг\n"
        "• <a href='https://disk.yandex.ru/d/d5cAK6TBCJSa_Q'>Добавить новую книгу</a> (требуется регистрация)\n"
        "• <a href='https://disk.yandex.ru/d/BX1xA5UCNxz3YA?sort=modified'>Новинки</a> - последние добавленные книги\n\n"
        "🔐 <i>Для доступа к книгам требуется пароль от архива</i>\n"
        "💡 Пароль можно получить в основном канале: @republic_inform"
    )
    await update.message.reply_html(response_text, disable_web_page_preview=True)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /help с кнопкой перезапуска"""
    keyboard = [
        [InlineKeyboardButton("🔄 Перезапустить бота", callback_data="/start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    help_text = (
        "ℹ️ <b>Помощь по боту Фёдор Семёныч</b>\n\n"
        "📚 <u>Основные команды</u>:\n"
        "/start - начать работу с ботом\n"
        "/books - доступ к книжной библиотеке\n"
        "/profile - ваш профиль\n"
        "/settings - настройки бота\n\n"
        "🔗 <u>Полезные ссылки</u>:\n"
        "• Основной канал: @republic_inform\n"
        "• Разработчик: @Alex_De_White\n"
        "• Техническая поддержка: @Alex_De_White\n\n"
        "💡 По всем вопросам обращайтесь к разработчику"
    )
    await update.message.reply_html(help_text, reply_markup=reply_markup)

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /settings"""
    await update.message.reply_html(
        "⚙️ <b>Настройки бота</b>\n\n"
        "🔔 Уведомления: включены\n"
        "🌐 Язык: русский\n"
        "🛡️ Безопасность: стандартная\n\n"
        "⚡ Дополнительные настройки в разработке"
    )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /profile"""
    user = update.effective_user
    user_name = user.full_name or "пользователь"
    username = f"@{user.username}" if user.username else "не установлен"
    
    profile_text = (
        f"👤 <b>Ваш профиль</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Имя: {user_name}\n"
        f"🔗 Username: {username}\n\n"
        f"📅 Дата регистрации: 2025-08-10\n"
        f"⭐ Статус: стандартный пользователь\n\n"
        f"📚 Книг скачано: 0\n"
        f"🎁 Премиум: не активен"
    )
    await update.message.reply_html(profile_text)

# ===== ОБРАБОТЧИК КНОПОК =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на in-line кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "/start":
        user = update.effective_user
        user_name = user.full_name or "пользователь"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Перезапустить бота", callback_data="/start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"🚀 Привет, {user_name}!\n"
            "Я Средний Научный Бот канала <b>Республика Информация</b>, Фёдор Семёныч!🤖\n\n"
            "Используйте команды:\n"
            "/books - доступ к книжной библиотеке\n"
            "/help - помощь по боту\n"
            "/profile - ваш профиль\n\n"
            "📢 Основной канал: @republic_inform",
            parse_mode='HTML',
            reply_markup=reply_markup
        )

# ===== ОБРАБОТЧИК ОШИБОК =====
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Логируем ошибки"""
    logger.error(msg="Исключение при обработке команды:", exc_info=True)
    
    if update and isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "⚠️ Произошла ошибка при обработке команды. "
            "Попробуйте еще раз или обратитесь к разработчику @Alex_De_White"
        )

# ===== ВЕБХУК ЭНДПОИНТЫ =====
async def webhook(request: Request) -> Response:
    """Эндпоинт для вебхуков от Telegram"""
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.update_queue.put(update)
        return Response()
    except Exception as e:
        logger.error(f"Ошибка в вебхуке: {e}")
        return Response(status_code=500)

async def health_check(request: Request) -> PlainTextResponse:
    """Эндпоинт для проверки здоровья приложения (обязателен для Render)"""
    return PlainTextResponse("OK")

async def set_webhook():
    """Установка вебхука при запуске"""
    if WEBHOOK_URL:
        await application.bot.set_webhook(url=f"{WEBHOOK_URL}")
        logger.info(f"Вебхук установлен: {WEBHOOK_URL}")
    else:
        logger.warning("RENDER_EXTERNAL_URL не установлен, вебхук не настроен")

# ===== РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ =====
def setup_handlers():
    """Регистрация всех обработчиков"""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("books", books))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

# ===== ЗАПУСК ПРИЛОЖЕНИЯ =====
async def main():
    """Основная функция запуска"""
    logger.info("🔄 Инициализация бота с вебхуками...")
    
    # Регистрируем обработчики
    setup_handlers()
    
    # Запускаем приложение
    await application.initialize()
    await application.start()
    
    # Устанавливаем вебхук
    await set_webhook()
    
    # Создаем Starlette приложение
    starlette_app = Starlette(routes=[
        Route("/webhook", webhook, methods=["POST"]),
        Route("/healthcheck", health_check, methods=["GET"]),
        Route("/", health_check, methods=["GET"]),  # Корневой путь тоже для health check
    ])
    
    # Запускаем сервер
    config = uvicorn.Config(
        app=starlette_app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
    server = uvicorn.Server(config)
    
    logger.info(f"🤖 Бот запущен на порту {PORT}. Ожидание вебхуков...")
    await server.serve()

# ===== ТОЧКА ВХОДА =====
if __name__ == "__main__":
    asyncio.run(main())
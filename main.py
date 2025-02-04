from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Укажите свой API токен
API_TOKEN = '7758192329:AAFZ5DbgQOrmjtcfGeWCVhD8CPnRK-oB3Ac'

# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь два файла .txt, и я найду общие данные.")

# Функция для обработки файлов
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.user_data) < 2:
        file = update.message.document
        # Получаем объект файла
        file_obj = await file.get_file()
        
        # Скачиваем файл как байтовый массив
        file_path = f"./{file.file_name}"
        file_content = await file_obj.download_as_bytearray()  # Скачивание как байты

        # Записываем байтовые данные в файл на диск
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Чтение данных из файла и сохранение в user_data
        with open(file_path, 'r') as f:
            data = f.read().split(',')
            data = [item.strip() for item in data]  # Убираем пробелы
            context.user_data[len(context.user_data)] = set(data)  # Сохраняем как множество
        
        # Уведомление пользователя
        await update.message.reply_text(f"Файл {file.file_name} обработан.")
        
        # Если два файла уже загружены, находим общие данные
        if len(context.user_data) == 2:
            common_data = context.user_data[0].intersection(context.user_data[1])
            result = ', '.join(common_data) if common_data else "Нет общих данных."
            await update.message.reply_text(f"Общие данные: {result}")
            context.user_data.clear()  # Очищаем для следующих файлов
    else:
        await update.message.reply_text("Уже получены два файла. Отправьте /start, чтобы начать заново.")

# Основная функция для запуска бота
def main():
    application = Application.builder().token(API_TOKEN).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))  # Команда /start
    application.add_handler(MessageHandler(filters.Document.FileExtension("txt"), handle_file))  # Обработчик файлов

    application.run_polling()

if __name__ == "__main__":
    main()
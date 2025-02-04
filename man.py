from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Укажите свой API токен
API_TOKEN = '#'

# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь от двух до четырех файлов .txt, и я найду общие данные.")

# Функция для обработки файлов
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.user_data) < 4:  # Позволяем загрузить до 4 файлов
        file = update.message.document
        # Получаем объект файла
        file_obj = await file.get_file()
        
        # Скачиваем файл как байтовый массив
        file_path = f"./{file.file_name}"
        file_content = await file_obj.download_as_bytearray()

        # Записываем байтовые данные в файл на диск
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Чтение данных из файла и сохранение в user_data
        with open(file_path, 'r') as f:
            data = f.read().split(',')
            data = {item.strip() for item in data}  # Убираем пробелы и сохраняем как множество
            context.user_data[len(context.user_data)] = data  # Сохраняем множество данных
        
        # Уведомление пользователя
        await update.message.reply_text(f"Файл {file.file_name} обработан.")
        
        # Если загружено минимум 2 файла, ищем общие данные
        if len(context.user_data) >= 2:
            common_data = set.intersection(*context.user_data.values())  # Пересечение всех множеств
            result = ', '.join(common_data) if common_data else "Нет общих данных."
            await update.message.reply_text(f"Общие данные: {result}")
            
            # Если загружено 4 файла, очищаем данные для следующих файлов
            if len(context.user_data) == 4:
                context.user_data.clear()
                await update.message.reply_text("Получено максимальное количество файлов. Отправьте /start, чтобы начать заново.")
    else:
        await update.message.reply_text("Уже получены четыре файла. Отправьте /start, чтобы начать заново.")

# Основная функция для запуска бота
def main():
    application = Application.builder().token(API_TOKEN).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))  # Команда /start
    application.add_handler(MessageHandler(filters.Document.FileExtension("txt"), handle_file))  # Обработчик файлов

    application.run_polling()

if __name__ == "__main__":
    main()

import logging

from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.keyboards.inline import build_initial_survey_keyboard
import os
import random
from aiogram.types import FSInputFile

router = Router(name=__name__)
logger = logging.getLogger()


def get_random_image():
    images_dir = "bot/images"
    if not os.path.exists(images_dir):
        return None
        
    images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        return None
        
    random_image = random.choice(images)
    return FSInputFile(os.path.join(images_dir, random_image))

@router.message(CommandStart())
async def start(message: types.Message) -> None:
    # Получаем список файлов из папки images
    images_dir = "bot/images"
    images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if images:
        # Выбираем случайное изображение
        random_image = random.choice(images)
        image_path = os.path.join(images_dir, random_image)
        
        # Отправляем изображение с подписью
        await message.answer_photo(
            photo=FSInputFile(image_path),
            caption="""👋 <b>Привет!</b>

Этот бот поможет тебе лучше понять свой уровень тревожности и получить <b>персональные рекомендации</b> 🌟

🔍 <b>Что такое тревожность?</b>
Это ощущение внутреннего напряжения, беспокойства или страха, которое возникает как реакция на стрессовые ситуации. 
• Умеренная тревожность — это нормально 😌
• Но если тревога мешает учёбе, сну или общению — стоит обратить на это внимание ⚠️

🧠 <b>Как это работает?</b>
Мы используем модель машинного обучения, обученную на данных студентов (<a href="https://www.kaggle.com/datasets/sonia22222/students-mental-health-assessments/data">исходные данные</a>), чтобы:
✅ Оценить твой уровень тревожности
✅ Дать персонализированные советы
✅ Помочь улучшить эмоциональное состояние 💆‍♀️

❗ <b>Важно:</b>
Результаты не являются медицинским диагнозом. 
Если ты ощущаешь <b>высокий уровень тревожности</b>, пожалуйста, обратись к специалисту 👩‍⚕️

⏳ Анкета займет всего <b>2-3 минуты</b> (17 вопросов)
📊 Результат получишь <b>мгновенно</b>

<b>Готов(а) начать?</b> 🚀
    """,
            reply_markup=build_initial_survey_keyboard(),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            text="""
Привет!

Этот бот поможет тебе лучше понять, насколько ты тревожен(а)...
            """,
            reply_markup=build_initial_survey_keyboard()
        )


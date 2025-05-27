import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.database.engine import Repositories
from bot.database.models import User
from bot.keyboards.inline import build_initial_survey_keyboard

router = Router(name=__name__)
logger = logging.getLogger()


class SurveyStates(StatesGroup):
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_gpa = State()
    waiting_for_relationship_status = State()
    waiting_for_dormitory = State()
    waiting_for_stress_level = State()
    waiting_for_financial_stress = State()
    waiting_for_social_support = State()
    waiting_for_psychologist_help = State()
    waiting_for_sleep_hours = State()
    waiting_for_nutrition = State()
    waiting_for_physical_activity = State()
    waiting_for_anxiety_signs = State()
    waiting_for_depression_signs = State()
    waiting_for_panic_attacks = State()
    waiting_for_substance_use = State()
    waiting_for_chronic_diseases = State()
    waiting_for_family_mental_illness = State()
    waiting_for_feedback = State()
    waiting_for_bot_rating = State()


def build_keyboard(options, one_time=True):
    builder = ReplyKeyboardBuilder()
    for option in options:
        builder.add(types.KeyboardButton(text=option))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=one_time)


@router.message(Command("survey"))
async def start_survey(message: types.Message, state: FSMContext):
    await message.answer(
        "Вы хотите пройти опрос самостоятельно или сгенерировать случайные ответы для теста?",
        reply_markup=build_initial_survey_keyboard(),
    )
    await state.set_state("waiting_for_survey_choice")


async def ask_age(message: types.Message, state: FSMContext):
    age_options = ["18–20", "21–23", "24–26", "27–29", "30+"]
    await message.answer("Сколько вам лет?", reply_markup=build_keyboard(age_options))
    await state.set_state(SurveyStates.waiting_for_age)


@router.message(SurveyStates.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    valid_ages = ["18–20", "21–23", "24–26", "27–29", "30+"]
    if message.text not in valid_ages:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Age=message.text)
    await ask_gender(message, state)


async def ask_gender(message: types.Message, state: FSMContext):
    gender_options = ["Мужской", "Женский"]
    await message.answer("Ваш пол:", reply_markup=build_keyboard(gender_options))
    await state.set_state(SurveyStates.waiting_for_gender)


def convert_sex(sex: str):
    return "Male" if sex == "Мужчина" else "Female"

@router.message(SurveyStates.waiting_for_gender)
async def process_gender(message: types.Message, state: FSMContext):
    valid_genders = ["Мужской", "Женский"]
    if message.text not in valid_genders:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Gender=convert_sex(message.text))
    await ask_gpa(message, state)


async def ask_gpa(message: types.Message, state: FSMContext):
    gpa_options = ["0", "1", "2", "3", "4", "5"]
    await message.answer("Ваш CGPA (успеваемость):", reply_markup=build_keyboard(gpa_options))
    await state.set_state(SurveyStates.waiting_for_gpa)


@router.message(SurveyStates.waiting_for_gpa)
async def process_gpa(message: types.Message, state: FSMContext):
    valid_gpas = ["0", "1", "2", "3", "4", "5"]
    if message.text not in valid_gpas:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(CGPA=message.text)
    await ask_relationship_status(message, state)


def convert_relationship_status(status: str):
    mapping = {"Холост/не замужем": "Single", "В отношениях": "InaRelationship", "Женат/замужем": "Married"}
    return mapping[status]

async def ask_relationship_status(message: types.Message, state: FSMContext):
    status_options = ["Холост/не замужем", "В отношениях", "Женат/замужем"]
    await message.answer("Ваше семейное положение:", reply_markup=build_keyboard(status_options))
    await state.set_state(SurveyStates.waiting_for_relationship_status)


@router.message(SurveyStates.waiting_for_relationship_status)
async def process_relationship_status(message: types.Message, state: FSMContext):
    valid_statuses = ["Холост/не замужем", "В отношениях", "Женат/замужем"]
    if message.text not in valid_statuses:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Relationship_Status=convert_relationship_status(message.text))
    await ask_dormitory(message, state)

def convert_Residence_Type(status: str):
    mapping = {"Да": "Yes", "Нет": "No", "Живу с семьей": "WithFamily"}
    return mapping[status]

async def ask_dormitory(message: types.Message, state: FSMContext):
    dormitory_options = ["Да", "Нет", "Живу с семьей"]
    await message.answer("Вы проживаете в общежитии?", reply_markup=build_keyboard(dormitory_options))
    await state.set_state(SurveyStates.waiting_for_dormitory)


@router.message(SurveyStates.waiting_for_dormitory)
async def process_dormitory(message: types.Message, state: FSMContext):
    valid_answers = ["Да", "Нет", "Живу с семьей"]
    if message.text not in valid_answers:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Residence_Type=convert_Residence_Type(message.text))
    await ask_stress_level(message, state)


async def ask_stress_level(message: types.Message, state: FSMContext):
    await message.answer(
        "Оцените ваш уровень стресса в данный момент времени (1: абсолютно спокоен, 5: претерпеваю высокий уровень стресса):",
        reply_markup=build_keyboard(["1", "2", "3", "4", "5"]),
    )
    await state.set_state(SurveyStates.waiting_for_stress_level)


@router.message(SurveyStates.waiting_for_stress_level)
async def process_stress_level(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4", "5"]:
        await message.answer("Пожалуйста, выберите число от 1 до 5")
        return

    await state.update_data(Stress_Level=int(message.text))
    await ask_financial_stress(message, state)


async def ask_financial_stress(message: types.Message, state: FSMContext):
    await message.answer(
        "Насколько вы испытываете финансовый стресс? (1 — совсем не беспокоит, 5 — постоянный источник тревоги)",
        reply_markup=build_keyboard(["1", "2", "3", "4", "5"]),
    )
    await state.set_state(SurveyStates.waiting_for_financial_stress)


@router.message(SurveyStates.waiting_for_financial_stress)
async def process_financial_stress(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4", "5"]:
        await message.answer("Пожалуйста, выберите число от 1 до 5")
        return

    await state.update_data(Financial_Stress=int(message.text))
    await ask_social_support(message, state)


async def ask_social_support(message: types.Message, state: FSMContext):
    options = ["Низкое", "Среднее", "Хорошее"]
    await message.answer(
        "Как вы оцениваете уровень социальной поддержки в вашей жизни?",
        reply_markup=build_keyboard(options=options),
    )
    await state.set_state(SurveyStates.waiting_for_social_support)

def convert_social_support(socail_support: str):
    mapping = {"Низкое": "Weak", "Среднее": "Moderate", "Хорошее": "Strong"}
    return mapping[socail_support]

@router.message(SurveyStates.waiting_for_social_support)
async def process_social_support(message: types.Message, state: FSMContext):
    options = ["Низкое", "Среднее", "Хорошее"]
    if message.text not in options:
        await message.answer("Пожалуйста, выберите из: (Низкий, Средний, Хороший)")
        return

    await state.update_data(Social_Support=convert_social_support(message.text))
    await ask_psychologist_help(message, state)


async def ask_psychologist_help(message: types.Message, state: FSMContext):
    options = ["Да", "Нет"]
    await message.answer("Пользуетесь ли вы помощью психолога?", reply_markup=build_keyboard(options))
    await state.set_state(SurveyStates.waiting_for_psychologist_help)

@router.message(F.text.in_(["Пройти опрос"]))
async def handle_survey_choice(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == "Пройти опрос":
        await ask_age(message, state)



@router.message(SurveyStates.waiting_for_psychologist_help)
async def process_psychologist_help(message: types.Message, state: FSMContext):
    valid_options = ["Да", "Нет"]
    if message.text not in valid_options:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Counseling_Service_Use="Yes" if message.text == "Да" else "No")
    await ask_sleep_hours(message, state)


async def ask_sleep_hours(message: types.Message, state: FSMContext):
    options = ["Низкое", "Среднее", "Хорошее"]
    await message.answer("Как вы оцениваете свое качество сна?", reply_markup=build_keyboard(options))
    await state.set_state(SurveyStates.waiting_for_sleep_hours)

def convert_sleep_quality(quality: str):
    mapping = {"Низкое": "Poor", "Среднее": "Average", "Хорошее": "Good"}
    return mapping[quality]


@router.message(SurveyStates.waiting_for_sleep_hours)
async def process_sleep_hours(message: types.Message, state: FSMContext):
    valid_options = ["Низкое", "Среднее", "Хорошее"]
    if message.text not in valid_options:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Sleep_Quality=convert_sleep_quality(message.text))
    await ask_nutrition(message, state)


async def ask_nutrition(message: types.Message, state: FSMContext):
    options = ["Плохо", "Средне", "Хорошо"]
    await message.answer("Как оцениваете свое питание?", reply_markup=build_keyboard(options))
    await state.set_state(SurveyStates.waiting_for_nutrition)

def convert_diet_quality(quality: str):
    mapping = {"Плохо": "Poor", "Средне": "Average", "Хорошо": "Good"}
    return mapping[quality]

@router.message(SurveyStates.waiting_for_nutrition)
async def process_nutrition(message: types.Message, state: FSMContext):
    valid_options = ["Плохо", "Средне", "Хорошо"]
    if message.text not in valid_options:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Diet_Quality=convert_diet_quality(message.text))
    await ask_physical_activity(message, state)


# TODO LOW MEDIUM HIGH
async def ask_physical_activity(message: types.Message, state: FSMContext):
    options = ["Высокий", "Средний", "Низкий"]
    await message.answer("Оцените ваш уровень физической активности?", reply_markup=build_keyboard(options))
    await state.set_state(SurveyStates.waiting_for_physical_activity)

def convert_physical_activity(activity: str):
    mapping = {
        "Высокий": "High",
        "Средний": "Medium",
        "Низкий": "Low",
    }
    return mapping[activity]

@router.message(SurveyStates.waiting_for_physical_activity)
async def process_physical_activity(message: types.Message, state: FSMContext):
    valid_options = ["Высокий", "Средний", "Низкий"]
    if message.text not in valid_options:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Physical_Activity=convert_physical_activity(message.text))
    await ask_anxiety_signs(message, state)


async def ask_anxiety_signs(message: types.Message, state: FSMContext):
    options = ["0", "1", "2", "3", "4", "5"]
    await message.answer("Как вы оцениваете уровень тревожности от 0 до 5?", reply_markup=build_keyboard(options))
    await state.set_state(SurveyStates.waiting_for_anxiety_signs)


@router.message(SurveyStates.waiting_for_anxiety_signs)
async def process_anxiety_signs(message: types.Message, state: FSMContext):
    valid_options = ["0", "1", "2", "3", "4", "5"]
    if message.text not in valid_options:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Anxiety_Score=int(message.text))
    await ask_substance_use(message, state)


async def ask_substance_use(message: types.Message, state: FSMContext):
    options = ["Да", "Нет"]
    await message.answer("Вы употребляете алкоголь/никотин?", reply_markup=build_keyboard(options))
    await state.set_state(SurveyStates.waiting_for_substance_use)

# TODO 
@router.message(SurveyStates.waiting_for_substance_use)
async def process_substance_use(message: types.Message, state: FSMContext):
    valid_options = ["Да", "Нет"]
    if message.text not in valid_options:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Substance_Use="Yes" if message.text == "Да" else "No")
    await ask_chronic_diseases(message, state)


async def ask_chronic_diseases(message: types.Message, state: FSMContext):
    options = ["Да", "Нет"]
    await message.answer("Есть ли у вас хронические заболевания?", reply_markup=build_keyboard(options))
    await state.set_state(SurveyStates.waiting_for_chronic_diseases)


@router.message(SurveyStates.waiting_for_chronic_diseases)
async def process_chronic_diseases(message: types.Message, state: FSMContext):
    valid_options = ["Да", "Нет"]
    if message.text not in valid_options:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Chronic_Illness="Yes" if message.text == "Да" else "No")
    await ask_family_mental_illness(message, state)


async def ask_family_mental_illness(message: types.Message, state: FSMContext):
    options = ["Да", "Нет"]
    await message.answer("Есть ли в вашей семье психические заболевания?", reply_markup=build_keyboard(options))
    await state.set_state(SurveyStates.waiting_for_family_mental_illness)


@router.message(SurveyStates.waiting_for_family_mental_illness)
async def process_family_mental_illness(message: types.Message, state: FSMContext, repo: Repositories, user: User):
    valid_options = ["Да", "Нет"]
    if message.text not in valid_options:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return

    await state.update_data(Family_History="Yes" if message.text == "Да" else "No")
    await process_feedback(message, state, repo, user)


@router.message(SurveyStates.waiting_for_feedback)
async def process_feedback(message: types.Message, state: FSMContext, repo: Repositories, user: User):
    valid_options = ["Да", "Нет"]
    if message.text not in valid_options:
        await message.answer("Пожалуйста, выберите вариант используя кнопки ниже")
        return
    await ask_bot_rating(message, state)


async def ask_bot_rating(message: types.Message, state: FSMContext):
    await message.answer("Оцените бота (1:плохо–5:восторг):", reply_markup=build_keyboard(["1", "2", "3", "4", "5"]))
    await state.set_state(SurveyStates.waiting_for_bot_rating)


import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

try:
    depression_model = joblib.load("model/depression_model3.pkl")
except Exception as e:
    logger.error(f"Failed to load ML model: {e}")
    depression_model = None


def age_mapping(age: int):
    mapping = {"18–20": 19, "21–23": 22, "24–26": 25, "27–29": 28, "30+": 30}
    return mapping.get(age, 25)

def prepare_features(data: dict) -> pd.DataFrame:
    """Преобразует ответы анкеты в признаки, которые ожидает модель"""

    features = {
        "Age": age_mapping(data["Age"]),
        "Gender": data['Gender'],
        "Course": "Engineering",
        "CGPA": convert_gpa(data["CGPA"]),
        "Stress_Level": data["Stress_Level"],
        "Anxiety_Score": data["Anxiety_Score"],
        "Sleep_Quality": data["Sleep_Quality"],
        "Physical_Activity": data["Physical_Activity"],
        "Diet_Quality": data["Diet_Quality"],
        "Social_Support": data["Social_Support"],
        "Relationship_Status": data["Relationship_Status"],
        "Substance_Use": data["Substance_Use"],
        "Counseling_Service_Use": data["Counseling_Service_Use"],
        "Family_History": data["Family_History"],
        "Chronic_Illness": data["Chronic_Illness"],
        "Financial_Stress": data["Financial_Stress"],
        "Extracurricular_Involvement": 2,
        "Semester_Credit_Load": 22,
        "Residence_Type": data["Residence_Type"],
        'Counseling_Service_Use_Level': None, 
        'Diet_Quality_Level': None, 
        'Family_History_Bool': None, 
        'Gender_Bool': None, 
        'Substance_Use_Level': None,
        'Social_Support_Level': None,
        'Extracurricular_Involvement_Level': None, 
        'Physical_Activity_Level': None, 
        'Sleep_Quality_Level': None, 
        'Chronic_Illness_Bool': None,
    }

    if hasattr(depression_model["model"], "feature_names_in_"):
        print("Ожидаемые признаки:", depression_model["model"].feature_names_in_)
        print("Их количество:", len(depression_model["model"].feature_names_in_))
    df = pd.DataFrame([features])
    return df


def convert_gpa(gpa_str):
    if gpa_str == "< 2.0":
        return 1.0
    elif gpa_str == "2.0–2.5":
        return 2.25
    elif gpa_str == "2.6–3.0":
        return 2.8
    elif gpa_str == "3.1–3.5":
        return 3.3
    else:
        return 3.8

import os
import random
from aiogram.types import FSInputFile

@router.message(SurveyStates.waiting_for_bot_rating)
async def process_bot_rating(message: types.Message, state: FSMContext, repo: Repositories, user: User):
    if message.text not in ["1", "2", "3", "4", "5"]:
        await message.answer("Пожалуйста, выберите число от 1 до 5")
        return

    data = await state.get_data()
    data["bot_rating"] = int(message.text)

    converted_data = {
        "user_id": user.id,
        "age": age_mapping(data["Age"]),
        "gender": data['Gender'],
        "course": "Business",
        "gpa": convert_gpa(data["CGPA"]),
        "stress_level": data["Stress_Level"],
        "anxiety_score": data["Anxiety_Score"],
        "sleep_quality": data["Sleep_Quality"],
        "physical_activity": data["Physical_Activity"],
        "diet_quality": data["Diet_Quality"],
        "social_support": data["Social_Support"],
        "relationship_status": data["Relationship_Status"],
        "substance_use": data["Substance_Use"],
        "counseling_service_use": data["Counseling_Service_Use"],
        "family_history": data["Family_History"],
        "chronic_illness": data["Chronic_Illness"],
        "financial_stress": data["Financial_Stress"],
        "extracurricular_involvement": "Moderate",
        "semester_credit_load": 17,
        "residence_type": data["Residence_Type"],
        "bot_rating": data["bot_rating"],
    }

    survey = await repo.survey_responses.create(**converted_data)
    await repo.session.commit()

    # Получаем случайное изображение
    images_dir = "bot/images"  # Папка с картинками для результатов
    try:
        images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        random_image = random.choice(images) if images else None
    except Exception as e:
        logger.error(f"Error loading images: {e}")
        random_image = None

    prediction_text = ""
    if depression_model:
        try:
            new_df = prepare_features(data)
            proba_arr = depression_model["model"].predict_proba(new_df)
            proba = proba_arr[:, 1][0]
            pred = int(proba >= depression_model["threshold"])
            
            if proba >= 0.41:
                prediction_text = """
🔴 <b>Высокий уровень тревожности</b>

У тебя высокий уровень тревожности. Это может проявляться в:
• Навязчивых мыслях 🤯
• Постоянном напряжении �
• Проблемах со сном 🌙
• Ощущении усталости 😴

💡 <b>Рекомендации:</b>
→ Обратись за профессиональной поддержкой (психолог или консультант) 👩⚕️
→ Минимизируй источники стресса 🧘‍♀️
→ Начни с малого: дыхательные упражнения, режим сна, базовая физическая активность 🏃
→ Избегай стимуляторов (кофе, алкоголь, никотин) ☕🚭

<b>Помни:</b> Ты не один(а), и тревожность — это не слабость. 
Это сигнал организма, который можно услышать и с ним работать 💪
                """
            else:
                prediction_text = """
🟢 <b>Низкий уровень тревожности</b>

У тебя низкий уровень тревожности — это отличный результат! 🌟
Ты, вероятно, умеешь справляться со стрессом и сохраняешь внутреннее спокойствие даже в сложных ситуациях 😌

💡 <b>Советы для поддержания состояния:</b>
→ Поддерживай здоровые привычки (сон, питание, физическая активность) 🥗🏋️
→ Делай перерывы в учёбе/работе ⏸️
→ Развивай навыки саморегуляции и осознанности 🧠
→ Попробуй дыхательные практики или медитации для укрепления устойчивости к стрессу 🌬️

Продолжай в том же духе! 💫
                """

            prediction_text = f"\n🔍 <b>Результат анализа:</b>\nВероятность: {proba:.1%}\n{prediction_text}"

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            prediction_text = "\n⚠️ <b>Не удалось проанализировать результаты</b>"
    else:
        prediction_text = "\n⚠️ <b>Сервис анализа временно недоступен</b>"

    # Отправляем сообщение с картинкой или без
    if random_image:
        image_path = os.path.join(images_dir, random_image)
        try:
            await message.answer_photo(
                photo=FSInputFile(image_path),
                caption=f"Спасибо за прохождение опроса! {prediction_text}",
                reply_markup=types.ReplyKeyboardRemove(),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            await message.answer(
                f"Спасибо за прохождение опроса! {prediction_text}",
                reply_markup=types.ReplyKeyboardRemove(),
                parse_mode="HTML"
            )
    else:
        await message.answer(
            f"Спасибо за прохождение опроса! {prediction_text}",
            reply_markup=types.ReplyKeyboardRemove(),
            parse_mode="HTML"
        )

    await state.clear()


@router.message(Command("my_surveys"))
async def show_my_surveys(message: types.Message, user: User, repo: Repositories):
    responses = await repo.survey_responses.get_user_responses(user.id)

    if not responses:
        await message.answer("У вас нет сохраненных анкет.")
        return

    builder = InlineKeyboardBuilder()
    for response in responses:
        date = response.created_at.strftime("%d.%m.%Y %H:%M")
        builder.row(types.InlineKeyboardButton(text=f"Анкета от {date}", callback_data=f"view_survey_{response.id}"))

    await message.answer("Ваши сохраненные анкеты:", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("view_survey_"))
async def view_survey(callback: types.CallbackQuery, user: User, repo: Repositories):
    survey_id = int(callback.data.split("_")[-1])
    response = await repo.survey_responses.get_by_id(survey_id)

    if not response or response.user_id != user.id:
        await callback.answer("⚠️ Анкета не найдена", show_alert=True)
        return

    gender_map = {"Male": "Мужской", "Female": "Женский"}
    residence_map = {"Yes": "Да", "No": "Нет", "WithFamily": "С семьей"}
    activity_map = {"High": "Высокая", "Medium": "Средняя", "Low": "Низкая"}
    diet_map = {"Good": "Хорошее", "Average": "Среднее", "Poor": "Плохое"}
    sleep_map = {"Good": "Хорошее", "Average": "Среднее", "Poor": "Плохое"}
    support_map = {"Strong": "Сильная", "Moderate": "Средняя", "Weak": "Слабая"}

    text = (
        f"📅 <b>Дата заполнения:</b> {response.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        f"👤 <b>Возраст:</b> {response.age}\n"
        f"🚻 <b>Пол:</b> {gender_map.get(response.gender, response.gender)}\n"
        f"🎓 <b>Успеваемость (GPA):</b> {response.gpa:.1f}\n"
        f"💍 <b>Семейное положение:</b> {response.relationship_status}\n"
        f"🏠 <b>Проживание:</b> {residence_map.get(response.residence_type, response.residence_type)}\n\n"
        f"😔 <b>Уровень стресса:</b> {response.stress_level}/5\n"
        f"💰 <b>Финансовый стресс:</b> {response.financial_stress}/5\n"
        f"👥 <b>Социальная поддержка:</b> {support_map.get(response.social_support, response.social_support)}\n"
        f"🛌 <b>Качество сна:</b> {sleep_map.get(response.sleep_quality, response.sleep_quality)}\n"
        f"🏃 <b>Физическая активность:</b> {activity_map.get(response.physical_activity, response.physical_activity)}\n"
        f"🍎 <b>Качество питания:</b> {diet_map.get(response.diet_quality, response.diet_quality)}\n"
        f"😟 <b>Уровень тревожности:</b> {response.anxiety_score}/5\n\n"
        f"⭐ <b>Оценка бота:</b> {'★' * response.bot_rating}{'☆' * (5 - response.bot_rating)}"
    )

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="❌ Удалить", 
            callback_data=f"delete_survey_{response.id}"
        ),
        types.InlineKeyboardButton(
            text="⬅️ Назад", 
            callback_data="back_to_surveys"
        ),
    )

    await callback.message.edit_text(
        text, 
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("delete_survey_"))
async def delete_survey(callback: types.CallbackQuery, user: User, repo: Repositories):
    survey_id = int(callback.data.split("_")[-1])
    deleted = await repo.survey_responses.delete_response(survey_id, user.id)

    if deleted:
        await callback.answer("✅ Анкета удалена", show_alert=True)
        await show_my_surveys(callback.message, user, repo)
    else:
        await callback.answer("❌ Не удалось удалить анкету", show_alert=True)


@router.callback_query(F.data == "back_to_surveys")
async def back_to_surveys(callback: types.CallbackQuery, user: User, repo: Repositories):
    await show_my_surveys(callback.message, user, repo)

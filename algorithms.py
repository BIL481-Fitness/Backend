import random
from typing import Dict, List
from sqlalchemy.orm import Session
from models import Exercise, User
from datetime import datetime
from models import UserFitnessData
import pandas as pd



def save_workout_plan_to_excel(workout_plan, filename="workout_plan.xlsx"):
    """
    Exports the workout plan to an Excel file.

    Args:
    - workout_plan (dict): The workout plan dictionary, with days as keys and plans as values.
    - filename (str): Name of the Excel file to save the plan.
    """
    with pd.ExcelWriter(filename) as writer:
        for day, exercises in workout_plan.items():
            if exercises:  # If there are exercises for the day
                # Ensure the DataFrame columns align with the workout plan structure
                df = pd.DataFrame(exercises, columns=["bolge", "hareket_adi", "set_sayisi", "tekrar_sayisi", "ekipman"])
                df.to_excel(writer, sheet_name=day, index=False)
            else:  # Handle rest day or no exercises
                pd.DataFrame([{"Message": "Rest Day"}]).to_excel(writer, sheet_name=day, index=False)



'''

BELOW IS SAME

'''






def generate_workout_plan(user_id: int, days: int, db: Session) -> Dict[str, List[Dict[str, str]]]:
    # Kullanıcıyı veritabanından al
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Kullanıcı bulunamadı.")
    
    # Kullanıcı özelliklerine göre yoğunluk ayarları
    # bmi = user.bmi
    # exercise_intensity = (
    #     'low' if bmi < 18.5 else
    #     'medium' if bmi < 24.9 else
    #     'high' if bmi < 29.9 else
    #     'very high'
    # )
    
    # Egzersiz verilerini al
    exercises = db.query(Exercise).all()
    workout_plan = {}

    # Kas grupları
    regions = ["Gogus", "Omuz", "Biceps", "On Kol", "Arka Kol", "Sirt", "Bacak"]

    def get_random_exercises(region, count):
        region_exercises = [e for e in exercises if e.body_part == region]
        return random.sample(region_exercises, min(count, len(region_exercises)))

    # Gün sayısına göre egzersiz planı
    for day in range(1, days + 1):
        day_key = f"Day {day}"

        if day == 5 and days == 7:  # Dinlenme günü
            workout_plan[day_key] = [{"Message": "Dinlenme Günü"}]
            continue

        if day == 1:
            day_plan = (
                get_random_exercises("Gogus", 2) +
                get_random_exercises("Omuz", 2) +
                get_random_exercises("Biceps", 1) +
                get_random_exercises("On Kol", 1) +
                get_random_exercises("Arka Kol", 1) +
                get_random_exercises("Sirt", 2) +
                get_random_exercises("Bacak", 2)
            )
        elif day == 2:
            day_plan = (
                get_random_exercises("Gogus", 2) +
                get_random_exercises("Omuz", 2) +
                get_random_exercises("Biceps", 1) +
                get_random_exercises("On Kol", 1) +
                get_random_exercises("Arka Kol", 1) +
                get_random_exercises("Sirt", 2)
            )
        elif day == 3:
            day_plan = (
                get_random_exercises("Gogus", 3) +
                get_random_exercises("Omuz", 3) +
                get_random_exercises("Arka Kol", 2)
            )
        elif day == 4:
            day_plan = get_random_exercises("Bacak", 5)
        elif day == 6:
            day_plan = (
                get_random_exercises("Arka Kol", 3) +
                get_random_exercises("Biceps", 3) +
                get_random_exercises("On Kol", 3)
            )
        elif day == 7:
            day_plan = (
                get_random_exercises("Bacak", 4) +
                get_random_exercises("Arka Kol", 3) +
                get_random_exercises("Biceps", 3)
            )
        else:
            day_plan = []

        # Gün planını uygun formatta düzenle
        workout_plan[day_key] = [
            {
                "bolge": exercise.body_part,
                "hareket_adi": exercise.exercise_name,
                "set_sayisi": max(1, exercise.sets),
                "tekrar_sayisi": max(5, exercise.reps),
                "ekipman": exercise.equipment or "None"
            }
            for exercise in day_plan
        ]

    return workout_plan
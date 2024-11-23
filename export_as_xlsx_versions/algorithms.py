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
    """
    Kullanıcının bilgilerine göre bir workout planı oluşturur.

    Args:
    - user_id: Kullanıcı ID'si
    - days: Program süresi (gün sayısı)
    - db: Veritabanı bağlantısı

    Returns:
    - workout_plan: Günlere göre egzersiz planı
    """
    # Kullanıcı bilgilerini veritabanından alıyoruz
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise ValueError("Kullanıcı bulunamadı")

    # Kullanıcı özelliklerine göre egzersiz ayarları yapalım (örnek)
    fitness_level = user.fitness_level
    weight = user.weight
    age = user.age
    bmi = user.bmi

    # BMI'ye göre egzersiz yoğunluğu ayarlama
    if bmi < 18.5:
        exercise_intensity = 'low'  # Zayıf kullanıcılar için düşük yoğunluklu egzersizler
    elif 18.5 <= bmi < 24.9:
        exercise_intensity = 'medium'  # Normal kilolu kullanıcılar için orta yoğunluklu egzersizler
    elif 25 <= bmi < 29.9:
        exercise_intensity = 'high'  # Fazla kilolu kullanıcılar için yüksek yoğunluklu egzersizler
    else:
        exercise_intensity = 'very high'  # Obez kullanıcılar için çok yüksek yoğunluklu egzersizler

    # Egzersizlerin bulunduğu tablodan gerekli verileri alıyoruz
    exercises = db.query(Exercise).all()
    
    # Kullanıcı için oluşturulacak planı başlatıyoruz
    workout_plan = {}
    
    # Kullanıcıya uygun kas grupları
    body_parts = ["Gogus", "Omuz", "Biceps", "Arka Kol", "Sirt", "Bacak"]
    
    # Kullanıcı bilgilerine göre günlük egzersiz sayısını dinamik olarak ayarlıyoruz
    if age < 30:
        min_exercises_per_day = 4  # Genç kullanıcılar için en az 4 egzersiz
        max_exercises_per_day = 7  # Genç kullanıcılar için en fazla 7 egzersiz
    elif 30 <= age <= 50:
        min_exercises_per_day = 3  # Orta yaş grubuna göre en az 3 egzersiz
        max_exercises_per_day = 6  # Orta yaş grubu için en fazla 6 egzersiz
    else:
        min_exercises_per_day = 2  # 50 yaş ve üzeri için daha az egzersiz
        max_exercises_per_day = 5  # 50 yaş ve üzeri için daha az egzersiz

    # Kilo bilgisiyle yoğunluğu ayarlama
    if weight > 100:  # Ağırsız egzersizlere yönelmek
        min_exercises_per_day = max(min_exercises_per_day, 3)
        max_exercises_per_day = min(max_exercises_per_day, 5)
    elif weight < 60:  # Daha fazla egzersiz yapılabilir
        min_exercises_per_day = max(min_exercises_per_day, 4)
        max_exercises_per_day = min(max_exercises_per_day, 7)

    # Egzersizleri kullanıcıya göre (gün sayısına göre) dağıtıyoruz
    for day in range(1, days + 1):
        day_key = f"DAY{day}"
        workout_plan[day_key] = []

        # Her gün için farklı kas gruplarından birden fazla kas grubu seçiyoruz
        selected_body_parts = random.sample(body_parts, k=random.randint(2, 3))  # Her gün 2-3 kas grubu seçelim
        
        # Her seçilen kas grubu için egzersizleri rastgele seçiyoruz
        for body_part in selected_body_parts:
            # O kas grubundan uygun egzersizleri seçiyoruz
            body_part_exercises = [e for e in exercises if e.body_part == body_part]

            # Kullanıcı bilgilerine göre rastgele sayıda egzersiz seçiyoruz
            num_exercises = random.randint(min_exercises_per_day, max_exercises_per_day)
            
            # Egzersizleri rastgele seçiyoruz
            selected_exercises = random.sample(body_part_exercises, min(num_exercises, len(body_part_exercises)))
            
            # Egzersizleri kullanıcı seviyesine göre düzenliyoruz
            for exercise in selected_exercises:
                # Fitness seviyesini göz önünde bulundurarak zorluk belirlemesi yapıyoruz
                if fitness_level == "beginner":
                    sets, reps = exercise.sets - 1, exercise.reps - 2  # Başlangıç seviyesi
                elif fitness_level == "intermediate":
                    sets, reps = exercise.sets, exercise.reps  # Orta seviyede kalıyoruz
                else:  # Advanced
                    sets, reps = exercise.sets + 1, exercise.reps + 2  # İleri seviye

                # BMI'ye göre yoğunluğu belirliyoruz
                if exercise_intensity == 'low':
                    sets, reps = max(sets - 1, 1), max(reps - 2, 5)  # Düşük yoğunluklu egzersiz
                elif exercise_intensity == 'high':
                    sets, reps = min(sets + 1, 6), min(reps + 2, 15)  # Yüksek yoğunluklu egzersiz
                elif exercise_intensity == 'very high':
                    sets, reps = min(sets + 2, 8), min(reps + 3, 20)  # Çok yüksek yoğunluklu egzersiz

                workout_plan[day_key].append({
                    "bolge": exercise.body_part,
                    "hareket_adi": exercise.exercise_name,
                    "set_sayisi": sets,
                    "tekrar_sayisi": reps,
                    "ekipman": exercise.equipment
                })
    
    return workout_plan


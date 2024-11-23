import os
from algorithms import save_workout_plan_to_excel
from algorithms import generate_workout_plan
from unittest.mock import MagicMock


def test_save_empty_workout_plan():
    # Boş bir egzersiz planı
    workout_plan = {}
    filename = "test_empty_workout_plan.xlsx"
    
    save_workout_plan_to_excel(workout_plan, filename)
    
    # Dosyanın oluşturulduğunu doğrula
    assert os.path.exists(filename)
    
    # Dosyayı temizle
    os.remove(filename)

def test_save_workout_plan_with_rest_days():
    # Rest day içeren bir plan
    workout_plan = {
        "DAY1": [],
        "DAY2": [
            {"bolge": "Bacak", "hareket_adi": "Squat", "set_sayisi": 4, "tekrar_sayisi": 12, "ekipman": "Barbell"}
        ]
    }
    filename = "test_rest_day_plan.xlsx"
    save_workout_plan_to_excel(workout_plan, filename)
    
    # Dosyanın oluşturulduğunu doğrula
    assert os.path.exists(filename)
    
    # Dosyayı temizle
    os.remove(filename)

def test_generate_workout_plan_with_no_user():
    db = MagicMock()
    db.query().filter().first.return_value = None  # Kullanıcı bulunamadı
    
    # Kullanıcı olmadan hata döndürmesini bekliyoruz
    try:
        generate_workout_plan(user_id=999, days=7, db=db)
        assert False  # Hata vermezse test başarısız
    except ValueError as e:
        assert str(e) == "Kullanıcı bulunamadı"

def test_generate_workout_plan_with_high_bmi():
    db = MagicMock()

    # Mock kullanıcı bilgileri
    user_mock = MagicMock()
    user_mock.id = 1
    user_mock.fitness_level = "intermediate"
    user_mock.weight = 120
    user_mock.age = 35
    user_mock.bmi = 30  # Obez sınıfı
    db.query().filter().first.return_value = user_mock

    # Mock egzersiz bilgileri
    exercise_mock = MagicMock()
    exercise_mock.body_part = "Gogus"
    exercise_mock.exercise_name = "Push-Up"
    exercise_mock.sets = 3
    exercise_mock.reps = 10
    db.query().all.return_value = [exercise_mock]

    # Plan oluştur
    workout_plan = generate_workout_plan(user_id=1, days=5, db=db)
    assert len(workout_plan) == 5  # Planın 5 günlük olduğundan emin ol
    assert all("Gogus" in [e["bolge"] for e in day] for day in workout_plan.values())

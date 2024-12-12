from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from models import (
    Base, 
    User, 
    WorkoutPlan, 
    UserFitnessData, 
    WorkoutPlanResponse, 
    UserFitnessDataResponse, 
    UpdateUserData, 
    LoginRequest, 
    Coach, 
    StudentResponse, 
    UserResponse,
    CoachResponse,
    CoachSelectionRequest)
from algorithms import generate_workout_plan
from pydantic import BaseModel
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from datetime import datetime
from algorithms import save_workout_plan_to_excel
from fastapi.responses import FileResponse
import os, json


app = FastAPI()

DATABASE_URL = "sqlite:///./fitness.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def remove_file(filename: str):
    os.remove(filename)

@app.get("/export_workout_plan/{user_id}")
def export_workout_plan(user_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Fetch the user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch the workout plan
    workout_plan_record = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    if not workout_plan_record:
        raise HTTPException(status_code=404, detail="Workout plan not found")

    # Parse the workout data
    workout_plan = json.loads(workout_plan_record.workout_data)

    # Define filename
    filename = f"workout_plan_user_{user_id}.xlsx"

    # Save the workout plan to an Excel file
    save_workout_plan_to_excel(workout_plan, filename)

    # Ensure the file is properly deleted after being served
    background_tasks.add_task(remove_file, filename)

    return FileResponse(filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=filename)



'''

BELOW IS SAME


'''









@app.post("/generate_workout_plan/{user_id}", response_model=List[WorkoutPlanResponse])  # response_model kullanarak cevap modelini belirtiyoruz
def generate_workout_plan_for_user(user_id: int, user_data: UpdateUserData, db: Session = Depends(get_db)):
    # Kullanıcıyı veritabanından alıyoruz
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete any existing workout plan for the user
    existing_workout_plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    if existing_workout_plan:
        db.delete(existing_workout_plan)
        db.commit()
    
    # Kullanıcıyı veritabanında güncellenmiş verilerle güncelliyoruz
    user.age = user_data.age
    user.weight = user_data.weight
    user.height = user_data.height
    db.commit()  # Veritabanında güncelleme yapıyoruz

    # Workout planını oluşturuyoruz
    workout_plan = generate_workout_plan(user_id, user_data.days, db)  # 7 gün için plan oluşturuyoruz

    # Workout planını dönüştürerek response modeline uygun hale getiriyoruz
    workout_plan_response = []
    for day, exercises in workout_plan.items():
        day_data = {
            "day": day,
            "exercises": [
                {
                    "bolge": exercise.get("bolge", "Unknown"),
                    "hareket_adi": exercise.get("hareket_adi", "Unknown"),
                    "set_sayisi": exercise.get("set_sayisi", 0),
                    "tekrar_sayisi": exercise.get("tekrar_sayisi", 0),
                    "ekipman": exercise.get("ekipman", "None")
                }
                for exercise in exercises
            ]
        }
        workout_plan_response.append(day_data)
    
        # Workout planındaki her egzersizi UserFitnessData tablosuna kaydediyoruz
        for exercise in exercises:
            new_fitness_data = UserFitnessData(
                user_id=user.id,
                date=datetime.today(),
                exercise_name=exercise.get("hareket_adi", "Unknown"),
                weight=0,  # Başlangıçta ağırlık verisi yoksa 0 olarak kaydedebiliriz
                sets=exercise.get("tekrar_sayisi", 0),
                reps=exercise.get("ekipman", "None")
            )
            db.add(new_fitness_data)

    # Workout planını veritabanına kaydediyoruz
    new_workout_plan = WorkoutPlan(user_id=user.id, workout_data=json.dumps(workout_plan))  # JSON formatında kaydediyoruz
    db.add(new_workout_plan)
    db.commit()
    
    # Endpoint cevap olarak workout planı döndürüyor
    return workout_plan_response


# Endpoint: Kullanıcının belirli bir egzersiziyle ilgili gelişim verilerini çekme
@app.get("/user_fitness_data/{user_id}/exercise/{exercise_name}", response_model=List[UserFitnessDataResponse])
def get_user_exercise_data(user_id: int, exercise_name: str, db: Session = Depends(get_db)):
    # Kullanıcı ve egzersiz adıyla eşleşen verileri sorguluyoruz
    user_fitness_data = db.query(UserFitnessData).filter(
        UserFitnessData.user_id == user_id,
        UserFitnessData.exercise_name == exercise_name
    ).order_by(UserFitnessData.date).all()

    # Eğer veri bulunmazsa 404 hatası döndürüyoruz
    if not user_fitness_data:
        raise HTTPException(status_code=404, detail="No data found for the given user and exercise")

    # Kullanıcı fitness verilerini döndürüyoruz
    return user_fitness_data

@app.put("/update_user_data/{user_id}")
def update_user_data(user_id: int, user_data: UpdateUserData, db: Session = Depends(get_db)):
    # Kullanıcıyı veritabanından alıyoruz
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Gelen yeni verileri kullanıcıya uyguluyoruz
    user.age = user_data.age
    user.weight = user_data.weight
    user.height = user_data.height
    
    db.commit()  # Veritabanında güncelleme yapıyoruz
    
    return {"message": "User data updated successfully"}

@app.get("/workout_plans/{user_id}")
def get_workout_plans(user_id: int, db: Session = Depends(get_db)):
    workout_plans = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).all()
    if not workout_plans:
        raise HTTPException(status_code=404, detail="Workout plans not found")
    
    return workout_plans


@app.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # Önce Users tablosunda kontrol edelim
    user = db.query(User).filter(User.name == credentials.name, User.password == credentials.password).first()
    if user:
        return {"id": user.id, "role": "user"}  # Kullanıcı bulundu

    # Eğer Users tablosunda bulunmazsa Coaches tablosunda arayalım
    coach = db.query(Coach).filter(Coach.name == credentials.name, Coach.password == credentials.password).first()
    if coach:
        return {"id": coach.id, "role": "coach"}  # Koç bulundu

    # Her iki tabloda da eşleşme yoksa hata döndürelim
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/coach/{coach_id}/students", response_model=List[StudentResponse])
def get_students_by_coach(coach_id: int, db: Session = Depends(get_db)):
    # Koçu kontrol et
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    # Koça bağlı tüm öğrencileri getir
    students = db.query(User).filter(User.coach_id == coach_id).all()

    # Eğer öğrenci bulunmazsa boş liste dönebiliriz
    if not students:
        return []

    return students

@app.get("/user_info/{user_id}", response_model=UserResponse)
def get_user_info(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@app.get("/coaches", response_model=List[CoachResponse])
def get_all_coaches(db: Session = Depends(get_db)):
    coaches = db.query(Coach).all()
    return coaches


@app.post("/select_coach")
def select_coach(request: CoachSelectionRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    coach = db.query(Coach).filter(Coach.id == request.coach_id).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    
    user.coach_id = request.coach_id
    db.commit()
    return {"message": "Coach selected successfully"}


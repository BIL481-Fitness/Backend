from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Base, User, WorkoutPlan, UserFitnessData, WorkoutPlanResponse, UserFitnessDataResponse, UpdateUserData
from algorithms import generate_workout_plan
from pydantic import BaseModel
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from datetime import datetime

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



@app.post("/generate_workout_plan/{user_id}", response_model=List[WorkoutPlanResponse])  # response_model kullanarak cevap modelini belirtiyoruz
def generate_workout_plan_for_user(user_id: int, user_data: UpdateUserData, db: Session = Depends(get_db)):
    # Kullanıcıyı veritabanından alıyoruz
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
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
                    "bolge": exercise["bolge"],
                    "hareket_adi": exercise["hareket_adi"],
                    "set_sayisi": exercise["set_sayisi"],
                    "tekrar_sayisi": exercise["tekrar_sayisi"],
                    "ekipman": exercise["ekipman"]
                }
                for exercise in exercises
            ]
        }
        workout_plan_response.append(day_data)
    
        # Workout planındaki her egzersizi UserFitnessData tablosuna kaydediyoruz
        for exercise in exercises:
            new_fitness_data = UserFitnessData(
                user_id=user.id,
                date=datetime.date.today(),  # Bugünün tarihi ile kaydediyoruz
                exercise_name=exercise["hareket_adi"],
                weight=0,  # Başlangıçta ağırlık verisi yoksa 0 olarak kaydedebiliriz
                sets=exercise["set_sayisi"],
                reps=exercise["tekrar_sayisi"]
            )
            db.add(new_fitness_data)
    # Workout planını veritabanına kaydediyoruz
    new_workout_plan = WorkoutPlan(user_id=user.id, workout_data=str(workout_plan))  # JSON formatında kaydediyoruz
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

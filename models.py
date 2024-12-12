from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List
from datetime import date

Base = declarative_base()

class Coach(Base):
    __tablename__ = 'Coaches'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    specialization = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    experience_level = Column(Integer)
    password = Column(String, nullable=False)

class User(Base):
    __tablename__ = 'Users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    fitness_level = Column(Integer)
    bmi = Column(Float)
    coach_id = Column(Integer, ForeignKey('Coaches.id'))
    daily_calories = Column(Integer)
    goal = Column(String)
    password = Column(String, nullable=False) 
    
    coach = relationship('Coach', backref='users')

class WorkoutPlan(Base):
    __tablename__ = 'WorkoutPlans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    workout_data = Column(String)  # JSON format for workout plan
    
    user = relationship('User', backref='workout_plans')

class UserFitnessData(Base):
    __tablename__ = 'UserFitnessData'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    date = Column(Date)
    exercise_name = Column(String)
    weight = Column(Float)
    sets = Column(Integer)
    reps = Column(Integer)
    
    user = relationship('User', backref='fitness_data')

class Exercise(Base):
    __tablename__ = 'Exercises'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_name = Column(String, nullable=False)
    body_part = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)
    equipment = Column(String)

# Pydantic models
class ExerciseResponse(BaseModel):
    bolge: str  # Kas grubu
    hareket_adi: str  # Egzersiz adı
    set_sayisi: int  # Set sayısı
    tekrar_sayisi: int  # Tekrar sayısı
    ekipman: str  # Kullanılacak ekipman

class WorkoutPlanResponse(BaseModel):
    day: str  # Gün numarası (DAY1, DAY2, ...)
    exercises: List[ExerciseResponse]  # Günün egzersizleri

class UserFitnessDataResponse(BaseModel):
    date: date
    exercise_name: str
    sets: int
    reps: str

    class Config:
        from_attributes = True  # ORM modelinden veri alabilmesini sağlıyor

class UpdateUserData(BaseModel):
    age: int
    weight: float
    height: float
    days: int = None  # Bu parametre isteğe bağlıdır; workout planı oluşturulacaksa sağlanmalıdır

class LoginRequest(BaseModel):
    name: str
    password: str

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    weight: float
    height: float
    fitness_level: int
    bmi: float
    daily_calories: int
    goal: str

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    weight: float
    height: float
    fitness_level: int
    bmi: float
    daily_calories: int
    goal: str
    coach_id: int

    class Config:
        from_attributes = True

class CoachResponse(BaseModel):
    id: int
    name: str
    specialization: str
    age: int
    weight: float
    height: float
    experience_level: int

    class Config:
        from_attributes = True

class CoachSelectionRequest(BaseModel):
    user_id: int
    coach_id: int
-- Creating the Coaches table
CREATE TABLE IF NOT EXISTS Coaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT,
    age INTEGER,
    weight REAL,
    height REAL,
    experience_level INTEGER
);

-- Creating the Users table
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    weight REAL,
    height REAL,
    fitness_level INTEGER,
    bmi REAL,
    coach_id INTEGER,
    daily_calories INTEGER,
    goal TEXT,
    FOREIGN KEY (coach_id) REFERENCES Coaches(id)
);

-- Creating the WorkoutPlans table
CREATE TABLE IF NOT EXISTS WorkoutPlans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    workout_data TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Creating the UserFitnessData table
CREATE TABLE IF NOT EXISTS UserFitnessData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE,
    exercise_name TEXT,
    weight REAL,
    sets INTEGER,
    reps INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Creating the Exercises table
CREATE TABLE IF NOT EXISTS Exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_name TEXT NOT NULL,
    body_part TEXT,
    sets INTEGER,
    reps INTEGER,
    equipment TEXT
);



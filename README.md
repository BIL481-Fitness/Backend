### Fitness Database

This project contains a SQLite database designed for managing fitness-related data, such as coaches, users, exercises, and workout plans. Below is an overview of the tables and their sample data:

---

### **Coaches**
| Column            | Description                   |
|-------------------|-------------------------------|
| `id`              | Unique identifier for coaches |
| `name`            | Name of the coach             |
| `specialization`  | Areas of expertise            |
| `age`             | Age of the coach              |
| `weight`          | Weight of the coach           |
| `height`          | Height of the coach           |
| `experience_level`| Experience level (1-5)        |
| `passowrd`        | Password                      |
**Sample Data:**
```plaintext
(1, 'Sibel Demir', 'Strength Training, CrossFit', 29, 71.06, 179.35, 5, 1234)
(2, 'Cem Kilic', 'Nutrition, Bodybuilding', 27, 85.96, 189.02, 3, 1234)
(3, 'Hakan Arslan', 'Cardio, Endurance', 35, 75.0, 168.42, 2, 1234)
(4, 'Berk Demir', 'Nutrition, Weight Loss', 35, 82.53, 189.96, 1, 1234)
(5, 'Mustafa Demir', 'Endurance, Strength Training', 32, 84.87, 168.71, 3, 1234)
```

---

### **sqlite_sequence**
| Column | Description                            |
|--------|----------------------------------------|
| `name` | Name of the table                     |
| `seq`  | Last used ID for auto-increment fields |

**Sample Data:**
```plaintext
('Coaches', 5)
('Users', 100)
('Exercises', 70)
```

---

### **Users**
| Column           | Description                               |
|------------------|-------------------------------------------|
| `id`             | Unique identifier for users              |
| `name`           | Name of the user                         |
| `age`            | Age of the user                          |
| `weight`         | Weight of the user                       |
| `height`         | Height of the user                       |
| `fitness_level`  | Fitness level (Beginner/Intermediate/Advanced) |
| `bmi`            | Body Mass Index                         |
| `coach_id`       | ID of the assigned coach                 |
| `daily_calories` | Daily calorie goal                       |
| `goal`           | Fitness goal (e.g., Weight Loss, Muscle Gain) |
| `passowrd`       | Password                      |

**Sample Data:**
```plaintext
(1, 'Ayse Guler', 37, 87.38, 153.42, '2', 37.12, 5, 2500, 'Muscle Gain', 1234)
(2, 'Emre Ozturk', 55, 63.72, 176.64, '2', 20.42, 1, 2200, 'Endurance', 1234)
(3, 'Ayse Aydin', 23, 64.57, 163.07, '1', 24.28, 1, 2300, 'Weight Loss', 1234)
(4, 'Cem Celik', 56, 96.88, 173.53, '1', 32.17, 5, 2400, 'Weight Loss', 1234)
(5, 'Oguz Arslan', 25, 83.85, 160.47, '2', 32.56, 5, 2100, 'Weight Loss', 1234)
```

---

### **WorkoutPlans**
| Column       | Description                   |
|--------------|-------------------------------|
| `id`         | Unique identifier for plans  |
| `user_id`    | ID of the user                |
| `workout_data` | Planned workout details    |

_No sample data provided._

---

### **UserFitnessData**
| Column        | Description                     |
|---------------|---------------------------------|
| `id`          | Unique identifier for records  |
| `user_id`     | ID of the user                 |
| `date`        | Date of the workout            |
| `exercise_name` | Name of the exercise          |
| `weight`      | Weight used in the exercise    |
| `sets`        | Number of sets                 |
| `reps`        | Number of repetitions          |

_No sample data provided._

---

### **Exercises**
| Column          | Description                   |
|-----------------|-------------------------------|
| `id`            | Unique identifier for exercises |
| `exercise_name` | Name of the exercise           |
| `body_part`     | Targeted body part             |
| `sets`          | Number of sets                |
| `reps`          | Number of repetitions         |
| `equipment`     | Equipment used                |

**Sample Data:**
```plaintext
(1, 'Bench Press', 'Gogus', 3, 8, 'Barbell')
(2, 'Incline Bench Press', 'Gogus', 3, 8, 'Barbell')
(3, 'Chest Fly', 'Gogus', 4, 10, 'Dumbbell')
(4, 'Push-Up', 'Gogus', 3, 10, 'Bodyweight')
(5, 'Cable Crossover', 'Gogus', 4, 8, 'Cable')
```

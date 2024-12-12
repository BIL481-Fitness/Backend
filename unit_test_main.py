from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)
'''
GENERATE WORKOUT
'''
def test_generate_workout_plan_for_existing_user():
    user_data = {
        "age": 25,
        "weight": 70,
        "height": 175,
        "days": 7
    }
    response = client.post("/generate_workout_plan/1", json=user_data)
    assert response.status_code == 200
    assert len(response.json()) == 7  # 7 günlük plan bekleniyor

def test_generate_workout_plan_for_nonexistent_user():
    user_data = {
        "age": 30,
        "weight": 80,
        "height": 180,
        "days": 5
    }
    response = client.post("/generate_workout_plan/999", json=user_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


'''
EXPORT WORKOUT PLAN
'''
def test_export_workout_plan_success():
    response = client.get("/export_workout_plan/1")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

def test_export_workout_plan_with_invalid_user():
    response = client.get("/export_workout_plan/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}



'''
UPDATE USER DATA
'''

def test_update_user_data_success():
    user_data = {
        "age": 30,
        "weight": 85,
        "height": 175
    }
    response = client.put("/update_user_data/1", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User data updated successfully"}

def test_update_user_data_invalid_user():
    user_data = {
        "age": 40,
        "weight": 90,
        "height": 180
    }
    response = client.put("/update_user_data/999", json=user_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


'''
GET USER DATA
'''

def test_get_user_exercise_data_with_existing_data():
    response = client.get("/user_fitness_data/1/exercise/Push-Up")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Veri içermelidir

def test_get_user_exercise_data_no_data():
    response = client.get("/user_fitness_data/1/exercise/NonexistentExercise")
    assert response.status_code == 404
    assert response.json() == {"detail": "No data found for the given user and exercise"}


'''
GET ALL COACHES
'''
def test_get_all_coaches():
    response = client.get("/coaches")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure the response is a list
    if response.json():  # If there are coaches in the response
        coach = response.json()[0]
        assert "id" in coach
        assert "name" in coach
        assert "specialization" in coach
        assert "age" in coach
        assert "weight" in coach
        assert "height" in coach
        assert "experience_level" in coach
    
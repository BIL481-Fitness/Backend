SELECT * FROM Users;

UPDATE Users SET bmi = REPLACE(bmi, ',', '.');
UPDATE Users SET height = REPLACE(height, ',', '.');
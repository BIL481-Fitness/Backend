SELECT * FROM Coaches;

UPDATE Coaches SET weight = REPLACE(weight, ',', '.');
UPDATE Coaches SET height = REPLACE(height, ',', '.');
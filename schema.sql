PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE quizz (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
	question VARCHAR (800),
	man_temp INTEGER,
	woman_temp INTEGER,
	status INTEGER
);
COMMIT;
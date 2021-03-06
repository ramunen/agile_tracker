DROP TABLE IF EXISTS developers;
DROP TABLE IF EXISTS stories;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS logs;


CREATE TABLE developers (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name_surname CHAR NOT NULL);
CREATE TABLE stories (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title CHAR NOT NULL,
                    content CHAR, 
                    estimate NUMERIC, 
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                    modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    developer_id INTEGER NOT NULL, 
                    story_id INTEGER NOT NULL, 
                    title CHAR NOT NULL, 
                    content CHAR, 
                    estimate NUMERIC, 
                    iteration NUMERIC,
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                    modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (developer_id) REFERENCES developers (id), 
                    FOREIGN KEY (story_id) REFERENCES stories (id));
CREATE TABLE logs (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    developer_id INTEGER NOT NULL, 
                    task_id INTEGER NOT NULL, 
                    work_date DATE NOT NULL, 
                    content CHAR, 
                    actual NUMERIC NOT NULL, 
                    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                    modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                    FOREIGN KEY (developer_id) REFERENCES developers (id), 
                    FOREIGN KEY (task_id) REFERENCES tasks (id));

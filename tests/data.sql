INSERT INTO developers (name_surname)
VALUES
    ('John Smith'),
    ('Janne Jalonen'),
    ('Anna Teesti'),
    ('James Joyce');

INSERT INTO stories (title, content, estimate)
VALUES
    ('Story one', 'Some descrioption', '200'),
    ('Story two', 'Also some descrioption', '55');

INSERT INTO tasks (developer_id, story_id, title, content, estimate, iteration)
VALUES
    ('1', '1', 'Task one', 'Some descrioption', '65' , '1b'),
    ('2', '1', 'Task two', 'Some descrioption', '716' , '1b'),
    ('2', '2', 'Task three', 'Some descrioption', '80' , '1b'),
    ('3', '2', 'Task four', 'Some descrioption', '204' , '1b'),
    ('4', '2', 'Task five', 'Also some descrioption', '400', '1a');

INSERT INTO logs (developer_id, task_id, work_date, content, actual)
VALUES
    ('2', '1', '2021-02-23', 'Some work', '50'),
    ('3', '1', '2021-02-23', 'Some more work', '100' ),
    ('1', '2', '2021-02-24', 'Some more more work', '300'),
    ('1', '2', '2021-02-24', 'Some more more more work', '500' ),
    ('1', '4', '2021-02-25', 'Some more more more work', '204'),
    ('1', '5', '2021-02-26', 'Some more more more more work', '400');

USE todo_list;

CREATE TABLE tasks(
    id INT PRIMARY KEY AUTO_INCREMENT,
    task VARCHAR(255),
    status VARCHAR(255)
);

INSERT INTO tasks VALUES(1, "finish cs411 hw", "Todo");

SELECT * from tasks;

INSERT INTO tasks(task, status) VALUES("finish cs411 project stage 4", "Todo");

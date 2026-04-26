SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;
SET AUTOCOMMIT = 0;

INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Christopher', 'Turner', 1);
INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Margaret', 'Osborne', 2);
INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Stephanie', 'Davis', 3);
INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Jake', 'Meyer', 4);
INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Margaret', 'Mcgrath', 5);
INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Bryan', 'Davis', 6);
INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Brandon', 'Marsh', 7);
INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Gary', 'Brown', 8);
INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Wendy', 'Smith', 9);
INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('Leonard', 'Navarro', 10);

COMMIT;
SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;
SET AUTOCOMMIT = 1;

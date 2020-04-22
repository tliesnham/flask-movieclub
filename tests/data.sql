INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:150000$34SUZlzr$e6be7b5d2b2cc7ba01b61f8006be1fdb83ccc5b6042bf3d9a9da98ec332256e4'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO movie (title, synopsis, released, age_rating, user_id, created)
VALUES
  ('Yes Man', 'Synopsis', 2008, '12A', 1, '2020-01-01 00:00:00');
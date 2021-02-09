CREATE TABLE notifications(
  id TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  last_notified TEXT NOT NULL,

  PRIMARY KEY(id, user_id)
);

CREATE TABLE cache(
  key TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  value TEXT NOT NULL,

  PRIMARY KEY(key, user_id)
);

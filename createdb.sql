CREATE TABLE notifications(
  id TEXT PRIMARY KEY,
  last_notified TEXT NOT NULL
);

CREATE TABLE cache(
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

DROP TABLE IF EXISTS schedules;

CREATE TABLE schedules (
  crn INT PRIMARY KEY,
  course_id TEXT NOT NULL,
  component_id TEXT,
  start_date TEXT,
  end_date TEXT,
  day TEXT,
  start_time TEXT,
  duration TEXT,
  pattern_day TEXT,
  pattern_start_time TEXT,
  pattern_duration TEXT,
  building_id TEXT,
  room_number TEXT,
  professor TEXT
)

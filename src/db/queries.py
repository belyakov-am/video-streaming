CREATE_VIDEOS_TABLE = """
CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY,
    name TEXT,
    description TEXT
)
"""

INSERT_VIDEO_INFO = """
INSERT INTO videos(id, name, description) 
VALUES($1, $2, $3)
"""
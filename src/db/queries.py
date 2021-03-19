CREATE_VIDEOS_TABLE = """
CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY,
    name TEXT,
    description TEXT
)
"""
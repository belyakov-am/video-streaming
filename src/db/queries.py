CREATE_VIDEOS_TABLE = """
CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY,
    name TEXT,
    storage_video_uid TEXT,
    description TEXT
)
"""

INSERT_VIDEO_INFO = """
INSERT INTO videos(id, name, storage_video_uid, description)
VALUES($1, $2, $3, $4)
"""

SELECT_VIDEO_INFO = """
SELECT * from videos
"""
CREATE TABLE IF NOT EXISTS post_data (
    id TEXT PRIMARY KEY,
    title TEXT,
    selftext TEXT NULL,
    score INTEGER,
    post_url TEXT NULL,
    distinguished TEXT NULL,
    locked BOOLEAN,
    is_original_content BOOLEAN,
    spoiler BOOLEAN,
    author TEXT,
    created_utc TIMESTAMP,
    num_comments INTEGER,
    upvote_ratio DOUBLE PRECISION,
    subreddit TEXT
);

CREATE TABLE IF NOT EXISTS comment_data (
    post_id TEXT REFERENCES post_data (id),
    comment_id TEXT PRIMARY KEY,
    body TEXT,
    author TEXT,
    score INTEGER,
    distinguished TEXT NULL,
    edited BOOLEAN NULL,
    created_utc TIMESTAMP,
    is_top_level BOOLEAN,
    depth INTEGER,
    is_submitter BOOLEAN
);
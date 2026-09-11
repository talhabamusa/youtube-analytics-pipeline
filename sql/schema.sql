CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(20) NOT NULL,
    trending_date DATE,
    title TEXT,
    channel_title VARCHAR(255),
    category_id INT,
    category_name VARCHAR(100),
    publish_time TIMESTAMP,
    tags TEXT,
    views BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    comment_count BIGINT,
    engagement_rate FLOAT,
    country VARCHAR(2),
    comment_disabled BOOLEAN,
    ratings_disabled BOOLEAN
);

CREATE INDEX idx_video_id ON videos (video_id);
CREATE INDEX idc_country ON videos (country);
CREATE INDEX idx_category_id ON videos (category_name);

-- Top 10 categories by average engagement rate
SELECT category_name, Name(AVG(engagement_rate)::numeric,4) AS avg_engagement, COUNT(*) AS video_count
FROM videos
GROUP BY category_name
ORDER BY avg_engagement DESC
LIMIT 10;

-- Does country affect engagement rate?
SELECT country, Name(AVG(engagement_rate)::numeric,4) AS avg_engagement, ROUND(AVG(views)::numeric,0) AS avg_views
FROM videos
GROUP BY country
ORDER BY avg_engagement DESC;

-- Which category gets the most views on average?
SELECT category_name, ROUND(AVG(views)::numeric,0) AS avg_views
FROM videos
GROUP BY category_name
ORDER BY avg_views DESC
LIMIT 10;
SELECT * FROM earthquake_analysis.earthquakes_cleaned_26features;
SELECT id, time, place, mag, depth_km
SELECT *
FROM earthquake_analysis.earthquakes_cleaned_26features
ORDER BY mag DESC
LIMIT 10;
SELECT id, time, place, depth_km, mag
FROM earthquake_analysis.earthquakes_cleaned_26features
ORDER BY depth_km DESC
LIMIT 10;

SHOW COLUMNS FROM earthquake_analysis.earthquakes_cleaned_26features;
SELECT time, place, country, mag, depth_km
FROM earthquake_analysis.earthquakes_cleaned_26features
ORDER BY mag DESC
LIMIT 10;
SELECT time, place, country, mag, depth_km
FROM earthquake_analysis.earthquakes_cleaned_26features
ORDER BY depth_km DESC
LIMIT 10;
SELECT time, place, country, mag, depth_km
FROM earthquake_analysis.earthquakes_cleaned_26features
WHERE depth_km < 50
  AND mag > 7.5
ORDER BY mag DESC;
SELECT 
    CASE
        WHEN country IN ('Japan', 'China', 'India', 'Indonesia', 'Nepal', 'Turkey', 'Philippines', 'Iran') THEN 'Asia'
        WHEN country IN ('USA', 'Mexico', 'Canada', 'Chile', 'Peru', 'Guatemala', 'Costa Rica') THEN 'North America'
        WHEN country IN ('Argentina', 'Brazil', 'Ecuador', 'Colombia') THEN 'South America'
        WHEN country IN ('Italy', 'Greece', 'Portugal', 'Spain', 'France') THEN 'Europe'
        WHEN country IN ('New Zealand', 'Australia', 'Fiji', 'Papua New Guinea') THEN 'Oceania'
        WHEN country IN ('Egypt', 'Morocco', 'Algeria', 'Ethiopia') THEN 'Africa'
        ELSE 'Other'
    END AS continent,
    AVG(depth_km) AS avg_depth
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY continent
ORDER BY avg_depth DESC;
SELECT 
    magType,
    AVG(mag) AS avg_magnitude
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY magType
ORDER BY avg_magnitude DESC;
SELECT year, COUNT(*) AS earthquake_count
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY year
ORDER BY earthquake_count DESC
LIMIT 1;
SELECT year, COUNT(*) AS earthquake_count
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY year
ORDER BY earthquake_count DESC
LIMIT 1;
SELECT month, COUNT(*) AS earthquake_count
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY month
ORDER BY earthquake_count DESC
LIMIT 1;
SELECT day_of_week, COUNT(*) AS earthquake_count
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY day_of_week
ORDER BY earthquake_count DESC
LIMIT 1;
SELECT hour, COUNT(*) AS earthquake_count
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY hour
ORDER BY hour;
SELECT net, COUNT(*) AS report_count
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY net
ORDER BY report_count DESC
LIMIT 1;
SELECT type, COUNT(*) AS count
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY type
ORDER BY count DESC;
SELECT year, COUNT(*) AS tsunami_count
FROM earthquake_analysis.earthquakes_cleaned_26features
WHERE tsunami = 1
GROUP BY year
ORDER BY tsunami_count DESC;
SELECT alert, COUNT(*) AS alert_count
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY alert
ORDER BY alert_count DESC;
SELECT country, AVG(mag) AS avg_magnitude
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY country
ORDER BY avg_magnitude DESC
LIMIT 5;
SELECT country, month
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY country, month
HAVING COUNT(DISTINCT depth_category) >= 2;
SELECT 
    year,
    COUNT(*) AS total_quakes,
    LAG(COUNT(*)) OVER (ORDER BY year) AS previous_year_quakes,
    ROUND(
        ( (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year)) 
          / LAG(COUNT(*)) OVER (ORDER BY year) ) * 100,
        2
    ) AS growth_rate_percent
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY year
ORDER BY year;
SELECT 
    country,
    COUNT(*) AS earthquake_count,
    AVG(mag) AS avg_magnitude
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY country
ORDER BY earthquake_count DESC, avg_magnitude DESC
LIMIT 3;
SELECT 
    country,
    AVG(depth_km) AS avg_depth_near_equator
FROM earthquake_analysis.earthquakes_cleaned_26features
WHERE latitude BETWEEN -5 AND 5
GROUP BY country
ORDER BY avg_depth_near_equator DESC;
SELECT 
    country,
    SUM(CASE WHEN depth_category = 'shallow' THEN 1 ELSE 0 END) AS shallow_count,
    SUM(CASE WHEN depth_category = 'deep' THEN 1 ELSE 0 END) AS deep_count,
    ROUND(
        SUM(CASE WHEN depth_category = 'shallow' THEN 1 ELSE 0 END) /
        NULLIF(SUM(CASE WHEN depth_category = 'deep' THEN 1 ELSE 0 END), 0), 
        2
    ) AS shallow_to_deep_ratio
FROM earthquake_analysis.earthquakes_cleaned_26features
GROUP BY country
ORDER BY shallow_to_deep_ratio DESC;
SELECT 
    AVG(CASE WHEN tsunami = 1 THEN mag END) AS avg_mag_tsunami,
    AVG(CASE WHEN tsunami = 0 THEN mag END) AS avg_mag_no_tsunami,
    (AVG(CASE WHEN tsunami = 1 THEN mag END) -
     AVG(CASE WHEN tsunami = 0 THEN mag END)) AS magnitude_difference
FROM earthquake_analysis.earthquakes_cleaned_26features;
SELECT 
    time,
    place,
    country,
    rms,
    gap,
    (rms + gap) AS error_score
FROM earthquake_analysis.earthquakes_cleaned_26features
ORDER BY error_score DESC
LIMIT 20;
SELECT VERSION();
WITH quake_pairs AS (
    SELECT
        time,
        latitude,
        longitude,
        LAG(time) OVER (ORDER BY time) AS prev_time,
        LAG(latitude) OVER (ORDER BY time) AS prev_latitude,
        LAG(longitude) OVER (ORDER BY time) AS prev_longitude
    FROM earthquake_analysis.earthquakes_cleaned_26features
)

SELECT
    time AS current_event_time,
    prev_time AS previous_event_time,
    latitude,
    longitude,
    prev_latitude,
    prev_longitude,
    TIMESTAMPDIFF(MINUTE, prev_time, time) AS time_difference_minutes
FROM quake_pairs
WHERE prev_time IS NOT NULL
  AND TIMESTAMPDIFF(MINUTE, prev_time, time) <= 60   -- within 1 hour
  AND ABS(latitude - prev_latitude) <= 0.5           -- approx 50 km lat difference
  AND ABS(longitude - prev_longitude) <= 0.5;        -- approx 50 km lon difference
  SELECT 
    country,
    COUNT(*) AS deep_quakes
FROM earthquake_analysis.earthquakes_cleaned_26features
WHERE depth_km > 300
GROUP BY country
ORDER BY deep_quakes DESC;













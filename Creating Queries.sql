-- Retrieve All Users Information
SELECT * FROM Users;


-- Find Posts by Specific User
SELECT * FROM Posts
WHERE user_id = (SELECT User_id FROM Users WHERE Username = 'user8');

-- Count Total Posts by Each User
SELECT user_id, COUNT(post_id) AS Total_Posts
FROM Posts
GROUP BY user_id;


-- Get Posts with Specific Topic
SELECT p.*
FROM Posts p
JOIN Topic_Posts tp ON p.post_id = tp.post_id
WHERE tp.Topic_ID = (SELECT Topic_ID FROM Topic WHERE Name = 'Databases');

-- Retrieve Comments for a Specific Post
SELECT * FROM Comments
WHERE Post_id = (SELECT post_id FROM Posts WHERE post_id = 12);

-- List Top 5 Trending Posts
SELECT p.*, tp.Score
FROM Posts p
JOIN Trending_Posts tp ON p.post_id = tp.post_id
ORDER BY tp.Score DESC
OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY;

-- Find Users Followed by a Specific User
SELECT u.*
FROM Users u
JOIN Follow f ON u.User_id = f.Following_id
WHERE f.Follower_id = (SELECT User_id FROM Users WHERE Username = 'user2');


-- Count Reactions and Comments on Each Post
SELECT p.post_id,
       COUNT(DISTINCT c.Comment_id) AS Total_Comments,
       COUNT(DISTINCT r.Reaction_id) AS Total_Reactions
FROM Posts p
LEFT JOIN Comments c ON p.post_id = c.Post_id
LEFT JOIN Post_Reaction r ON p.post_id = r.Post_id
GROUP BY p.post_id;


-- Get User Preferences
SELECT * FROM User_Preferences
WHERE user_Id = (SELECT User_id FROM Users WHERE Username = 'user1');


-- Aggregate Engagement Metrics for All Posts
SELECT p.post_id,
       SUM(em.Like_Count) AS Total_Likes,
       SUM(em.Comment_Count) AS Total_Comments,
       SUM(em.Share_Count) AS Total_Shares
FROM Posts p
LEFT JOIN Engagement_Metrics em ON p.post_id = em.Post_ID
GROUP BY p.post_id;


-- Retrieve All Notifications for a User
SELECT * FROM Notification
WHERE user_Id = (SELECT User_id FROM Users WHERE Username = 'user1')
ORDER BY Notification_date DESC;


-- Get Sentiments for Comments on a Post
SELECT c.Comment_Text, s.Sentiment_Score, s.Sentiment_Label
FROM Comments c
JOIN Sentiments s ON c.Comment_id = s.comment_id
WHERE c.Post_id = (SELECT post_id FROM Posts WHERE post_id = 3);


-- Retrieve a User's Saved Posts
SELECT p.*
FROM Posts p
JOIN Saved_Post sp ON p.post_id = sp.Post_id
WHERE sp.user_id = (SELECT User_id FROM Users WHERE Username = 'user6');

-- Posts with Their Top Reaction Count
SELECT p.post_id, COUNT(r.Reaction_id) AS Total_Reactions
FROM Posts p
LEFT JOIN Post_Reaction r ON p.post_id = r.Post_id
GROUP BY p.post_id
ORDER BY Total_Reactions DESC;

-- Users and Their Follower Counts
SELECT u.Username, COUNT(f.Follower_id) AS Follower_Count
FROM Users u
LEFT JOIN Follow f ON u.User_id = f.Following_id
GROUP BY u.Username;

-- Engagement Metrics for Posts
SELECT p.post_id, 
       SUM(em.Like_Count) AS Total_Likes, 
       SUM(em.Comment_Count) AS Total_Comments,
       SUM(em.Share_Count) AS Total_Shares
FROM Posts p
LEFT JOIN Engagement_Metrics em ON p.post_id = em.Post_ID
GROUP BY p.post_id;


-- Identify Users with Badges
SELECT u.Username, b.Badge_Name
FROM Users u
JOIN Badge b ON u.User_id = b.user_Id
ORDER BY u.Username;


-- Trending Hashtags Used in Posts
SELECT h.Hashtag_Text, COUNT(ph.Post_ID) AS Usage_Count
FROM Hashtag h
JOIN Post_Hashtags ph ON h.Hashtag_ID = ph.Hashtag_ID
GROUP BY h.Hashtag_Text
ORDER BY Usage_Count DESC;


-- Sentiments Analysis for Comments on Specific Post
SELECT c.Comment_Text, s.Sentiment_Score, s.Sentiment_Label
FROM Comments c
JOIN Sentiments s ON c.Comment_id = s.comment_id
WHERE c.Post_id = (SELECT post_id FROM Posts WHERE post_id = 1);


-- Notifications by Type
SELECT Notification_Type, COUNT(*) AS Count
FROM Notification
GROUP BY Notification_Type;


-- Retrieve Users with the Most Followers
SELECT u.Username, COUNT(f.Follower_id) AS Follower_Count
FROM Users u
JOIN Follow f ON u.User_id = f.Following_id
GROUP BY u.Username
ORDER BY Follower_Count DESC;


-- Identify Historical Trends in Sentiment Scores
SELECT s.Sentiment_Label, AVG(s.Sentiment_Score) AS Average_Sentiment, DATEPART(month, s.Created_at) AS Month
FROM Sentiments s
GROUP BY s.Sentiment_Label, DATEPART(month, s.Created_at)
ORDER BY Month;

-- Find the Most Engaging Posts by Reaction Count
SELECT TOP 10 
    p.post_id, 
    CAST(p.Content AS VARCHAR(MAX)) AS Content, 
    COUNT(r.Reaction_id) AS Reaction_Count
FROM Posts p
LEFT JOIN Post_Reaction r ON p.post_id = r.Post_id
GROUP BY p.post_id, CAST(p.Content AS VARCHAR(MAX))
ORDER BY Reaction_Count DESC;


-- Analyze Comments by Sentiment
SELECT c.User_id, c.Comment_Text, s.Sentiment_Label
FROM Comments c
JOIN Sentiments s ON c.Comment_id = s.comment_id
WHERE s.Sentiment_Score < 0;


-- List of Users with No Posts
SELECT u.Username
FROM Users u
LEFT JOIN Posts p ON u.User_id = p.user_id
WHERE p.post_id IS NULL;

-- Summary of All Posts and Their Engagement Metrics
SELECT p.post_id, 
       COUNT(DISTINCT c.Comment_id) AS Total_Comments,
       COUNT(DISTINCT r.Reaction_id) AS Total_Reactions,
       SUM(em.Like_Count) AS Total_Likes
FROM Posts p
LEFT JOIN Comments c ON p.post_id = c.Post_id
LEFT JOIN Post_Reaction r ON p.post_id = r.Post_id
LEFT JOIN Engagement_Metrics em ON p.post_id = em.Post_ID
GROUP BY p.post_id;

-- Trending Topics Over Time
SELECT t.Name, COUNT(tp.post_id) AS Post_Count
FROM Topic t
JOIN Topic_Posts tp ON t.Topic_ID = tp.Topic_ID
GROUP BY t.Name
ORDER BY Post_Count DESC;

-- Analyze User Activity by Location
SELECT ul.Location, COUNT(u.User_id) AS User_Count
FROM User_Location ul
JOIN Users u ON ul.User_ID = u.User_id
GROUP BY ul.Location;

-- Get a Breakdown of Posts by Visibility
SELECT Visibility, COUNT(*) AS Post_Count
FROM Posts
GROUP BY Visibility;


-- Retrieve Saved Posts by User
SELECT u.Username, COUNT(sp.Post_id) AS Total_Saved_Posts
FROM Users u
JOIN Saved_Post sp ON u.User_id = sp.user_id
GROUP BY u.Username;


-- Most Active Users Based on Comments
SELECT u.Username, COUNT(c.Comment_id) AS Total_Comments
FROM Users u
JOIN Comments c ON u.User_id = c.User_id
GROUP BY u.Username
ORDER BY Total_Comments DESC;


-- Posts with the Highest Average Sentiment Score
SELECT p.post_id, AVG(s.Sentiment_Score) AS Avg_Sentiment
FROM Posts p
JOIN Sentiments s ON p.post_id = s.Post_Id
GROUP BY p.post_id
ORDER BY Avg_Sentiment DESC;


-- Users Who Have Blocked Others
SELECT u.Username, COUNT(b.Blocked_id) AS Total_Blocks
FROM Users u
JOIN Block b ON u.User_id = b.Blocker_id
GROUP BY u.Username
ORDER BY Total_Blocks DESC;


-- Monthly Engagement Trends
SELECT 
    DATEPART(month, e.Recoreded_at) AS Month, 
    SUM(COALESCE(e.Like_Count, 0)) AS Total_Likes, 
    SUM(COALESCE(e.Comment_Count, 0)) AS Total_Comments,
    SUM(COALESCE(e.Share_Count, 0)) AS Total_Shares
FROM Engagement_Metrics e
GROUP BY DATEPART(month, e.Recoreded_at)
ORDER BY Month;

-- Retrieve Users with Specific Preferences
SELECT u.Username, up.Theme, up.Language
FROM Users u
JOIN User_Preferences up ON u.User_id = up.user_Id
WHERE up.Theme = 'Dark';


-- Find Average Reaction Count by Post Type
SELECT p.platform AS Post_Platform, 
       AVG(r.Reaction_id) AS Avg_Reactions
FROM Posts p
LEFT JOIN Post_Reaction r ON p.post_id = r.Post_id
GROUP BY p.platform;


-- Count of Posts Saved by Time Frame
SELECT DATEPART(year, sp.Saved_Date) AS Year, 
       COUNT(sp.Saved_id) AS Total_Saved_Posts
FROM Saved_Post sp
GROUP BY DATEPART(year, sp.Saved_Date)
ORDER BY Year;

-- Sentiment Distribution for a Specific Topic
SELECT s.Sentiment_Label, COUNT(s.Sentiment_id) AS Count
FROM Sentiments s
JOIN Comments c ON s.comment_id = c.Comment_id
JOIN Topic_Posts tp ON c.Post_id = tp.post_id
WHERE tp.Topic_ID = (SELECT Topic_ID FROM Topic WHERE Name = 'user1')
GROUP BY s.Sentiment_Label;

-- Users Who Have Joined Recently
SELECT Username, Date_Joined
FROM Users
WHERE Date_Joined >= DATEADD(month, -6, GETDATE()); -- Last 6 months

-- Engagement Metrics by User for Specific Time Period
SELECT 
    u.Username, 
    SUM(em.Like_Count) AS Total_Likes, 
    SUM(em.Comment_Count) AS Total_Comments
FROM Users u
JOIN Admin_Views av ON u.User_id = av.User_ID
JOIN Engagement_Metrics em ON av.Viewed_id = em.Viewed_id
WHERE em.Recoreded_at BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY u.Username;

-- User Engagement Metrics by Region
SELECT ul.Location, 
       COUNT(u.User_id) AS User_Count, 
       SUM(em.Like_Count) AS Total_Likes,
       SUM(em.Comment_Count) AS Total_Comments
FROM User_Location ul
JOIN Users u ON ul.User_ID = u.User_id
JOIN Engagement_Metrics em ON u.User_id = em.Viewed_id
GROUP BY ul.Location
ORDER BY User_Count DESC;

-- Campaign Performance
SELECT 
    C.Name AS Campaign_Name, 
    C.Objective, 
    COUNT(DISTINCT A.Ad_ID) AS Total_Ads, 
    C.Budget AS Total_Budget, 
    COUNT(AC.Clicks_ID) AS Total_Clicks 
FROM Campaign C 
JOIN Advertisement A ON C.Campaign_ID = A.Campaign_ID 
LEFT JOIN Ad_Clicks AC ON A.Ad_ID = AC.Ad_ID 
GROUP BY C.Name, C.Objective, C.Budget 
ORDER BY Total_Clicks DESC;


-- Total Unique Countries Reached';
SELECT 
    COUNT(DISTINCT Country) AS Number_Of_Countries 
FROM Users;


-- Total Time Span of Content (Days)
SELECT 
    DATEDIFF(DAY, MIN(Post_date), MAX(Post_date)) AS Days_Between_First_and_Last_Post 
FROM Posts;


-- Most Popular Tags Used On Posts
SELECT 
    T.Name, 
    COUNT(PT.post_id) AS Times_Used 
FROM Tags T 
JOIN Post_Tags PT ON T.Tag_ID = PT.Tag_id 
GROUP BY T.Name 
ORDER BY Times_Used DESC;

-- Users Who Only Use One Type of Device
SELECT 
    U.Username, 
    COUNT(DISTINCT S.Device) AS Device_Types_Used 
FROM Users U 
JOIN Session S ON U.User_id = S.user_Id 
GROUP BY U.Username 
HAVING COUNT(DISTINCT S.Device) = 1;


-- Busiest Hour Of The Day For Logins
SELECT 
    DATEPART(HOUR, log_in_time) AS Hour_Of_Day, 
    COUNT(*) AS Login_Count 
FROM Session 
GROUP BY DATEPART(HOUR, log_in_time) 
ORDER BY Login_Count DESC;


-- Users Who Have Never Clicked an AD
SELECT 
    U.Username 
FROM Users U 
JOIN Session S ON U.User_id = S.user_Id 
LEFT JOIN Ad_Clicks AC ON U.User_id = AC.user_id 
WHERE AC.Clicks_ID IS NULL 
GROUP BY U.Username;


-- Tags with the most negative posts
SELECT 
    T.Name AS Tag, 
    COUNT(S.Sentiment_id) AS Negative_Count
FROM Tags T 
JOIN Post_Tags PT ON T.Tag_ID = PT.Tag_id 
JOIN Sentiments S ON PT.post_id = S.Post_Id 
WHERE S.Sentiment_Label = 'Negative' 
GROUP BY T.Name;


-- Number of posts: Weekends VS Weekdays
SELECT 
    CASE 
        WHEN DATENAME(dw, Post_date) IN ('Saturday', 'Friday') THEN 'Weekend' 
        ELSE 'Weekday' 
    END AS Day_Type, 
    COUNT(*) AS Post_Vol 
FROM Posts 
GROUP BY 
    CASE 
        WHEN DATENAME(dw, Post_date) IN ('Saturday', 'Friday') THEN 'Weekend' 
        ELSE 'Weekday' 
    END;


-- Most Active Users bty Total Activity';
SELECT 
    U.Username, 
    (COUNT(DISTINCT P.post_id) + COUNT(DISTINCT C.Comment_id) + COUNT(DISTINCT S.Saved_id)) AS Total_Activity_Score
FROM Users U 
LEFT JOIN Posts P ON U.User_id = P.user_id 
LEFT JOIN Comments C ON U.User_id = C.User_id 
LEFT JOIN Saved_Post S ON U.User_id = S.user_id 
GROUP BY U.Username 
ORDER BY Total_Activity_Score DESC;


-- Unspent Money by Campaign';
SELECT 
    C.Name, 
    C.Budget AS Total_Budget, 
    SUM(A.Budget) AS Allocated_Ads, 
    (C.Budget - SUM(A.Budget)) AS Unspent_Cash
FROM Campaign C 
LEFT JOIN Advertisement A ON C.Campaign_ID = A.Campaign_ID 
GROUP BY C.Name, C.Budget;


-- Monthly New Users Signups
SELECT 
    FORMAT(Date_Joined, 'yyyy-MM') AS Join_Month, 
    COUNT(User_id) AS New_Users 
FROM Users 
GROUP BY FORMAT(Date_Joined, 'yyyy-MM') 
ORDER BY Join_Month DESC;


-- Language Diversity In Comments
SELECT 
    Language, 
    COUNT(Comment_id) AS Comment_Count 
FROM Comments 
GROUP BY Language 
ORDER BY Comment_Count DESC;


-- Top Commenters
SELECT TOP 10
    U.Username, 
    COUNT(C.Comment_id) AS Comments_Made 
FROM Users U 
JOIN Comments C ON U.User_id = C.User_id 
GROUP BY U.Username 
ORDER BY Comments_Made DESC;


-- Device Usage Breakdown (Session Analytics)
SELECT 
    Device, 
    COUNT(session_id) AS Session_Count, 
    COUNT(DISTINCT user_Id) AS Unique_Users 
FROM Session 
GROUP BY Device 
ORDER BY Session_Count DESC;


-- Job Status Per Type
SELECT 
    job_type, 
    status, 
    COUNT(job_id) AS Count, 
    target_type 
FROM Job_Queue 
GROUP BY job_type, status, target_type 
ORDER BY status;
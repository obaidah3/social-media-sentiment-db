CREATE DATABASE SENTIMENT;
GO
USE SENTIMENT;
GO

-- ===========================================
-- USERS
-- ===========================================

CREATE TABLE Users (
    User_id         BIGINT IDENTITY(1,1) PRIMARY KEY,
    Username        VARCHAR(100) NOT NULL UNIQUE,
    Email           VARCHAR(150) NOT NULL UNIQUE,
    Country         VARCHAR(100),
    Date_Joined     DATE NOT NULL,
    Language        VARCHAR(50),
    Bio             TEXT,
    Profile_pic_url TEXT,
    Birthdate       DATE,
    Platform        VARCHAR(50),
    Password        VARCHAR(255) NOT NULL
);
GO

-- ===========================================
-- POSTS
-- ===========================================

CREATE TABLE Posts (
    post_id      BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_id      BIGINT NOT NULL,
    plocation    VARCHAR(255),
    Visibility   VARCHAR(50),
    Post_date    DATE NOT NULL,
    Content      TEXT,
    platform     VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(User_id)
);
GO

-- ===========================================
-- TOPICS
-- ===========================================

CREATE TABLE Topic (
    Topic_ID         BIGINT IDENTITY(1,1) PRIMARY KEY,
    Name             VARCHAR(255) NOT NULL,
    Category         VARCHAR(100),
    Created_at       DATE NOT NULL,
    PopularityScore  INT
);
GO

CREATE TABLE Topic_Posts (
    Topic_ID   BIGINT NOT NULL,
    post_id    BIGINT NOT NULL,
    PRIMARY KEY (Topic_ID, post_id),
    FOREIGN KEY (Topic_ID) REFERENCES Topic(Topic_ID),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- SOCIAL RELATIONS
-- ===========================================

CREATE TABLE Follow (
    Follower_id  BIGINT NOT NULL,
    Following_id BIGINT NOT NULL,
    PRIMARY KEY (Follower_id, Following_id),
    FOREIGN KEY (Follower_id) REFERENCES Users(User_id),
    FOREIGN KEY (Following_id) REFERENCES Users(User_id)
);
GO

CREATE TABLE Block (
    Blocker_id BIGINT NOT NULL,
    Blocked_id BIGINT NOT NULL,
    PRIMARY KEY (Blocker_id, Blocked_id),
    FOREIGN KEY (Blocker_id) REFERENCES Users(User_id),
    FOREIGN KEY (Blocked_id) REFERENCES Users(User_id)
);
GO

-- ===========================================
-- TAGS
-- ===========================================

CREATE TABLE Tags (
    Tag_ID       BIGINT IDENTITY(1,1) PRIMARY KEY,
    Name         VARCHAR(255) NOT NULL,
    Created_at   DATE NOT NULL,
    Description  TEXT
);
GO

CREATE TABLE Post_Tags (
    Tag_id     BIGINT NOT NULL,
    post_id    BIGINT NOT NULL,
    Created_at DATE NOT NULL,
    PRIMARY KEY (Tag_id, post_id),
    FOREIGN KEY (Tag_id) REFERENCES Tags(Tag_ID),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- TRENDING POSTS
-- ===========================================

CREATE TABLE Trending_Posts (
    TrendingPost_ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    post_id         BIGINT NOT NULL,
    Score           INT,
    Date            DATE NOT NULL,
    Rank            INT,
    FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- USER LOCATION
-- ===========================================

CREATE TABLE User_Location (
    User_ID   BIGINT PRIMARY KEY,
    Location  VARCHAR(255),
    FOREIGN KEY (User_ID) REFERENCES Users(User_id)
);
GO

-- ===========================================
-- RECOMMENDATION + PREFERENCES
-- ===========================================

CREATE TABLE Recommendation (
    Recommendation_ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_Id           BIGINT NOT NULL,
    Score             INT,
    Date              DATE NOT NULL,
    Recommendation_Type VARCHAR(255),
    FOREIGN KEY (user_Id) REFERENCES Users(User_id)
);
GO

CREATE TABLE User_Preferences (
    preferences_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_Id        BIGINT NOT NULL,
    Theme          VARCHAR(255),
    Date           DATE NOT NULL,
    Language       VARCHAR(100),
    FOREIGN KEY (user_Id) REFERENCES Users(user_id)
);
GO

CREATE TABLE P_Notification (
    Preference_ID BIGINT PRIMARY KEY,
    Notification_Setting VARCHAR(255),
    FOREIGN KEY (Preference_ID) REFERENCES User_Preferences(preferences_id)
);
GO

-- ===========================================
-- SESSIONS & NOTIFICATIONS
-- ===========================================

CREATE TABLE Session (
    session_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_Id      BIGINT NOT NULL,
    Device       VARCHAR(255),
    ip_address   VARCHAR(255),
    log_in_time  DATETIME,
    log_out_time DATETIME,
    FOREIGN KEY (user_Id) REFERENCES Users(user_id)
);
GO

CREATE TABLE Notification (
    notification_id  BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_Id          BIGINT NOT NULL,
    Is_Read          BIT,
    Notification_date DATE NOT NULL,
    Notification_Type VARCHAR(255),
    Content          TEXT,
    FOREIGN KEY (user_Id) REFERENCES Users(user_id)
);
GO

-- ===========================================
-- PROFILE / BADGES
-- ===========================================

CREATE TABLE Profile (
    Profile_ID        BIGINT IDENTITY(1,1) PRIMARY KEY,
    User_ID           BIGINT NOT NULL,
    Platform          VARCHAR(255),
    Handle            VARCHAR(255),
    Followers_Count   INT,
    Platform_User_ID  VARCHAR(255),
    Created_at        DATE NOT NULL,
    Following_Count   INT,
    FOREIGN KEY (User_ID) REFERENCES Users(user_id)
);
GO

CREATE TABLE Badge (
    Badge_ID     BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_Id      BIGINT NOT NULL,
    Badge_Name   VARCHAR(255),
    Description  TEXT,
    FOREIGN KEY (user_Id) REFERENCES Users(user_id)
);
GO

-- ===========================================
-- PLACES
-- ===========================================

CREATE TABLE Places (
    Places_id  BIGINT IDENTITY(1,1) PRIMARY KEY,
    Name       VARCHAR(200),
    Country    VARCHAR(100),
    City       VARCHAR(100)
);
GO

CREATE TABLE User_Places (
    Places_id BIGINT NOT NULL,
    User_id   BIGINT NOT NULL,
    PRIMARY KEY (Places_id, User_id),
    FOREIGN KEY (Places_id) REFERENCES Places(Places_id),
    FOREIGN KEY (User_id) REFERENCES Users(user_id)
);
GO

CREATE TABLE Post_Places (
    Places_id BIGINT NOT NULL,
    Post_id   BIGINT NOT NULL,
    PRIMARY KEY (Places_id, Post_id),
    FOREIGN KEY (Places_id) REFERENCES Places(Places_id),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- INTERACTIONS
-- ===========================================

CREATE TABLE Interaction_Logs (
    log_id           BIGINT IDENTITY(1,1) PRIMARY KEY,
    Target_id        BIGINT NOT NULL,
    interaction_type VARCHAR(100) NOT NULL,
    interaction_date DATETIME NOT NULL
);
GO

CREATE TABLE User_Interaction (
    log_id  BIGINT PRIMARY KEY,
    User_id BIGINT NOT NULL,
    FOREIGN KEY (log_id) REFERENCES Interaction_Logs(log_id),
    FOREIGN KEY (User_id) REFERENCES Users(user_id)
);
GO

CREATE TABLE Post_Interaction (
    log_id  BIGINT PRIMARY KEY,
    Post_id BIGINT NOT NULL,
    FOREIGN KEY (log_id) REFERENCES Interaction_Logs(log_id),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- STORIES
-- ===========================================

CREATE TABLE Story (
    Story_id    BIGINT IDENTITY(1,1) PRIMARY KEY,
    Expired_at  DATETIME,
    MediaType   VARCHAR(50),
    Created_at  DATETIME NOT NULL,
    Media_Url   TEXT,
    user_id     BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
GO

CREATE TABLE Post_Story (
    Story_id BIGINT NOT NULL,
    Post_id  BIGINT NOT NULL,
    PRIMARY KEY (Story_id, Post_id),
    FOREIGN KEY (Story_id) REFERENCES Story(Story_id),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- SAVED POSTS / FEEDS
-- ===========================================

CREATE TABLE Saved_Post (
    Saved_id       BIGINT IDENTITY(1,1) PRIMARY KEY,
    Saved_Date     DATETIME NOT NULL,
    Saved_Location VARCHAR(255),
    user_id        BIGINT NOT NULL,
    Post_id        BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

CREATE TABLE User_Feed (
    Feed_ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    Score   INT,
    Date    DATETIME NOT NULL,
    user_id BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
GO

CREATE TABLE User_Feed_Post (
    Feed_id BIGINT NOT NULL,
    Post_id BIGINT NOT NULL,
    PRIMARY KEY (Feed_id, Post_id),
    FOREIGN KEY (Feed_id) REFERENCES User_Feed(Feed_ID),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- MESSAGING & MEDIA
-- ===========================================

CREATE TABLE Message (
    Message_id      BIGINT IDENTITY(1,1) PRIMARY KEY,
    Message_content TEXT,
    Status          VARCHAR(50),
    Message_date    DATETIME NOT NULL,
    user_id         BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
GO

CREATE TABLE Media (
    Media_id    BIGINT IDENTITY(1,1) PRIMARY KEY,
    Media_type  VARCHAR(50),
    Media_url   TEXT,
    Uploaded_at DATETIME NOT NULL
);
GO

CREATE TABLE Media_Message (
    Message_id BIGINT NOT NULL,
    Media_id   BIGINT NOT NULL,
    PRIMARY KEY (Message_id, Media_id),
    FOREIGN KEY (Message_id) REFERENCES Message(Message_id),
    FOREIGN KEY (Media_id) REFERENCES Media(Media_id)
);
GO

CREATE TABLE Media_Post (
    Media_id BIGINT NOT NULL,
    Post_id  BIGINT NOT NULL,
    PRIMARY KEY (Media_id, Post_id),
    FOREIGN KEY (Media_id) REFERENCES Media(Media_id),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- COMMENTS & REACTIONS
-- ===========================================

CREATE TABLE Comments (
    Comment_id      BIGINT IDENTITY(1,1) PRIMARY KEY,
    Comment_Text    TEXT,
    Language        VARCHAR(50),
    Comment_date    DATETIME NOT NULL,
    Sentiment_Score FLOAT,
    C_id            BIGINT,
    User_id         BIGINT NOT NULL,
    Post_id         BIGINT NOT NULL,
    FOREIGN KEY (C_id) REFERENCES Comments(Comment_id),
    FOREIGN KEY (User_id) REFERENCES Users(user_id),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

CREATE TABLE Reaction (
    Reaction_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
    Reaction_date DATETIME NOT NULL,
    Reaction_Type VARCHAR(100),
    comment_id    BIGINT,
    User_id       BIGINT NOT NULL,
    FOREIGN KEY (comment_id) REFERENCES Comments(Comment_id),
    FOREIGN KEY (User_id) REFERENCES Users(user_id)
);
GO

CREATE TABLE Post_Reaction (
    Reaction_id BIGINT NOT NULL,
    Post_id     BIGINT NOT NULL,
    PRIMARY KEY (Reaction_id, Post_id),
    FOREIGN KEY (Reaction_id) REFERENCES Reaction(Reaction_id),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- SENTIMENTS
-- ===========================================

CREATE TABLE Sentiments (
    Sentiment_id    BIGINT IDENTITY(1,1) PRIMARY KEY,
    Created_at      DATETIME NOT NULL,
    Sentiment_Score FLOAT,
    Sentiment_Label VARCHAR(100),
    Target_Type     VARCHAR(50),
    comment_id      BIGINT,
    Post_Id         BIGINT,
    FOREIGN KEY (comment_id) REFERENCES Comments(Comment_id),
    FOREIGN KEY (Post_Id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- EVENTS & CALENDAR
-- ===========================================

CREATE TABLE Event (
    Event_id    BIGINT IDENTITY(1,1) PRIMARY KEY,
    Target_id   BIGINT,
    Date        DATETIME NOT NULL,
    Event_Type  VARCHAR(100),
    user_id     BIGINT NOT NULL,
    Post_id     BIGINT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

CREATE TABLE Calendar (
    Calendar_ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    Event_id    BIGINT NOT NULL,
    Calendar_Type VARCHAR(100),
    Start_time   TIME,
    End_time     TIME,
    Start_date   DATE,
    End_date     DATE,
    Status       VARCHAR(50),
    FOREIGN KEY (Event_id) REFERENCES Event(Event_id)
);
GO

-- ===========================================
-- MODERATION
-- ===========================================

CREATE TABLE Moderation_Action (
    Action_ID      BIGINT IDENTITY(1,1) PRIMARY KEY,
    Action_Type    VARCHAR(100),
    Action_Date    DATETIME NOT NULL,
    Action_Details TEXT,
    Moderator_Id   BIGINT NOT NULL,
    user_id        BIGINT NOT NULL,
    FOREIGN KEY (Moderator_Id) REFERENCES Users(user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
GO

CREATE TABLE Flags (
    Flag_ID      BIGINT IDENTITY(1,1) PRIMARY KEY,
    Status       VARCHAR(50),
    Created_at   DATETIME NOT NULL,
    Reason       TEXT,
    Target_Type  VARCHAR(50),
    Moderator_Id BIGINT,
    user_id      BIGINT,
    comment_id   BIGINT,
    Post_id      BIGINT,
    FOREIGN KEY (Moderator_Id) REFERENCES Users(user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (comment_id) REFERENCES Comments(Comment_id),
    FOREIGN KEY (Post_id) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- HASHTAGS
-- ===========================================

CREATE TABLE Hashtag (
    Hashtag_ID   BIGINT IDENTITY(1,1) PRIMARY KEY,
    Hashtag_Text VARCHAR(255) NOT NULL,
    Usage_Count  INT DEFAULT 0,
    Created_at   DATETIME,
    Last_Used_at DATETIME
);
GO

CREATE TABLE Trending_Hashtags (
    Trending_ID    BIGINT IDENTITY(1,1) PRIMARY KEY,
    Date           DATE NOT NULL,
    Rank           INT NOT NULL,
    Mention_Counts INT,
    Hashtag_ID     BIGINT NOT NULL,
    FOREIGN KEY (Hashtag_ID) REFERENCES Hashtag(Hashtag_ID)
);
GO

CREATE TABLE Post_Hashtags (
    Hashtag_ID BIGINT NOT NULL,
    Post_ID    BIGINT NOT NULL,
    PRIMARY KEY (Hashtag_ID, Post_ID),
    FOREIGN KEY (Hashtag_ID) REFERENCES Hashtag(Hashtag_ID),
    FOREIGN KEY (Post_ID) REFERENCES Posts(post_id)
);
GO

-- ===========================================
-- ADMIN VIEWS
-- ===========================================

CREATE TABLE Admin_Views (
    Viewed_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
    Description TEXT,
    Name        VARCHAR(255),
    Created_at  DATETIME NOT NULL,
    User_ID     BIGINT NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(user_id)
);
GO

CREATE TABLE Admin_Hashtags (
    Hashtag_ID BIGINT NOT NULL,
    Viewed_id  BIGINT NOT NULL,
    PRIMARY KEY (Hashtag_ID, Viewed_id),
    FOREIGN KEY (Hashtag_ID) REFERENCES Hashtag(Hashtag_ID),
    FOREIGN KEY (Viewed_id) REFERENCES Admin_Views(Viewed_id)
);
GO

CREATE TABLE Post_Admin_Views (
    Viewed_id BIGINT NOT NULL,
    Post_ID   BIGINT NOT NULL,
    PRIMARY KEY (Viewed_id, Post_ID),
    FOREIGN KEY (Viewed_id) REFERENCES Admin_Views(Viewed_id),
    FOREIGN KEY (Post_ID) REFERENCES Posts(post_id)
);
GO

CREATE TABLE User_Admin_Views (
    Viewed_id BIGINT NOT NULL,
    User_ID   BIGINT NOT NULL,
    PRIMARY KEY (Viewed_id, User_ID),
    FOREIGN KEY (Viewed_id) REFERENCES Admin_Views(Viewed_id),
    FOREIGN KEY (User_ID) REFERENCES Users(user_id)
);
GO

-- ===========================================
-- ENGAGEMENT METRICS
-- ===========================================

CREATE TABLE Engagement_Metrics (
    Metric_ID       BIGINT IDENTITY(1,1) PRIMARY KEY,
    Viewed_id       BIGINT NOT NULL,
    Engagement_Rate FLOAT,
    Recoreded_at    DATETIME,
    Like_Count      INT DEFAULT 0,
    Share_Count     INT DEFAULT 0,
    Comment_Count   INT DEFAULT 0,
    Save_Count      INT DEFAULT 0,
    Post_ID         BIGINT,
    FOREIGN KEY (Viewed_id) REFERENCES Admin_Views(Viewed_id),
    FOREIGN KEY (Post_ID) REFERENCES Posts(post_id)
);
GO

CREATE TABLE Experiments_Engagement_Metrics (
    Experiment_ID BIGINT IDENTITY(1,1) PRIMARY KEY,
    Metric_id     BIGINT NOT NULL,
    FOREIGN KEY (Metric_id) REFERENCES Engagement_Metrics(Metric_ID)
);
GO

-- ===========================================
-- EXPERIMENTS
-- ===========================================

CREATE TABLE Experiments (
    Experiment_ID INT PRIMARY KEY,
    Name          VARCHAR(255),
    Start_Date    DATE,
    End_Date      DATE,
    Objective     VARCHAR(255),
    Variant       VARCHAR(100)
);
GO

CREATE TABLE Post_Experiments (
    Experiment_ID INT,
    Post_id BIGINT,
    PRIMARY KEY (Experiment_ID, Post_id),
    FOREIGN KEY (Experiment_ID) REFERENCES Experiments(Experiment_ID),
    FOREIGN KEY (Post_id) REFERENCES Posts(Post_id)
);
GO

CREATE TABLE Campaign (
    Campaign_ID INT PRIMARY KEY,
    Budget      FLOAT,
    Name        VARCHAR(255),
    Objective   VARCHAR(255),
    Start_Date  DATE,
    End_Date    DATE
);
GO

CREATE TABLE Experiments_Campaign (
    Experiment_ID INT,
    Campaign_ID   INT,
    PRIMARY KEY (Experiment_ID, Campaign_ID),
    FOREIGN KEY (Experiment_ID) REFERENCES Experiments(Experiment_ID),
    FOREIGN KEY (Campaign_ID) REFERENCES Campaign(Campaign_ID)
);
GO

CREATE TABLE Post_Campaign (
    Campaign_ID INT,
    Post_id BIGINT,
    PRIMARY KEY (Campaign_ID, Post_id),
    FOREIGN KEY (Campaign_ID) REFERENCES Campaign(Campaign_ID),
    FOREIGN KEY (Post_id) REFERENCES Posts(Post_id)
);
GO

CREATE TABLE Admin_Campaign (
    Campaign_ID INT,
    Viewed_id   BIGINT,
    PRIMARY KEY (Campaign_ID, Viewed_id),
    FOREIGN KEY (Campaign_ID) REFERENCES Campaign(Campaign_ID),
    FOREIGN KEY (Viewed_id) REFERENCES Admin_Views(Viewed_id)
);
GO

-- ===========================================
-- ADVERTISEMENT
-- ===========================================

CREATE TABLE Advertisement (
    Ad_ID       INT PRIMARY KEY,
    Budget      FLOAT,
    Start_Date  DATE,
    End_Date    DATE,
    Content     TEXT,
    Campaign_ID INT,
    FOREIGN KEY (Campaign_ID) REFERENCES Campaign(Campaign_ID)
);
GO

CREATE TABLE User_Feed_Advertisement (
    Feed_id BIGINT PRIMARY KEY,
    Ad_ID   INT,
    FOREIGN KEY (Ad_ID) REFERENCES Advertisement(Ad_ID)
);
GO

CREATE TABLE Ad_Clicks (
    Clicks_ID  INT PRIMARY KEY,
    Created_at DATETIME,
    Ad_ID      INT,
    user_id    BIGINT,
    FOREIGN KEY (Ad_ID) REFERENCES Advertisement(Ad_ID),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
GO

CREATE TABLE Job_Queue (
    job_id        BIGINT IDENTITY(1,1) PRIMARY KEY,
    job_type      VARCHAR(100) NOT NULL,
    target_type   VARCHAR(100),
    status        VARCHAR(50) NOT NULL,
    created_at    DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    media_id      BIGINT NULL,
    comment_id    BIGINT NULL,
    post_id       BIGINT NULL, 

    FOREIGN KEY (media_id) REFERENCES Media(media_id),
    FOREIGN KEY (comment_id) REFERENCES Comments(comment_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id),
);
GO
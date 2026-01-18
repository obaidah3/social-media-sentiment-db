# app/v1/analytics.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict
from datetime import date, datetime, timedelta

from app.database import get_db
from app.models import User, Post, Comment, Reaction, Sentiment
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/dashboard")
def get_user_analytics_dashboard(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Get personalized analytics dashboard for current user

    Includes:
    - Total posts, comments, likes
    - Engagement metrics
    - Sentiment analysis trends
    - Top performing posts
    """

    # Total posts
    total_posts = db.query(Post).filter(Post.user_id == current_user.User_id).count()

    # Total comments
    total_comments = db.query(Comment).filter(Comment.User_id == current_user.User_id).count()

    # Total likes received
    total_likes = db.query(Reaction).join(
        Reaction.posts
    ).filter(Post.user_id == current_user.User_id).count()

    # Average engagement per post
    avg_engagement = 0
    if total_posts > 0:
        avg_engagement = total_likes / total_posts

    # Sentiment distribution
    sentiments = db.query(
        Sentiment.Sentiment_Label,
        func.count(Sentiment.Sentiment_id).label('count')
    ).join(
        Post, Post.post_id == Sentiment.Post_Id
    ).filter(
        Post.user_id == current_user.User_id
    ).group_by(Sentiment.Sentiment_Label).all()

    sentiment_distribution = {s.Sentiment_Label: s.count for s in sentiments}

    # Top performing posts
    user_posts = db.query(Post).filter(Post.user_id == current_user.User_id).all()
    posts_with_engagement = []

    for post in user_posts:
        likes = db.query(Reaction).join(Reaction.posts).filter(
            Post.post_id == post.post_id
        ).count()
        comments = db.query(Comment).filter(Comment.Post_id == post.post_id).count()
        engagement = likes + (comments * 2)

        posts_with_engagement.append({
            "post_id": post.post_id,
            "content": post.Content[:100] + "..." if len(post.Content) > 100 else post.Content,
            "likes": likes,
            "comments": comments,
            "engagement_score": engagement,
            "date": post.Post_date.isoformat()
        })

    # Sort by engagement
    posts_with_engagement.sort(key=lambda x: x['engagement_score'], reverse=True)
    top_posts = posts_with_engagement[:5]

    return {
        "overview": {
            "total_posts": total_posts,
            "total_comments": total_comments,
            "total_likes_received": total_likes,
            "average_engagement": round(avg_engagement, 2),
            "followers": current_user.followers_count,
            "following": current_user.following_count
        },
        "sentiment_analysis": {
            "distribution": sentiment_distribution,
            "positive_percentage": round(
                (sentiment_distribution.get('positive', 0) / max(total_posts, 1)) * 100, 1
            ),
            "negative_percentage": round(
                (sentiment_distribution.get('negative', 0) / max(total_posts, 1)) * 100, 1
            ),
            "neutral_percentage": round(
                (sentiment_distribution.get('neutral', 0) / max(total_posts, 1)) * 100, 1
            )
        },
        "top_posts": top_posts,
        "engagement_trend": "increasing"  # Placeholder - would calculate trend
    }


@router.get("/posts/performance")
def get_posts_performance(
        days: int = Query(30, ge=1, le=365),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Get posts performance over time

    - **days**: Number of days to analyze (default 30)

    Returns daily post counts and engagement metrics
    """

    start_date = date.today() - timedelta(days=days)

    # Get posts by date
    posts_by_date = db.query(
        Post.Post_date,
        func.count(Post.post_id).label('count')
    ).filter(
        Post.user_id == current_user.User_id,
        Post.Post_date >= start_date
    ).group_by(Post.Post_date).all()

    # Convert to dict
    posts_dict = {p.Post_date: p.count for p in posts_by_date}

    # Build daily data
    daily_data = []
    for i in range(days):
        check_date = start_date + timedelta(days=i)
        post_count = posts_dict.get(check_date, 0)

        daily_data.append({
            "date": check_date.isoformat(),
            "posts": post_count
        })

    return {
        "period_days": days,
        "total_posts": sum(d['posts'] for d in daily_data),
        "average_per_day": round(sum(d['posts'] for d in daily_data) / days, 2),
        "daily_data": daily_data
    }


@router.get("/sentiment/trends")
def get_sentiment_trends(
        days: int = Query(30, ge=1, le=365),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Get sentiment trends over time

    Shows how your content sentiment has changed
    """

    start_date = date.today() - timedelta(days=days)

    # Get posts with sentiments
    posts_with_sentiment = db.query(
        Post.Post_date,
        Sentiment.Sentiment_Label
    ).join(
        Sentiment, Sentiment.Post_Id == Post.post_id
    ).filter(
        Post.user_id == current_user.User_id,
        Post.Post_date >= start_date
    ).all()

    # Organize by date
    sentiment_by_date = {}
    for post_date, sentiment_label in posts_with_sentiment:
        if post_date not in sentiment_by_date:
            sentiment_by_date[post_date] = {'positive': 0, 'negative': 0, 'neutral': 0}
        sentiment_by_date[post_date][sentiment_label] += 1

    # Build daily data
    daily_sentiment = []
    for i in range(days):
        check_date = start_date + timedelta(days=i)
        sentiments = sentiment_by_date.get(check_date, {'positive': 0, 'negative': 0, 'neutral': 0})

        daily_sentiment.append({
            "date": check_date.isoformat(),
            "positive": sentiments['positive'],
            "negative": sentiments['negative'],
            "neutral": sentiments['neutral']
        })

    return {
        "period_days": days,
        "daily_sentiment": daily_sentiment
    }


@router.get("/engagement/breakdown")
def get_engagement_breakdown(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed engagement breakdown

    Shows which reaction types are most common
    """

    # Get reaction breakdown
    reactions = db.query(
        Reaction.Reaction_Type,
        func.count(Reaction.Reaction_id).label('count')
    ).join(
        Reaction.posts
    ).filter(
        Post.user_id == current_user.User_id
    ).group_by(Reaction.Reaction_Type).all()

    reaction_breakdown = {r.Reaction_Type: r.count for r in reactions}

    # Get comments breakdown
    total_comments = db.query(Comment).filter(Comment.User_id == current_user.User_id).count()

    comments_received = db.query(Comment).join(
        Post, Post.post_id == Comment.Post_id
    ).filter(
        Post.user_id == current_user.User_id
    ).count()

    return {
        "reactions": {
            "total": sum(reaction_breakdown.values()),
            "breakdown": reaction_breakdown
        },
        "comments": {
            "made": total_comments,
            "received": comments_received
        },
        "engagement_score": sum(reaction_breakdown.values()) + (comments_received * 2)
    }


@router.get("/audience/insights")
def get_audience_insights(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Get insights about your audience

    Shows who engages with your content most
    """

    # Get top engagers (users who like/comment most)
    user_posts = db.query(Post.post_id).filter(Post.user_id == current_user.User_id).all()
    post_ids = [p.post_id for p in user_posts]

    if not post_ids:
        return {
            "followers_growth": 0,
            "engagement_rate": 0,
            "top_engagers": [],
            "geographic_distribution": {}
        }

    # Get users who reacted to posts
    top_engagers = db.query(
        User.User_id,
        User.Username,
        func.count(Reaction.Reaction_id).label('engagement_count')
    ).join(
        Reaction, Reaction.User_id == User.User_id
    ).join(
        Reaction.posts
    ).filter(
        Post.post_id.in_(post_ids)
    ).group_by(
        User.User_id, User.Username
    ).order_by(desc('engagement_count')).limit(10).all()

    top_engagers_list = [
        {
            "user_id": e.User_id,
            "username": e.Username,
            "engagement_count": e.engagement_count
        }
        for e in top_engagers
    ]

    # Geographic distribution of followers
    follower_countries = db.query(
        User.Country,
        func.count(User.User_id).label('count')
    ).filter(
        User.User_id.in_([f.User_id for f in current_user.followers])
    ).group_by(User.Country).all()

    geo_distribution = {c.Country or 'Unknown': c.count for c in follower_countries}

    return {
        "total_followers": current_user.followers_count,
        "engagement_rate": round((len(top_engagers) / max(current_user.followers_count, 1)) * 100, 2),
        "top_engagers": top_engagers_list,
        "geographic_distribution": geo_distribution
    }


@router.get("/content/recommendations")
def get_content_recommendations(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """
    Get AI-powered content recommendations

    Suggests what type of content to post based on past performance
    """

    # Analyze past performance
    posts_with_sentiment = db.query(
        Sentiment.Sentiment_Label,
        func.avg(func.cast(Sentiment.Sentiment_Score, Float)).label('avg_score')
    ).join(
        Post, Post.post_id == Sentiment.Post_Id
    ).filter(
        Post.user_id == current_user.User_id
    ).group_by(Sentiment.Sentiment_Label).all()

    sentiment_performance = {s.Sentiment_Label: float(s.avg_score or 0) for s in posts_with_sentiment}

    # Generate recommendations
    recommendations = []

    if sentiment_performance.get('positive', 0) > 0.7:
        recommendations.append({
            "type": "content_style",
            "recommendation": "Your positive posts perform well! Continue sharing uplifting content.",
            "confidence": "high"
        })

    if current_user.followers_count < 100:
        recommendations.append({
            "type": "growth",
            "recommendation": "Engage more with others by commenting and reacting to build your network.",
            "confidence": "high"
        })

    # Post frequency
    recent_posts = db.query(Post).filter(
        Post.user_id == current_user.User_id,
        Post.Post_date >= date.today() - timedelta(days=7)
    ).count()

    if recent_posts < 3:
        recommendations.append({
            "type": "frequency",
            "recommendation": "Try posting more regularly. Aim for 3-5 posts per week for better engagement.",
            "confidence": "medium"
        })

    return {
        "recommendations": recommendations,
        "sentiment_performance": sentiment_performance
    }
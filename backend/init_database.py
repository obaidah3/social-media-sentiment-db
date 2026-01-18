# init_database.py

"""
Database Initialization Script

This script creates all database tables and optionally seeds with sample data.
Run this before starting the application for the first time.
"""

from app.database import engine, Base, SessionLocal
from app.models import *  # Import all models
from app.utils.security import get_password_hash
from datetime import date, datetime, timedelta
import random


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


def seed_sample_data():
    """Seed database with sample data for testing"""
    print("\nSeeding sample data...")
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            print("⚠️  Database already has data. Skipping seed.")
            return

        # Create admin user
        admin = User(
            Username="admin",
            Email="admin@socialhub.local",
            Password=get_password_hash("Admin123!"),
            Country="Egypt",
            Date_Joined=date.today(),
            Language="en",
            Bio="System Administrator",
            Profile_pic_url="AD",
            Birthdate=date(1990, 1, 1),
            Platform="web",
            role="admin",
            status="active"
        )
        db.add(admin)

        # Create sample users
        sample_users = [
            {
                "username": "johndoe",
                "email": "john@example.com",
                "name": "John Doe",
                "bio": "Full-stack developer 🚀",
                "country": "United States"
            },
            {
                "username": "sarahjohnson",
                "email": "sarah@example.com",
                "name": "Sarah Johnson",
                "bio": "React Developer | Designer",
                "country": "Canada"
            },
            {
                "username": "mikechen",
                "email": "mike@example.com",
                "name": "Mike Chen",
                "bio": "Database Expert | Backend Developer",
                "country": "Singapore"
            },
            {
                "username": "alexrivera",
                "email": "alex@example.com",
                "name": "Alex Rivera",
                "bio": "DevOps Engineer | Cloud Architect",
                "country": "Spain"
            },
            {
                "username": "emilywang",
                "email": "emily@example.com",
                "name": "Emily Wang",
                "bio": "Product Manager | Tech Enthusiast",
                "country": "China"
            }
        ]

        created_users = [admin]

        for user_data in sample_users:
            user = User(
                Username=user_data["username"],
                Email=user_data["email"],
                Password=get_password_hash("Test123!"),
                Country=user_data["country"],
                Date_Joined=date.today() - timedelta(days=random.randint(30, 365)),
                Language="en",
                Bio=user_data["bio"],
                Profile_pic_url=(user_data["name"][0] + user_data["name"].split()[1][0]).upper(),
                Platform="web",
                role="user",
                status="active"
            )
            db.add(user)
            created_users.append(user)

        db.commit()
        print(f"✅ Created {len(created_users)} users")

        # Create follow relationships
        for i, user in enumerate(created_users[1:], 1):
            # Each user follows a few random users
            num_to_follow = random.randint(1, min(3, len(created_users) - 1))
            possible_follows = [u for u in created_users if u != user]
            follows = random.sample(possible_follows, num_to_follow)
            user.following.extend(follows)

        db.commit()
        print("✅ Created follow relationships")

        # Create sample posts
        sample_posts = [
            "Just launched my new project! 🚀 Really excited about this. #coding #webdev",
            "Beautiful sunset today 🌅 Nature is amazing! #photography #nature",
            "Learning React has been an incredible journey. The component model is so intuitive! #react #javascript",
            "Coffee and code - the perfect combination ☕💻 #developer #coding",
            "Excited to announce our new feature release! Thanks to the amazing team 🎉 #teamwork #product",
            "Database optimization can make such a huge difference in performance! #database #performance",
            "Just finished a great book on system design. Highly recommended! 📚 #tech #reading",
            "Working on improving my algorithm skills. LeetCode here I come! 💪 #algorithms #practice",
            "The new TypeScript features are game-changing! Type safety FTW 🎯 #typescript #webdev",
            "Remember to take breaks! Your mental health matters 🧘‍♀️ #wellness #mentalhealth"
        ]

        for i, user in enumerate(created_users[1:], 1):
            # Each user creates 2-3 posts
            num_posts = random.randint(2, 3)
            for j in range(num_posts):
                post_content = random.choice(sample_posts)
                post = Post(
                    user_id=user.User_id,
                    Content=post_content,
                    Visibility="public",
                    Post_date=date.today() - timedelta(days=random.randint(0, 30)),
                    platform="web"
                )
                db.add(post)
                db.flush()

                # Add sentiment
                from app.utils.sentiment import analyze_sentiment
                sentiment_result = analyze_sentiment(post_content)

                sentiment = Sentiment(
                    Post_Id=post.post_id,
                    Sentiment_Label=sentiment_result['label'],
                    Sentiment_Score=str(sentiment_result['score']),
                    Target_Type='post'
                )
                db.add(sentiment)

        db.commit()
        print("✅ Created sample posts with sentiment analysis")

        # Create sample comments
        posts = db.query(Post).all()
        sample_comments = [
            "Great post! Thanks for sharing 👍",
            "This is so helpful, thank you!",
            "I completely agree with this",
            "Interesting perspective!",
            "Love this! Keep it up 🔥",
            "Well said!",
            "Can you share more about this?",
            "Amazing work!",
            "This made my day 😊",
            "Totally resonates with me"
        ]

        for post in posts[:10]:  # Comment on first 10 posts
            num_comments = random.randint(1, 3)
            for _ in range(num_comments):
                commenter = random.choice(created_users[1:])
                comment_text = random.choice(sample_comments)

                comment = Comment(
                    Comment_Text=comment_text,
                    User_id=commenter.User_id,
                    Post_id=post.post_id,
                    Comment_date=date.today() - timedelta(days=random.randint(0, 15)),
                    Language="en"
                )
                db.add(comment)
                db.flush()

                # Add sentiment to comment
                from app.utils.sentiment import analyze_sentiment
                sentiment_result = analyze_sentiment(comment_text)

                comment_sentiment = Sentiment(
                    comment_id=comment.Comment_id,
                    Sentiment_Label=sentiment_result['label'],
                    Sentiment_Score=str(sentiment_result['score']),
                    Target_Type='comment'
                )
                db.add(comment_sentiment)

        db.commit()
        print("✅ Created sample comments")

        # Create sample reactions
        for post in posts[:15]:  # Add reactions to first 15 posts
            num_reactions = random.randint(1, 5)
            for _ in range(num_reactions):
                reactor = random.choice(created_users[1:])
                reaction_type = random.choice(['like', 'love', 'haha', 'wow'])

                reaction = Reaction(
                    User_id=reactor.User_id,
                    Reaction_Type=reaction_type
                )
                reaction.posts.append(post)
                db.add(reaction)

        db.commit()
        print("✅ Created sample reactions")

        print("\n🎉 Sample data seeded successfully!")
        print("\n📝 Test Accounts:")
        print("   Admin: admin@socialhub.local / Admin123!")
        print("   User: john@example.com / Test123!")
        print("   (All test users have password: Test123!)")

    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Main initialization function"""
    print("=" * 60)
    print("SocialHub Database Initialization")
    print("=" * 60)

    # Create tables
    if not create_tables():
        return

    # Ask if user wants to seed data
    response = input("\nWould you like to seed sample data? (y/n): ")
    if response.lower() == 'y':
        seed_sample_data()

    print("\n" + "=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print("\nYou can now start the server with: python run.py")
    print("Visit: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
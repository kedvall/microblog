from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from config import AppConfig


class TestConfig(AppConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(username='susan')
        user.set_password('cat')
        self.assertFalse(user.check_password('dog'))
        self.assertTrue(user.check_password('cat'))

    def test_avatar(self):
        user = User(username='john', email='john@example.com')
        self.assertEqual(user.avatar(128), ('https://www.gravatar.com/avatar/'
                                            'd4c74594d841139328695756648b6bd6'
                                            '?d=identicon&s=128'))

    def test_follow(self):
        user1 = User(username='john', email='john@example.com')
        user2 = User(username='susan', email='susan@example.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(user1.followed.all(), [])
        self.assertEqual(user1.followers.all(), [])

        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 1)
        self.assertEqual(user1.followed.first().username, 'susan')
        self.assertEqual(user2.followers.count(), 1)
        self.assertEqual(user2.followers.first().username, 'john')

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.followed.count(), 0)
        self.assertEqual(user2.followers.count(), 0)

    def test_follow_posts(self):
        # Create four users
        user1 = User(username='john', email='john@example.com')
        user2 = User(username='susan', email='susan@example.com')
        user3 = User(username='mary', email='mary@example.com')
        user4 = User(username='david', email='david@example.com')
        db.session.add_all([user1, user2, user3, user4])

        # Create four posts
        now = datetime.utcnow()
        post1 = Post(body="post from john", author=user1, timestamp=now + timedelta(seconds=1))
        post2 = Post(body="post from susan", author=user2, timestamp=now + timedelta(seconds=4))
        post3 = Post(body="post from mary", author=user3, timestamp=now + timedelta(seconds=3))
        post4 = Post(body="post from david", author=user4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()

        # Set up the followers
        user1.follow(user2)  # John follows susan
        user1.follow(user4)  # John follows david
        user2.follow(user3)  # Susan follows mary
        user3.follow(user4)  # Mary follows david
        db.session.commit()

        # Check the followed posts of each user
        followed1 = user1.followed_posts().all()
        followed2 = user2.followed_posts().all()
        followed3 = user3.followed_posts().all()
        followed4 = user4.followed_posts().all()
        self.assertEqual(followed1, [post2, post4, post1])
        self.assertEqual(followed2, [post2, post3])
        self.assertEqual(followed3, [post3, post4])
        self.assertEqual(followed4, [post4])


if __name__ == "__main__":
    unittest.main(verbosity=2)

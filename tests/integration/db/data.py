from bot.database.models import User


TEST_USER = User(id=1, username="1")

LIST_TEST_USERS = [User(id=i, username=f"user_{i}", is_admin=False) for i in range(100)]

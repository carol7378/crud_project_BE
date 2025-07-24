from sqlalchemy.orm import Session
from database import engine
from models import User, Post
import datetime

with Session(engine) as session:

    session.add_all([
        User(status=True, username="A", name="ABC", password="miintto1"),
        User(status=True, username="B", name="BCD", password="miintto2"),
        User(status=True, username="C", name="CDE", password="miintto3"),
    ])
    session.commit()

    session.add_all([
        Post(title="Hello", content="Hello World", username="B",
             create_at=datetime.datetime.now()),
        Post(title="Apple", content="Hello Apple", username="A",
             create_at=datetime.datetime.now()),
        Post(title="Peach", content="Hello Peach", username="C",
             create_at=datetime.datetime.now()),
    ])
    session.commit()

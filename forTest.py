from sqlalchemy.orm import Session
from database import engine
from models.user import User
#from models.post import Post

with Session(engine) as session:

    session.add_all([
        User(username="A", name="ABC", password="miintto1"),
        User(username="B", name="BCD", password="miintto2"),
        User(susername="C", name="CDE", password="miintto3"),
    ])
    session.commit()

    session.add_all([
        Post(title="Hello", content="Hello World", username="B"),
        Post(title="Apple", content="Hello Apple", username="A"),
        Post(title="Peach", content="Hello Peach", username="C"),
    ])
    session.commit()

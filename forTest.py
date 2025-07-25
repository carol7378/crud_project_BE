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


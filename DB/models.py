import sqlalchemy as sq

from sqlalchemy.orm import declarative_base

Base = declarative_base()


# пользователи VK
class Users(Base):
    __tablename__ = 'users'

    user_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String(length=30))
    last_name = sq.Column(sq.String(length=30))
    age = sq.Column(sq.Integer)
    gender = sq.Column(sq.String(length=10))
    city = sq.Column(sq.String(length=30))
    user_link = sq.Column(sq.String(length=150))


# фотографии
class Photos(Base):
    __tablename__ = 'photos'

    photo_id = sq.Column(sq.Integer, primary_key=True)
    photo_link = sq.Column(sq.String(length=150))
    likes = sq.Column(sq.Integer)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id', ondelete='CASCADE'))


# список избранных
class Favorites(Base):
    __tablename__ = 'favorites'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False)
    favorite_user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False)


# черный список
class Black_list(Base):
    __tablename__ = 'black_list'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False)
    black_list_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False)


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

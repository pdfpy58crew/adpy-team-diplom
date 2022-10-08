import os
from pprint import pprint

from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv, find_dotenv
from DB.models import *

# from vk_acs_2.py import get_my_information, get_photos, search_friends


def create_connection():
    load_dotenv(find_dotenv())
    USER = os.getenv('user')
    PASSWORD = os.getenv('password')
    BDNAME = os.getenv('bdname')
    DSN = f'postgresql://{USER}:{PASSWORD}@localhost:5432/{BDNAME}'
    engine = sq.create_engine(DSN)
    return engine


sessions = sessionmaker(bind=create_connection())
Session = scoped_session(sessions)


# декоратор для sessionmaker
def dbconnect(func):
    def _dbconnect(*args, **kwargs):
        session = Session()
        try:
            func(*args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            Session.remove()

    return _dbconnect


@dbconnect
def add_new_user(user_info):
    '''Добавляем нового пользователя в таблицу Users'''
    session = Session()
    if not check_users(user_info['user_id']):
        new_user = Users(**user_info)
        session.add(new_user)


def check_users(checking_id):
    '''Проверка наличия пользователя в Users'''
    session = Session()
    checking_user = session.query(Users).filter_by(user_id=checking_id).first()
    return checking_user is not None


@dbconnect
def add_photos(user_photo_info):
    '''Добавляем фотографии пользователя в таблицу Photos'''
    session = Session()
    user_photos = Photos(**user_photo_info)
    session.add(user_photos)


@dbconnect
def add_to_favorites(user_info, matched_user_info):
    '''Добавляем пользователя в Избранное, если пользователь отсутсвует'''
    session = Session()
    if not check_users(matched_user_info['user_id']):
        add_new_user(matched_user_info)
    if not check_favorites(matched_user_info['user_id']):
        new_favorite_user = Favorites(user_id=user_info['user_id'], favorite_user_id=matched_user_info['user_id'])
        session.add(new_favorite_user)


def check_favorites(checking_id):
    '''Проверка наличия пользователя в Избранном'''
    session = Session()
    checking_user = session.query(Favorites).filter_by(favorite_user_id=checking_id).first()
    return checking_user is not None


@dbconnect
def delete_from_favorites(delete_id):
    '''Удаляем пользователя из Избранного'''
    session = Session()
    session.query(Favorites).filter_by(favorite_user_id=delete_id).delete()


@dbconnect
def add_to_blacklist(user_info, matched_user_info):
    '''Добавляем пользователя в Черный список (и удаляем из Избранного)'''
    session = Session()
    if not check_users(matched_user_info['user_id']):
        add_new_user(matched_user_info)
    if check_favorites(matched_user_info['user_id']):
        delete_from_favorites(matched_user_info['user_id'])
    if not check_black_list(matched_user_info['user_id']):
        new_blacklist_user = Black_list(user_id=user_info['user_id'], black_list_id=matched_user_info['user_id'])
        session.add(new_blacklist_user)


def check_black_list(checking_id):
    '''Проверка наличия пользователя в Черном списке'''
    session = Session()
    checking_users = session.query(Black_list).filter_by(black_list_id=checking_id).first()
    return checking_users is not None


def favorites_list_output(user_id):
    '''Вывод списка Избранного'''
    session = Session()
    result = session.query(Users).join(Favorites, (Favorites.favorite_user_id == Users.user_id)).filter(
        Favorites.user_id == user_id).all()
    favorites_list = []
    for user in result:
        favorites_list.append({'id': user.user_id, 'first_name': user.first_name, 'last_name': user.last_name,
                               'user_link': user.user_link})
    return favorites_list


if __name__ == "__main__":
    matched_user_info = dict(user_id=888, first_name='qasd', last_name='qzxc', city=15, age=97)
    user_info = dict(user_id=1321, first_name='asd', last_name='zxc', city=5, age=7)
    # user = add_new_user(matched_user_info)
    # print(check_users(1321))
    # add_to_favorites(user_info, matched_user_info)
    print(check_black_list(11111))
    # add_to_blacklist(user_info, matched_user_info)
    # print(check_favorites(13221))
    # pprint(favorites_list_output(132))

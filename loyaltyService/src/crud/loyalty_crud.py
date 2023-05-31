from time import time

from src.db.database import SessionLocal
from src.db.point_db import Reward


def get_points(user_id, db):
    rewards = get_active_rewards(user_id, db)
    points = 0
    for reward in rewards:
        points += reward.points
    return points


def get_active_rewards(user_id, db: SessionLocal):
    return db.query(Reward).filter(Reward.date > int(time()), Reward.user_id == user_id).all()


def add_reward(reward, db):
    db_item = Reward(points=reward.points, user_id=reward.user_id, date=int(time()) + ONE_YEAR)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


ONE_YEAR = 3600 * 24 * 365

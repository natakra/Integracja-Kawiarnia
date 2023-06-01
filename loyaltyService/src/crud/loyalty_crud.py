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
    return db.query(Reward).filter(Reward.date > int(time()), Reward.user_id == user_id).order_by(
        Reward.date.asc()).all()


def add_reward(user_id, price, db):
    db_item = Reward(points=int(price), user_id=user_id, date=int(time()) + ONE_YEAR)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def collect_reward(points_to_collect, user_id, db):
    active_rewards = get_active_rewards(user_id, db)
    collected_points = 0
    for reward in active_rewards:
        if reward.points <= (points_to_collect - collected_points):
            db.query(Reward).filter(Reward.id == reward.id).delete()
            db.commit()
            collected_points += reward.points
        else:
            db.query(Reward).filter(Reward.id == reward.id).update({
                "points": (reward.points - (points_to_collect - collected_points))
            })
            db.commit()


ONE_YEAR = 3600 * 24 * 365

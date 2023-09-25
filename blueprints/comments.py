from sqlalchemy import func

from exts import db
from models import Comment


def calculate_product_star_rating(product_id):
    avg_rating = db.session.query(
        func.avg(Comment.rating).label('average_rating')
    ).filter_by(product_id=product_id).first()

    if avg_rating:
        return round(avg_rating[0])
    return 0

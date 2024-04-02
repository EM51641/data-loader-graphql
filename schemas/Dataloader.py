from promise import Promise
from promise.dataloader import DataLoader
from db.tables import PostEntity
from db.extension import db


class PostLoader(DataLoader):
    def batch_load_fn(self, user_ids):
        # Fetch all posts for the given user_ids in a single SQL query

        posts = (
            db.session.query(PostEntity).filter(PostEntity.user_id.in_(user_ids)).all()
        )

        # Create a dictionary that maps user_ids to their corresponding posts
        posts_by_user_id = {}
        for post in posts:
            if post.user_id not in posts_by_user_id:
                posts_by_user_id[post.user_id] = []
            posts_by_user_id[post.user_id].append(post)

        # Return the posts for each user_id
        return Promise.resolve(
            [posts_by_user_id.get(user_id, []) for user_id in user_ids]
        )

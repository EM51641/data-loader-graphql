import graphene  # type: ignore
from db.extension import db
from db.tables import UserEntity, PostEntity


class User(graphene.ObjectType):
    """
    User schema
    """

    id = graphene.ID(required=True)
    username = graphene.String()
    email = graphene.String()
    posts = graphene.List(lambda: Post)

    class Meta:
        name = "User"
        interfaces = (graphene.relay.Node,)

    @staticmethod
    def get_node(info, id):
        user = db.session.query(UserEntity).filter(UserEntity.id == id).one()
        return User(id=user.id, email=user.email, username=user.username)

    def resolve_posts(self, info):
        return info.context["post_loader"].load(self.id)


class Post(graphene.ObjectType):
    """
    Post schema
    """

    id = graphene.ID(required=True)
    title = graphene.String()
    content = graphene.String()
    user = graphene.Field(User)

    class Meta:
        name = "Post"
        interfaces = (graphene.relay.Node,)

    @staticmethod
    def get_node(info, id: int):
        post = db.session.query(PostEntity).filter(PostEntity.id == id).one()
        return Post(id=post.id, title=post.title, content=post.content)


class Query(graphene.ObjectType):
    """
    Query class
    """

    node = graphene.relay.Node.Field()
    user = graphene.Field(User, id=graphene.ID(required=True))
    users = graphene.List(User)
    posts = graphene.List(Post)

    def resolve_user(self, info, id):
        user = db.session.query(UserEntity).filter(UserEntity.id == id).first()
        return user

    def resolve_users(self, info):
        users = db.session.query(UserEntity).all()
        return users

    def resolve_posts(self, info):
        return db.session.query(PostEntity).all()

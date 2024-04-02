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
    posts = graphene.relay.ConnectionField(lambda: PostConnection)

    class Meta:
        name = "User"
        interfaces = (graphene.relay.Node,)

    @staticmethod
    def get_node(info, id):
        user = db.session.query(UserEntity).filter(UserEntity.id == id).one()
        return User(id=user.id, email=user.email, username=user.username)

    def resolve_posts(self, info, first=None, last=None, before=None, after=None):
        return info.context["post_loader"].load(self.id)


class Post(graphene.ObjectType):
    """
    Represents a Post object in the GraphQL API.

    Attributes:
        id (graphene.ID): The unique identifier of the post.
        title (graphene.String): The title of the post.
        content (graphene.String): The content of the post.
        user (graphene.Field): The user associated with the post.
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
        """
        Retrieve a Post object by its ID.

        Args:
            info (graphene.ResolveInfo): The resolve info object.
            id (int): The ID of the post to retrieve.

        Returns:
            Post: The Post object with the specified ID.
        """
        post = db.session.query(PostEntity).filter(PostEntity.id == id).one()
        return Post(id=post.id, title=post.title, content=post.content)


class PostConnection(graphene.relay.Connection):
    """
    A connection class for the Post GraphQL type.

    This connection class is used to paginate and retrieve a list of Post objects.

    Attributes:
        node (graphene.ObjectType): The GraphQL type for the individual nodes in the connection.

    """

    class Meta:  # type: ignore
        node = Post


class Query(graphene.ObjectType):
    """
    Query class
    """

    node = graphene.relay.Node.Field()
    user = graphene.Field(User, id=graphene.ID(required=True))
    post = graphene.Field(Post, id=graphene.ID(required=True))
    users = graphene.List(User)

    def resolve_user(self, info, id):
        user = db.session.query(UserEntity).filter(UserEntity.id == id).first()
        return user

    def resolve_users(self, info):
        users = db.session.query(UserEntity).all()
        return users

    def resolve_posts(self, info):
        return db.session.query(PostEntity).all()

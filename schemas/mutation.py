import graphene  # type: ignore
from db.tables import UserEntity, PostEntity
from db.extension import db
from schemas.query import User as UserType, Post as PostType


class UserMutation(graphene.Mutation):
    """
    Represents a GraphQL mutation for creating a new user.
    """

    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, email):
        """
        Mutates the GraphQL schema by creating a new user with the given username and email.

        Args:
            info: The GraphQL ResolveInfo object.
            username: The username of the new user.
            email: The email of the new user.

        Returns:
            A UserMutation object containing the newly created user.
        """
        user = UserEntity(username=username, email=email)
        db.add(user)
        db.commit()
        return UserMutation(user=user)


class PostMutation(graphene.Mutation):
    """
    Mutation for creating a new post.

    Args:
        user_id (graphene.ID): The ID of the user creating the post.
        title (str): The title of the post (required).
        content (str): The content of the post (required).

    Returns:
        PostMutation: The created post mutation.

    """

    post = graphene.Field(PostType)

    class Arguments:
        user_id = graphene.ID()
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, user_id, title, content):
        """
        Create a new post with the given title, content, and user ID.

        Args:
            info (obj): The GraphQL ResolveInfo object.
            user_id (int): The ID of the user creating the post.
            title (str): The title of the post.
            content (str): The content of the post.

        Returns:
            obj: The newly created PostMutation object.

        """
        new_post = PostEntity(title=title, content=content, user_id=user_id)
        db.add(new_post)
        db.commit()
        return PostMutation(post=new_post)


class Mutation(graphene.ObjectType):
    mutate_user = UserMutation.Field()
    mutate_post = PostMutation.Field()

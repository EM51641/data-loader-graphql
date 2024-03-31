from flask_graphql import GraphQLView  # type: ignore
from schemas.Dataloader import PostLoader
from schemas import schema


ctx = {"post_loader": PostLoader()}
view_func = GraphQLView.as_view(
    "graphql", schema=schema, graphiql=True, get_context=lambda: ctx
)

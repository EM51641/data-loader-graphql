import graphene  # type: ignore

from schemas.mutation import Mutation
from schemas.query import Query


schema = graphene.Schema(query=Query, mutation=Mutation)

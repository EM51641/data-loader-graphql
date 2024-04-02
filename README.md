# Build a GraphQL API with Graphene, SQLAlchemy, Flask, and Promise

This project demonstrates how to build a GraphQL API using Graphene, SQLAlchemy, Flask, and Promise. It includes a simple data model with users and posts, and provides GraphQL queries to fetch and manipulate the data. The Promise library is used to implement the DataLoader pattern for efficient loading of data.

## Installation

To install the project, you need to have Python and Poetry installed. Then, you can clone the repository and install the dependencies:

```sh
git clone https://github.com/EM51641/dataloader-graphql.git
cd data-loader-graphql
poetry install
```

## Getting Started

Before you can run the project, you need to set up your environment variables.

```sh
export SQLALCHEMY_DATABASE_URI=sqlite:///data.db
```

This command creates a new file named .env in the root of the project and adds a line to it that sets the `SQLALCHEMY_DATABASE_URI` environment variable. This variable tells SQLAlchemy where your database is located. In this example, it's set to use a SQLite database named data.db in the root of the project. You can replace `sqlite:///data.db` with the URI for your own database.

## Running the Project

To run the project, use the following command:

```sh
poetry run python main.py
```

This will start the Flask server on http://localhost:5000

## GraphQL Queries

Here are some example GraphQL queries that you can run on this API.

### Create a User

```graphql
mutation {
  CreateUser(username: "newuser", email: "newuser@example.com") {
    user {
      id
      username
      email
    }
  }
}
```

### Create a Post

```graphql
mutation {
  CreatePost(title: "New Post", content: "This is a new post.", user_id: 1) {
    post {
      id
      title
      content
    }
  }
}
```

### Fetch five user's posts

```graphql
query {
  users {
    id
    email
    username
    posts(first: 5) {
      edges {
        node {
          id
          content
          title
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

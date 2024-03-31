# Build a GraphQL API with Graphene, SQLAlchemy, Flask, and Promise

This project demonstrates how to build a GraphQL API using Graphene, SQLAlchemy, Flask, and Promise. It includes a simple data model with users and posts, and provides GraphQL queries to fetch and manipulate the data. The Promise library is used to implement the DataLoader pattern for efficient loading of data.

## Installation

To install the project, you need to have Python and Poetry installed. Then, you can clone the repository and install the dependencies:

```sh
git clone https://github.com/EM51641/dataloader-graphql.git
cd data-loader-graphql
poetry install
```

##

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
  mutateUser(username: "newuser", email: "newuser@example.com") {
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
  mutatePost(title: "New Post", content: "This is a new post.", user_id: 1) {
    post {
      id
      title
      content
    }
  }
}
```

### Fetch All Users

```graphql
query {
  users {
    id
    username
    email
  }
}
```

### Fetch a Single User

```graphql
query {
  user(id: "1") {
    id
    username
    email
  }
}
```

### Fetch All Posts

```graphql
query {
  posts {
    id
    title
    content
  }
}
```

from app.tests.factory import (
    UserFactory,
    PostFactory,
)
from app.posts.cached_schema_factory import CachedSchemaFactory


def test_get_posts_cloth(client):
    """
    Tests if the posts get request is successfull
    """
    post = PostFactory()
    response = client.get(f"/api/posts/{post.id}/")

    assert response.status_code == 200
    assert CachedSchemaFactory.schema_class_cache != {}
    assert response.json()["id"] == post.id

    assert not response.json().get("posts")
    assert not response.json().get("comments")
    assert not response.json().get("user")


def test_get_posts_user(client):
    """
    Tests if the posts get request is successfull and has user
    """
    user = UserFactory()
    post = PostFactory(user=user)

    response = client.get(f"/api/posts/{post.id}/?include=user")

    assert response.status_code == 200
    assert CachedSchemaFactory.schema_class_cache != {}
    assert response.json()["id"] == post.id

    assert not response.json().get("tags")
    assert not response.json().get("comments")
    assert response.json()["user"]["id"] == user.id


def test_get_posts_comments_tags_user(client):
    """
    Tests if the posts get request is successfull and returns nested objects
    """
    user = UserFactory()
    post = PostFactory(user=user)

    response = client.get(f"/api/posts/{post.id}/?include=user,comments,tags")

    assert response.status_code == 200
    assert CachedSchemaFactory.schema_class_cache != {}
    assert response.json()["id"] == post.id

    assert len(response.json()["tags"]) == 3
    assert len(response.json()["comments"]) == 3
    assert response.json()["user"]["id"] == user.id


def test_get_post_expected_fail_400(client):
    """
    Tests if the post get request is failing expectedly
    """

    post = PostFactory()
    response = client.get(f"/api/posts/{post.id}?include=test,test1")

    assert response.status_code == 400


def test_get_post_expected_fail_404(client):
    """
    Tests if the posts get request is failing expectedly
    """

    response = client.get("/api/posts/32?include=user")
    assert response.status_code == 404

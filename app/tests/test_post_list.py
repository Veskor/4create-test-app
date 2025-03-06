from app.tests.factory import (
    UserFactory,
    PostFactory,
)
from app.posts.cached_schema_factory import CachedSchemaFactory


def test_get_posts_cloth(client):
    """
    Tests if the posts get request is successfull
    """
    PostFactory.create_batch(3)
    response = client.get("/api/posts/")

    assert response.status_code == 200
    assert CachedSchemaFactory.schema_class_cache != {}
    assert len(response.json()) == 3

    for item in response.json():
        assert not item.get("posts")
        assert not item.get("comments")
        assert not item.get("user")


def test_get_posts_user(client):
    """
    Tests if the posts get request is successfull and has user
    """
    user = UserFactory()
    PostFactory.create_batch(3, user=user)

    response = client.get("/api/posts/?include=user")

    assert response.status_code == 200
    assert CachedSchemaFactory.schema_class_cache != {}
    assert len(response.json()) == 3

    for item in response.json():
        assert not item.get("tags")
        assert not item.get("comments")
        assert item["user"]["id"] == user.id


def test_get_posts_comments_tags_user(client):
    """
    Tests if the posts get request is successfull and returns nested objects
    """
    user = UserFactory()
    PostFactory.create_batch(3, user=user)

    response = client.get("/api/posts/?include=user,comments,tags")

    assert response.status_code == 200
    assert CachedSchemaFactory.schema_class_cache != {}
    assert len(response.json()) == 3

    for item in response.json():
        assert len(item["tags"]) == 3
        assert len(item["comments"]) == 3
        assert item["user"]["id"] == user.id


def test_get_post_expected_fail_400(client):
    """
    Tests if the post get request is failing expectedly
    """

    post = PostFactory()
    response = client.get(f"/api/posts/{post.id}?include=test,test1")

    assert response.status_code == 400

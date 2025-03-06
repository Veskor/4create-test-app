from app.tests.factory import UserFactory, PostFactory, CommentFactory
from app.posts.cached_schema_factory import CachedSchemaFactory


def test_get_user_cloth(client):
    """
    Tests if the user get request is successfull
    """
    user = UserFactory()

    response = client.get(f"/api/users/{user.id}")

    assert response.json()["id"] == user.id
    assert not response.json().get("posts")
    assert not response.json().get("comments")
    assert CachedSchemaFactory.schema_class_cache != {}

    assert response.status_code == 200


def test_get_user_with_posts(client):
    """
    Tests if the user get request is successfull and has posts.
    """

    user = UserFactory()
    PostFactory.create_batch(3, user=user)

    response = client.get(f"/api/users/{user.id}?include=posts")

    assert response.json()["id"] == user.id
    assert len(response.json().get("posts")) == 3
    assert not response.json().get("comments")
    assert CachedSchemaFactory.schema_class_cache != {}
    assert response.status_code == 200


def test_get_user_with_comments_posts(client):
    """
    Tests if the user get request is successfull and has posts & comments.
    """

    user = UserFactory()
    post = PostFactory(user=user)
    CommentFactory.create_batch(3, user=user, post=post)

    response = client.get(f"/api/users/{user.id}?include=posts,comments")

    assert response.json()["id"] == user.id
    assert len(response.json().get("posts")) == 1
    assert len(response.json().get("comments")) == 3
    assert CachedSchemaFactory.schema_class_cache != {}
    assert response.status_code == 200


def test_get_user_expected_fail_400(client):
    """
    Tests if the user get request is failing expectedly
    """

    user = UserFactory()
    response = client.get(f"/api/users/{user.id}?include=test,test1")

    assert response.status_code == 400


def test_get_user_expected_fail_404(client):
    """
    Tests if the user get request is failing expectedly
    """

    response = client.get("/api/users/32?include=posts")
    assert response.status_code == 404

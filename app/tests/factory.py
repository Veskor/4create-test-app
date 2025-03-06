import factory
from factory import fuzzy
from factory.alchemy import SQLAlchemyModelFactory
from app.posts.constants import PostStatus
from app.posts.models import User, Post, Comment, Tag
from app.core.db.mock_session import TestingSessionLocal


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = TestingSessionLocal()
        sqlalchemy_session_persistence = "flush"


class UserFactory(BaseFactory):
    class Meta:
        model = User

    name = fuzzy.FuzzyText(length=8, prefix="user_")


class TagFactory(BaseFactory):
    class Meta:
        model = Tag
        sqlalchemy_get_or_create = ("name",)  # Prevent duplicate tags

    name = factory.Sequence(lambda n: f"tag_{n}")


class PostFactory(BaseFactory):
    class Meta:
        model = Post

    title = fuzzy.FuzzyText(length=15, prefix="post_")
    content = fuzzy.FuzzyText(length=50)
    status = PostStatus.draft
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:  # Skip if not created (just building, not persisting)
            return

        if extracted:  # If tags are passed explicitly
            self.tags.extend(extracted)
        else:  # Default to 3 random tags
            for _ in range(3):
                self.tags.append(TagFactory())

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        if not create:  # Skip if not created (just building, not persisting)
            return

        if extracted:  # If tags are passed explicitly
            self.comments.extend(extracted)
        else:  # Default to 3 random tags
            for _ in range(3):
                CommentFactory(post=self)


class CommentFactory(BaseFactory):
    class Meta:
        model = Comment

    content = fuzzy.FuzzyText(length=30)
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)

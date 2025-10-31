# core/blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", args=[self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [(DRAFT, "Draft"), (PUBLISHED, "Published")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=230, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(Tag, blank=True)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    excerpt = models.TextField(max_length=300, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PUBLISHED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            i = 1
            while Post.objects.filter(slug=slug).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


# Tag.objects.exclude(post__title="abc", post__content="123")
# SELECT "blog_tag"."id", "blog_tag"."name", "blog_tag"."slug"
# FROM "blog_tag"
# WHERE NOT
# (
#     EXISTS(
#         SELECT 1 AS "a"
#         FROM "blog_post_tags" U1
#         INNER JOIN "blog_post" U2
#         ON (U1."post_id" = U2."id")
#         WHERE (U2."content" = 123 AND U1."tag_id" = ("blog_tag"."id"))
#         LIMIT 1
#     )
#     AND
#     EXISTS(
#         SELECT 1 AS "a"
#         FROM "blog_post_tags" U1
#         INNER JOIN "blog_post" U2
#         ON (U1."post_id" = U2."id")
#         WHERE (U2."title" = abc AND U1."tag_id" = ("blog_tag"."id"))
#         LIMIT 1
#     )
# )


# Post.objects.exclude(title="This is a title", content="This is a content")
# SELECT "blog_post"."id", "blog_post"."title", "blog_post"."slug", "blog_post"."author_id", "blog_post"."category_id", "blog_post"."cover", "blog_post"."excerpt", "blog_post"."content", "blog_post"."status", "blog_post"."created", "blog_post"."updated"
# FROM "blog_post"
# WHERE NOT
# (
#     "blog_post"."content" = This is a content
#     AND "blog_post"."title" = This is a title
# )
# ORDER BY "blog_post"."created" DESC


# Tag.objects.filter(post__title="This is a title", post__content="This is a content")
# SELECT "blog_tag"."id", "blog_tag"."name", "blog_tag"."slug"
# FROM "blog_tag"
# INNER JOIN "blog_post_tags" ON ("blog_tag"."id" = "blog_post_tags"."tag_id")
# INNER JOIN "blog_post" ON ("blog_post_tags"."post_id" = "blog_post"."id")
# WHERE ("blog_post"."content" = This is a content AND "blog_post"."title" = This is a title)


# Post.objects.exclude(tags__name="tag1", tags__slug="tag1_slug")
# SELECT "blog_post"."id", "blog_post"."title", "blog_post"."slug", "blog_post"."author_id", "blog_post"."category_id", "blog_post"."cover", "blog_post"."excerpt", "blog_post"."content", "blog_post"."status", "blog_post"."created", "blog_post"."updated"
# FROM "blog_post"
# WHERE NOT
# (
#     EXISTS(
#         SELECT 1 AS "a"
#         FROM "blog_post_tags" U1
#         INNER JOIN "blog_tag" U2
#         ON (U1."tag_id" = U2."id")
#         WHERE (U2."name" = tag1 AND U1."post_id" = ("blog_post"."id"))
#         LIMIT 1
#     )
#     AND
#     EXISTS(
#         SELECT 1 AS "a"
#         FROM "blog_post_tags" U1
#         INNER JOIN "blog_tag" U2
#         ON (U1."tag_id" = U2."id")
#         WHERE (U2."slug" = tag1_slug AND U1."post_id" = ("blog_post"."id"))
#         LIMIT 1
#     )
# )
# ORDER BY "blog_post"."created" DESC

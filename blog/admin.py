# core/blog/admin.py
from django.contrib import admin
from .models import Post, Category, Tag, Comment


class TagInline(admin.TabularInline):
    """Tabular Inline View for Post"""

    model = Tag.post_set.through
    min_num = 3
    max_num = 20
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created")
    list_filter = ("status", "created", "category", "tags")
    search_fields = ("title", "content", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("tags",)
    date_hierarchy = "created"
    ordering = ("-created",)

    inlines = [CommentInline, TagInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PostInline(admin.TabularInline):
    """Tabular Inline View for Post"""

    model = Post.tags.through
    min_num = 3
    max_num = 20
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)  # ✅ Added this line!

    inlines = [
        PostInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "active", "created")
    list_filter = ("active", "created")
    search_fields = ("name", "email", "body")

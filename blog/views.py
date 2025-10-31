# core/blog/views.py
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Category, Tag
from .forms import CommentForm, SearchForm


class HomeView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return (
            Post.objects.filter(status=Post.PUBLISHED)
            .select_related("author", "category")
            .prefetch_related("tags")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_form"] = SearchForm(self.request.GET or None)
        ctx["categories"] = Category.objects.all()
        ctx["tags"] = Tag.objects.all()[:20]
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = self.object
            c.save()
            return redirect(f"{self.object.get_absolute_url()}#comments")
        ctx = self.get_context_data(object=self.object)
        ctx["form"] = form
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = CommentForm()
        ctx["related"] = (
            Post.objects.filter(status=Post.PUBLISHED, category=self.object.category)
            .exclude(id=self.object.id)
            .prefetch_related("tags")[:3]
        )
        return ctx


class CategoryView(HomeView):
    template_name = "blog/list.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.objects.filter(status=Post.PUBLISHED, category=self.category)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = f"Category: {self.category.name}"
        return ctx


class TagView(HomeView):
    template_name = "blog/list.html"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return Post.objects.filter(status=Post.PUBLISHED, tags=self.tag)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = f"Tag: {self.tag.name}"
        return ctx


class SearchView(HomeView):
    template_name = "blog/list.html"

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        return Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(excerpt__icontains=q),
            status=Post.PUBLISHED,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["heading"] = "Search results"
        return ctx

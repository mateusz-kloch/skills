from django.http import Http404
from django.views import generic
from django.urls import reverse_lazy

from .forms import UserRegisterForm
from .models import Article, Author, Tag


class ArticleListView(generic.ListView):
    template_name = 'library/article_list.html'
    context_object_name = 'published_articles_list'

    def get_queryset(self):
        """
        Returns a query set that includes verified articles
        whose pub_date is present or past.
        """
        return Article.verified_objects.all()
    

class ArticleDetailView(generic.DetailView):
    template_name = 'library/article_detail.html'

    def get_object(self):
        """
        Returns verified article whose slug was provided in the request.
        If it not exists, raises 404.
        """
        try:
            return Article.verified_objects.get(slug=self.kwargs['slug'])
        except Article.DoesNotExist:
            raise Http404


class AuthorListView(generic.ListView):
    emplate_name = 'library/author_list.html'
    context_object_name = 'authors_list'

    def get_queryset(self):
        """
        Returns a query set that includes authors of published articles.
        """
        return Author.objects.all()


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'library/author_detail.html'

    def get_context_data(self, **kwargs):
        """
        Returns a queryset of articles related with an author,
        excludes defective articles.
        """
        context = super().get_context_data(**kwargs)
        author_obj = self.get_object()
        articles = Article.verified_objects.filter(author__slug=author_obj.slug)
        context['articles'] = articles
        return context


class TagListView(generic.ListView):
    template_name = 'library/tag_list.html'
    context_object_name = 'available_tags_list'

    def get_queryset(self):
        """
        Returns query set of all tags in database.
        """
        return Tag.objects.all()
    

class TagDetailView(generic.DetailView):
    model = Tag
    template_name = 'library/tag_detail.html'

    def get_context_data(self, **kwargs):
        """
        Returns a query set of verified articles whose
        tags contain the tag with primary key provided in the request.
        """
        context = super().get_context_data(**kwargs)
        tag_obj = self.get_object()
        articles = Article.verified_objects.filter(tags__slug=tag_obj.slug)
        context['articles'] = articles
        return context
    

class UserRegisterView(generic.FormView):
    form_class = UserRegisterForm
    template_name = 'library/user_register.html'
    success_url = reverse_lazy('library:user-login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

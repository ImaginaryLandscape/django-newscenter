from django import template
from django.template import Library, Node
from newscenter.models import Category

register = Library()


class FeaturedNode(Node):
    def __init__(self, newsroom):
        self.newsroom = template.Variable(newsroom)

    def render(self, context):
        try:
            from django.apps import apps
            model = apps.get_model('newscenter', 'Newsroom')
        except ImportError:
            from django.db.models import get_model
            model = get_model('newscenter', 'Newsroom')
        except:
            raise template.TemplateSyntaxError("Failed to retrieve model")
        try:
            newsroom_slug = self.newsroom.resolve(context)
            newsroom = model.objects.get(slug=newsroom_slug)
            context['newsroom'] = newsroom
            context['featured_list'] = newsroom.articles.get_featured()
        except:
            pass

        return ''

    def get_news(parser, token):
        try:
            tag_name, newsroom = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError("get_news requires a newsroom")

        return FeaturedNode(newsroom)

    get_news = register.tag(get_news)


class CategoryNode(Node):
    def render(self, context):
        try:
            context['category_list'] = Category.objects.all()
        except:
            raise template.TemplateSyntaxError("")

        return ''

    def show_categories(parser, token):
        return CategoryNode()

    show_categories = register.tag(show_categories)

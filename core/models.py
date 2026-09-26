from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    headline = models.CharField(max_length=160, default='A little green space. A lot of community.')
    intro = models.TextField(default='We’re the Friends of Larkhall Park — neighbours working together to care for our park and bring our community together.')
    membership_intro = models.TextField(default='Love your local park? Become a Friend for £5 a year and help support its future. Every member makes our community stronger.')
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    content_panels = Page.content_panels + [FieldPanel('headline'), FieldPanel('intro'), FieldPanel('hero_image'), FieldPanel('membership_intro')]
    max_count = 1
    subpage_types = ['core.ContentPage', 'core.NewsIndexPage', 'core.EventsIndexPage']

    def get_context(self, request):
        context = super().get_context(request)
        context['news_items'] = NewsPage.objects.live().public().descendant_of(self).filter(date__lte=timezone.localdate()).order_by('-date', '-pk')[:3]
        context['events'] = EventPage.objects.live().public().descendant_of(self).filter(start__gte=timezone.now()).order_by('start')[:3]
        return context


class ContentPage(Page):
    intro = models.TextField(blank=True)
    body = RichTextField(blank=True)
    kind = models.CharField(max_length=20, default='standard', choices=[('standard', 'Standard'), ('volunteering', 'Volunteering'), ('membership', 'Membership placeholder'), ('donate', 'Donation placeholder')])
    content_panels = Page.content_panels + [FieldPanel('intro'), FieldPanel('body'), FieldPanel('kind')]
    parent_page_types = ['core.HomePage']
    subpage_types = []


class NewsIndexPage(Page):
    parent_page_types = ['core.HomePage']
    subpage_types = ['core.NewsPage']

    def get_context(self, request):
        context = super().get_context(request)
        context['news_items'] = NewsPage.objects.child_of(self).live().public().filter(date__lte=timezone.localdate()).order_by('-date', '-pk')
        return context


class NewsPage(Page):
    date = models.DateField(default=timezone.localdate)
    category = models.CharField(max_length=60, default='Park news')
    summary = models.TextField()
    body = RichTextField()
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    is_demo = models.BooleanField(default=False, help_text='Clearly label fictional prototype content.')
    content_panels = Page.content_panels + [FieldPanel('date'), FieldPanel('category'), FieldPanel('summary'), FieldPanel('image'), FieldPanel('body'), FieldPanel('is_demo')]
    parent_page_types = ['core.NewsIndexPage']
    subpage_types = []


class EventsIndexPage(Page):
    parent_page_types = ['core.HomePage']
    subpage_types = ['core.EventPage']

    def get_context(self, request):
        context = super().get_context(request)
        context['events'] = EventPage.objects.child_of(self).live().public().filter(start__gte=timezone.now()).order_by('start')
        return context


class EventPage(Page):
    start = models.DateTimeField()
    location = models.CharField(max_length=200, default='Larkhall Park')
    summary = models.TextField()
    body = RichTextField()
    is_demo = models.BooleanField(default=False)
    content_panels = Page.content_panels + [FieldPanel('start'), FieldPanel('location'), FieldPanel('summary'), FieldPanel('body'), FieldPanel('is_demo')]
    parent_page_types = ['core.EventsIndexPage']
    subpage_types = []

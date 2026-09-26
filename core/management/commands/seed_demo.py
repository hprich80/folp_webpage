from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from wagtail.models import Page, Site
from core.models import HomePage, ContentPage, NewsIndexPage, NewsPage, EventsIndexPage, EventPage


class Command(BaseCommand):
    help = 'Create prototype pages and clearly labelled sample content. Safe to run again.'

    @transaction.atomic
    def handle(self, *args, **options):
        if HomePage.objects.exists():
            self.stdout.write('Prototype already exists; existing edits have been preserved.')
            return
        root = Page.get_first_root_node()
        home = root.add_child(instance=HomePage(title='Home', slug='folp'))
        home.save_revision().publish()
        site = Site.objects.filter(is_default_site=True).first()
        if site:
            site.root_page = home
            site.hostname = 'localhost'
            site.port = 8000
            site.site_name = 'Friends of Larkhall Park'
            site.save()
        else:
            Site.objects.create(hostname='localhost', port=8000, root_page=home, is_default_site=True)

        def publish(parent, page):
            parent.add_child(instance=page)
            page.save_revision().publish()
            return page

        publish(home, ContentPage(title='About', slug='about', show_in_menus=True,
            intro='Local people, working together for a park everyone can enjoy.',
            body='<p>The Friends of Larkhall Park is a group of local residents who care about the park and its place in our community. Formed in 1996, the Friends work to improve the park for the people who use it.</p><h2>A shared space, a shared future.</h2><p>We bring neighbours together, support volunteering and help people take part in caring for their local green space. Our community garden is one of the ways to get involved.</p><p>Have an idea or want to lend a hand? Email info@larkhallparkfriends.org.uk.</p>'))
        publish(home, ContentPage(title='Volunteering', slug='volunteering', show_in_menus=True, kind='volunteering',
            intro='Fresh air, friendly faces and something worthwhile. Find a way to help that feels right for you.'))
        news = publish(home, NewsIndexPage(title='News', slug='news', show_in_menus=True))
        events = publish(home, EventsIndexPage(title='Events', slug='events', show_in_menus=True))
        publish(home, ContentPage(title='Donate', slug='donate', kind='donate', intro='Help care for the green space we share.'))
        publish(home, ContentPage(title='Become a member', slug='membership', kind='membership', intro='Join the Friends of Larkhall Park for £5 a year.'))
        for days, title, slug, category, summary in [
            (1, 'Growing together in the community garden', 'growing-together', 'Community garden', 'A place to grow, share skills and get to know the people who live nearby.'),
            (5, 'Small actions, a greener park', 'a-greener-park', 'Volunteering', 'Meet the different ways neighbours can lend a hand around Larkhall Park.'),
            (10, 'A fresh chapter for the Friends', 'a-fresh-chapter', 'Friends of the park', 'Making it easier to find park news, get involved and stay connected.')]:
            publish(news, NewsPage(title=title, slug=slug, date=timezone.localdate()-timedelta(days=days), category=category,
                summary=summary, is_demo=True, body='<p>This is sample content for reviewing the website prototype. Replace it with an approved update before publishing the site.</p><p>News articles can include text, photographs and links. Editors can save a draft, preview their changes and publish when ready.</p>'))
        for days, title, slug, summary in [
            (8, 'Community garden morning', 'community-garden-morning', 'A sample listing for a morning of growing together.'),
            (15, 'Neighbourhood litter pick', 'neighbourhood-litter-pick', 'A sample listing for neighbours helping care for the park.'),
            (22, 'Friends of the park get-together', 'friends-get-together', 'A sample listing for sharing ideas about our park.')]:
            start = (timezone.now()+timedelta(days=days)).replace(hour=9, minute=0, second=0, microsecond=0)
            publish(events, EventPage(title=title, slug=slug, start=start, summary=summary, is_demo=True,
                body='<p>This event is fictional and exists only to demonstrate the prototype. Please do not attend based on this listing.</p><p>Once confirmed, editors can add the real date, meeting point, accessibility information and what to bring.</p>'))
        self.stdout.write(self.style.SUCCESS('Prototype pages created. Run createsuperuser to set up an editor login.'))

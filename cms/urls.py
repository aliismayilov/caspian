from django.conf.urls import patterns, url

from cms import views

urlpatterns = patterns('',
    # homepage
    (r'^(?P<lang_name>\w{2,3})/$', views.main_page, name='main_page'),
    (r'^$', 'main_page'),
    
    # search
    (r'^(?P<lang_name>\w{2,3})/search/', views.search, name='search'),
    
    # news entries
    (r'^(?P<lang_name>\w{2,3})/(?P<year>\d{4})/$', views.archive_year, name='archive_year'),
    (r'^(?P<lang_name>\w{2,3})/(?P<year>\d{4})/(?P<month>\w{3})/$', views.archive_month, name='archive_month'),
    (r'^(?P<lang_name>\w{2,3})/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', views.archive_day, name='archive_day'),
    (r'^(?P<lang_name>\w{2,3})/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+).html$', views.entry_detail, name='entry_detail'),
    
    # Pages
    (r'^(?P<lang_name>\w{2,3})/(?P<slug>[-\w]+).html$', views.page_detail, name='page_detail'),
    
    # Polls
    (r'^(?P<lang_name>\w{2,3})/poll/(?P<poll_id>\d*)/vote/$', views.poll_vote, name='poll_vote'),
    
    # Contact
    (r'^(?P<lang_name>\w{2,3})/contact/$', views.contact, name='contact'),
    (r'^(?P<lang_name>\w{2,3})/contact/thanks/$', views.contact_thanks, name='contact_thanks'),
)

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from cms.models import Poll, Entry, Language, Page

import datetime

def main_page(request, lang_name=None):
    if lang_name:
        language = get_object_or_404(Language, small_name=lang_name)
    else:
        language = Language.objects.all()[0]
    
    if request.session.get('poll_%d' % Poll.objects.all()[:1][0].id, False) or request.GET.get('show_result', False):
        show_result = True
    else:
        show_result = False
    
    return render_to_response('cms/%s/cms/main_page.html' % language.small_name, {
            'links': get_latest_links(lang_name),
            'languages': Language.objects.all(),
            'lang_name': language.small_name,
            'top_pages': Page.objects.filter(type=Page.TOP),
            'side_pages': Page.objects.filter(type=Page.SIDE),
            'latest_entries': get_latest_entries(2),
            'poll': Poll.objects.all()[:1][0],
            'show_result': show_result,
        },
        context_instance=RequestContext(request)
    )

def archive_year(request, lang_name, year):
    language = get_object_or_404(Language, small_name=lang_name)
    
    date_list = []
    for i in range(1, 13):
        date_list.append(datetime.datetime.strptime(year + str(i), "%Y%m"))
    
    return render_to_response('cms/%s/cms/entry_archive_year.html' % language.small_name, {
            'languages': Language.objects.all(),
            'lang_name': language.small_name,
            'top_pages': Page.objects.filter(type=Page.TOP),
            'side_pages': Page.objects.filter(type=Page.SIDE),
            'year': year,
            'date_list': date_list,
        },
        context_instance=RequestContext(request)
    )

def archive_month(request, lang_name, year, month):
    language = get_object_or_404(Language, small_name=lang_name)
    sub_date = datetime.datetime.strptime(year + month, "%Y%b")
    
    month = int(sub_date.month)
    if (month == 12):
        month = 1
    else:
        month = month + 1
    
    sub_date_one_month = datetime.datetime.strptime(year + str(month), "%Y%m")
    
    entries = get_list_or_404(Entry,
        status=Entry.LIVE_STATUS,
        pub_date__gte=sub_date,
        pub_date__lte=sub_date_one_month
    )
    
    paginator = Paginator(entries, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)
    
    return render_to_response('cms/%s/cms/entry_archive_month.html' % language.small_name, {
            'entries': entries,
            'languages': Language.objects.all(),
            'lang_name': language.small_name,
            'top_pages': Page.objects.filter(type=Page.TOP),
            'side_pages': Page.objects.filter(type=Page.SIDE),
            'month': sub_date,
        },
        context_instance=RequestContext(request)
    )

def archive_day(request, lang_name, year, month, day):
    language = get_object_or_404(Language, small_name=lang_name)
    sub_date = datetime.datetime.strptime(year + month + day, "%Y%b%d")
    
    entries = get_list_or_404(Entry,
        status=Entry.LIVE_STATUS,
        pub_date__gte=sub_date,
        pub_date__lte=sub_date + datetime.timedelta(days=1)
    )
    
    paginator = Paginator(entries, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)
    
    return render_to_response('%scms/entry_archive_day.html' % language.small_name, {
            'entries': entries,
            'languages': Language.objects.all(),
            'lang_name': language.small_name,
            'top_pages': Page.objects.filter(type=Page.TOP),
            'side_pages': Page.objects.filter(type=Page.SIDE),
            'day': sub_date,
        },
        context_instance=RequestContext(request)
    )

def entry_detail(request, lang_name, year, month, day, slug):
    language = get_object_or_404(Language, small_name=lang_name)
    sub_date = datetime.datetime.strptime(year + month + day, "%Y%b%d")
    
    entry = get_object_or_404(Entry,
        pub_date__gte=sub_date,
        pub_date__lte=sub_date + datetime.timedelta(days=1),
        slug=slug
    )
    
    entry.view_count += 1
    entry.save()
    
    return render_to_response('cms/%s/cms/entry_detail.html' % language.small_name, {
            'entry': entry,
            'languages': Language.objects.all(),
            'lang_name': language.small_name,
            'top_pages': Page.objects.filter(type=Page.TOP),
            'side_pages': Page.objects.filter(type=Page.SIDE),
        },
        context_instance=RequestContext(request)
    )

def page_detail(request, lang_name, slug):
    language = get_object_or_404(Language, small_name=lang_name)
    page = get_object_or_404(Page, slug__iexact=slug)
    
    return render_to_response('cms/%s/cms/page_detail.html' % language.small_name, {
            'page': page,
            'languages': Language.objects.all(),
            'lang_name': language.small_name,
            'top_pages': Page.objects.filter(type=Page.TOP),
            'side_pages': Page.objects.filter(type=Page.SIDE),
        },
        context_instance=RequestContext(request)
    )

def search(request, lang_name):
    language = get_object_or_404(Language, small_name=lang_name)
    
    query = request.GET.get('q')
    if query:
        entries = Entry.objects.filter(
            status=Entry.LIVE_STATUS,
            index__icontains=query
        )
        
        pages = Page.objects.filter(
            index__icontains=query
        )
        
        return render_to_response('cms/%s/cms/search.html' % language.small_name, {
                'query': query,
                'languages': Language.objects.all(),
                'lang_name': language.small_name,
                'top_pages': Page.objects.filter(type=Page.TOP),
                'side_pages': Page.objects.filter(type=Page.SIDE),
                'search_entries': entries,
                'search_pages': pages,
            },
            context_instance=RequestContext(request)
        )

def poll_vote(request, lang_name, poll_id):
    language = get_object_or_404(Language, small_name=lang_name)
    
    if request.method == 'POST':
        poll = get_object_or_404(Poll, pk=poll_id)
        try:
            selected_choice = poll.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return redirect(reverse('cms.views.main_page', args=(language.small_name,)))
        selected_choice.vote += 1
        selected_choice.save()
        
        request.session['poll_%s' % poll_id] = True
        
        return redirect(reverse('cms.views.main_page', args=(language.small_name,)))
    else:
        redirect(reverse('cms.views.main_page', args=(language.small_name,)))

from cms.forms import ContactForm
def contact(request, lang_name):
    language = get_object_or_404(Language, small_name=lang_name)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['email']
            message = form.cleaned_data['name'] + "\n" + form.cleaned_data['message']
            
            recipients = ['qaralama@gmail.com']
            
            from django.core.mail import send_mail
            try:
                send_mail(subject, message, sender, recipients)
            except:
                pass
            return redirect('/%s/contact/thanks/' % language.small_name)
    else:
        form = ContactForm()
    
    return render_to_response('cms/%s/cms/contact.html' % language.small_name, {
            'form': form,
            'languages': Language.objects.all(),
            'lang_name': language.small_name,
            'top_pages': Page.objects.filter(type=Page.TOP),
            'side_pages': Page.objects.filter(type=Page.SIDE),
        },
        context_instance=RequestContext(request)
    )

def contact_thanks(request, lang_name):
    language = get_object_or_404(Language, small_name=lang_name)
    
    return render_to_response('cms/%s/cms/thanks.html' % language.small_name, {
            'languages': Language.objects.all(),
            'lang_name': language.small_name,
            'top_pages': Page.objects.filter(type=Page.TOP),
            'side_pages': Page.objects.filter(type=Page.SIDE),
        },
        context_instance=RequestContext(request)
    )


def get_latest_entries(count):
    if (count > Entry.objects.count()):
        count = Entry.objects.count()
    return Entry.objects.filter(status=Entry.LIVE_STATUS).all()[:count]

def get_latest_links(lang_name):
    import feedparser
    links = []
    i = 1
    if lang_name == "az":
        feed = feedparser.parse("http://milli.az/rss.php")
        for e in feed.entries:
            if "qtisadiyyat" in e.category:
                links.append((e.title, e.link))
                if (i != 5):
                    i = i + 1
                else:
                    break
    if lang_name == "en":
        feed = feedparser.parse("http://today.az/rss.php")
        for e in feed.entries:
            if "Business" in e.category:
                links.append((e.title, e.link))
                if (i != 5):
                    i = i + 1
                else:
                    break
    else:
        feed = feedparser.parse("http://1news.az/rss.php?sec_id=21")
        for e in feed.entries[:4]:
            links.append((e.title, e.link))
    return links
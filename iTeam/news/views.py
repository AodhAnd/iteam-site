from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.core.files import File
import string
from django.template.defaultfilters import slugify

from iTeam.news.models import News

# Create your views here.

def index(request):
    TYPES = ('N', 'T', 'P')

    # get objects
    news_list = News.objects.all().order_by('-pub_date')

    type = request.GET.get('type')
    if type in TYPES:
        news_list = news_list.filter(type=type)

    # paginator
    paginator = Paginator(news_list, settings.NB_NEWS_PER_PAGE)

    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    # build data for template
    data = {"data":news, "cur_type":type}

    # add active field to proper filter
    if type in TYPES:
        data[''.join(("type_", type))] = "active"
    else:
        data['type_all'] = "active"

    return render(request, 'news/index.html', data)


def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)

    return render(request, 'news/detail.html', {'news': news,})


@login_required(redirect_field_name='suivant')
def create(request):
    # If the form has been submitted ...
    if request.method == 'POST':
        if 'title' in request.POST and 'text' in request.POST:
            news = News()

            news.author = request.user
            news.pub_date = timezone.now()

            news.title = request.POST['title'][:99]
            news.text = request.POST['text']

            if 'subtitle' in request.POST:
                news.subtitle = request.POST['subtitle'][:99]

            if 'image' in request.FILES:
                img = request.FILES['image']
                ext = string.lower(img.name.split('.')[-1])
                error = 0
                if img.size > 1024*1024*1024:
                    print('File too big')
                    error += 1
                if ext not in ('png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp'):
                    print('Not an img')
                    error += 1

                if error == 0:
                    news.image = img
                    news.image.name = '.'.join((slugify(news.title), ext))

            news.save()

            # Redirect after POST
            return HttpResponseRedirect(reverse('news:detail', args=(news.id,)))
        # missing data
        else:
            return render(request, 'news/create.html', {'msg' : 'Missing data'})
    # if no post data sent ...
    else:
        return render(request, 'news/create.html')




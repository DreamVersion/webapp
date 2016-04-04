# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlquote
from .models import WDJ
from django.core.urlresolvers import reverse
from django.utils import timezone
import urllib
import json

# Create your views here.

usable_urls = {
        "search":("http://ias.wandoujia.com/api/v3/search?query=%s",u"搜索"),
        "single":("http://apis.wandoujia.com/five/v2/apps/%s",u"App"),
        "explore":("http://startpage.wandoujia.com/five/v3/tabs/explore?pos=m/explore",u"推荐"),
        "nux":("http://startpage.wandoujia.com/five/v3/tabs/nux?pos=m/essential",u"必备"),
        "apps":("http://startpage.wandoujia.com/five/v3/tabs/apps?pos=m/apps/explore",u"应用"),
        "games":("http://startpage.wandoujia.com/five/v3/tabs/games?pos=m/games/explore",u"游戏"),
        "newgame":("http://startpage.wandoujia.com/five/v3/tabs/newgame?pos=m/tabs/newgame",u"新游戏"),
        "tops":("http://startpage.wandoujia.com/five/v3/tabs/tops?pos=m/tops",u"排行榜")
               }


def index(request):
    if request.GET.has_key('message'):
        print(request.GET['message'])
        return render(request, 'wdj/index.html', {'message': request.GET['message']})
    else:
        return render(request, 'wdj/index.html')
#search single app
def search(request):

    package_name = request.GET['name']

    f = urllib.urlopen(usable_urls['search'][0] % urlquote(package_name))
    result = f.read()
    result_json = json.loads(result)
    entities = result_json['entity']

    return render(request, 'wdj/search_result.html', {'apps': filter(lambda x:x['id']!=0, entities)})

#show single app search result
def result(request):

    app = eval( request.POST['app'] )
    package_name = app['title']

    app_json = json.dumps(app)

    return render(request, 'wdj/result.html', {'name': package_name, 'app': app_json })

#save app json to db
def submit(request):

    app = json.loads(request.POST['app'])
    package_name = app['title']
    package_id = app['detail']['app_detail']['package_name']

    app_json = json.dumps(app)

    #Save to db
    wdj_app = WDJ()
    wdj_app.package_name = package_name
    wdj_app.package_id = package_id
    wdj_app.package_content = app_json
    wdj_app.update_time = timezone.now()
    wdj_app.save()

    return HttpResponseRedirect(reverse('wdj:index') + "?message="+ "Save %s Successfully"% package_name)

#save function json
def fun(request):
    target = request.GET['target']
    apps = WDJ.objects.order_by('-update_time')
    # for app in apps:
    #     print(app.package_name)

    return render(request, "wdj/function.html", {"apps": apps, "target":usable_urls[target][0], "func":usable_urls[target][1]})

def generate_func_json(request):

    target = request.GET['target']

    all_app_list = []
    for (k,v) in request.GET.items():
        all_app_list.append(v)

    WDJ.objects.filter(all_app_list)

    return HttpResponse(all_app_list)
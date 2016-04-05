# coding=utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlquote
from django.conf import settings
from .models import WDJ
from django.core.urlresolvers import reverse
from django.utils import timezone
import urllib,urllib2,httplib
import json
import gzip
import StringIO
import os

# Create your views here.

usable_urls = {
        "search":("http://ias.wandoujia.com/api/v3/search?query=%s","Search"),
        "single":("http://apis.wandoujia.com/five/v2/apps/%s","SingleApp"),
        "explore":("http://startpage.wandoujia.com/five/v3/tabs/explore?pos=m/explore","recommend"),
        "nux":("http://startpage.wandoujia.com/five/v3/tabs/nux?pos=m/essential","essential"),
        "apps":("http://startpage.wandoujia.com/five/v3/tabs/apps?pos=m/apps/explore","apps"),
        "games":("http://startpage.wandoujia.com/five/v3/tabs/games?pos=m/games/explore","games"),
        "newgame":("http://startpage.wandoujia.com/five/v3/tabs/newgame?pos=m/tabs/newgame","newgame"),
        "tops":("http://startpage.wandoujia.com/five/v3/tabs/tops?pos=m/tops","tops")
               }

def findUrlGzip(url):
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    opener = urllib2.build_opener()
    f = opener.open(request)
    isGzip = f.headers.get('Content-Encoding')
    #print isGzip
    if isGzip :
        compresseddata = f.read()
        compressedstream = StringIO.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        data = gzipper.read()
    else:
        data = f.read()
    return data

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

    app_ids = request.POST.getlist('app')
    apps =[json.loads(app.package_content) for app in WDJ.objects.filter(pk__in=app_ids) ]

    target = request.POST['target']

    func_name = request.POST['func']

    result_html = findUrlGzip(target)

    result_json = json.loads(result_html)

    #repalce
    entities = result_json['entity']
    i = 0
    app_size = len(apps)

    for entity in entities:
        if entity.has_key('title'):
            for key in entity:
                if apps[i % app_size].has_key(key):
                    entity[key] = apps[i % app_size][key]
            i+=1
    function = json.dumps(result_json)
    func_filename = os.path.join(settings.BASE_DIR,"json/wdj/"+func_name)

    with open(func_filename,'w') as json_file:
        json_file.write(function)

    return HttpResponseRedirect(reverse('wdj:index')+"?message=Save %s successfully"%func_filename)
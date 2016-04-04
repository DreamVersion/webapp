from django.conf.urls import url
from . import views

app_name = 'wdj'

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^search/result', views.result, name='result'),
    url(r'^search/submit', views.submit, name='submit'),
    url(r'^func$', views.fun, name="function"),
    url(r'^generate', views.generate_func_json, name="generate")
]
from django.contrib import admin

# Register your models here.

from .models import WDJ
# Register your models here.

class WDJAdmin(admin.ModelAdmin):
    fields = ['package_name','package_id','update_time','package_content']
    list_display = ['package_name','package_id','update_time']

admin.site.register(WDJ,WDJAdmin)
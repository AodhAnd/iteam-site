from django.contrib import admin

from iTeam.news.models import News

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    # DETAIL fields for a news
    fieldsets = [
        ('Informations',    {'fields': ['title', 'subtitle', 'pub_date', 'author', 'type']}),
        ('Donnees',         {'fields': ['text', 'image']}),
    ]

    # fields for ALL news
    list_display = ('title', 'subtitle', 'author', 'pub_date', 'type')

    list_filter = ['pub_date', 'author', 'type']
    search_fields = ['title', 'subtitle', 'text']

    # add author name for the news based on the current logged user
    def save_model(self, request, obj, form, change):
        # set user
        obj.author = request.user
        # call the admin model save.
        super(NewsAdmin, self).save_model(request, obj, form, change)


admin.site.register(News, NewsAdmin)

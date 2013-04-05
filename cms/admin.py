from django.contrib import admin

from cms.models import Entry, Language, Page, Poll, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title_ru'] }
    list_filter = ['pub_date',]
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(Entry, EntryAdmin)


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title_ru'] }
    list_display = ('title_ru', 'priority')
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(Page, PageAdmin)



class LanguageAdmin(admin.ModelAdmin):
    list_display = ('small_name', 'priority')

admin.site.register(Language, LanguageAdmin)
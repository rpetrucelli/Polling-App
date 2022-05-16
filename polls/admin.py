from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    """
    I've chosen to show the choices view inside of the question view on the site, as this felt more logical
    due to the many-to-one relationship that choices have
    """
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):      #this method formats the question view of the admin page
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]                #here is where the choices get plugged in
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_per_page = 10

admin.site.register(Question, QuestionAdmin)    #here we register to the site the customizations made above

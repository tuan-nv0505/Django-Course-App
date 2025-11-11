from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'active']
    search_fields = ['subject']
    list_filter = ['id', 'subject', 'created_date']
    readonly_fields = ['image_view']

    def image_view(self, course):
        return mark_safe(f"<img src='/static/{course.image.name}' width='120' />")

    class Media:
        css = {
            'all': ('/static/css/styles.css', )
        }


admin.site.register(Category)
admin.site.register(Course, CourseAdmin)

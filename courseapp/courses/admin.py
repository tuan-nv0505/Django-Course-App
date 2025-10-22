from django.contrib import admin
from django.utils.safestring import mark_safe
from courses.models import Course, Category

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'category', 'created_date', 'activate']
    search_fields = ['subject']
    list_filter = ['id', 'created_date', 'activate']
    readonly_fields = ['image_view']
    
    def image_view(self, course):
        return mark_safe(f"<img src='/static/{course.image.name}' width='120' />")

    class Meta:
        css = {
            'all': ('/static/css/style.css', )
        }

admin.site.register(Course, CourseAdmin)
admin.site.register(Category)
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Student)
admin.site.register(AdminSetting)
admin.site.register(Section)
admin.site.register(Course)
admin.site.register(Selection)
admin.site.register(SpecialCourse)
admin.site.register(SelectionResult)
admin.site.register(CustomUser)
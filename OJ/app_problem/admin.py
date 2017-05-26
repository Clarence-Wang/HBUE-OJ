from django.contrib import admin
from app_problem.models import Problem, Submit
# Register your models here.

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'source', 'level', 'classify')

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Submit)


from django.contrib import admin
from .models import User, TestCase, Feature, TestResult, Report
# Register your models here.
admin.site.register(User)
admin.site.register(Feature)

admin.site.register(Report)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("created_by", "id")


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('testcase', 'result', 'tested_by')

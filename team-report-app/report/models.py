from django.db import models
from django.contrib.auth.models import AbstractUser
import re
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

def numbervalidator(val):
    if re.match('^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$', val):
        raise ValidationError("Enter a Valid Indian Phone Number")


class User(AbstractUser):
    mobile = models.CharField(max_length=13,validators=[numbervalidator])
    is_admin = models.BooleanField(default=False)


class Feature(models.Model):
    title = models.CharField(max_length=50)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class TestCase(models.Model):
    APP_CHOICES = [
        ("CUSTOMER_APP", "cx"),
        ("DELIVERYMAN_APP", "dm"),
        ("TEAM_CONSOLE", "tc"),
        ("API", "api")
    ]
    title = models.CharField(max_length=50)
    description = RichTextField()
    app = models.CharField(max_length=50, choices=APP_CHOICES)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.title} | {self.app}'


class Report(models.Model):
    title = models.CharField(max_length=90)
    features = models.ManyToManyField(Feature)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class TestResult(models.Model):
    RESULT_C = [
        ('untested', 'untested'),
        ('passed', 'passed'),
        ('failed', 'failed'),
    ]
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    comment = RichTextField()
    result = models.CharField(max_length=90, choices=RESULT_C, default='untested')
    tested_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.testcase)

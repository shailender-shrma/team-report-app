
from .models import Report, TestResult
from django import forms
from .models import TestCase
# from django.contrib.auth.forms import UserCreationForm

CHOICES = ((True, 'pass',), (False, 'fail',))


class UserCreationForm(forms.Form):
    mobile = forms.CharField(max_length=12, required=True)
    email = forms.EmailField(max_length=30, required=True)
    password = forms.CharField(max_length=10, required=True,
                               widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=10, required=True,
                                widget=forms.PasswordInput())
    username = forms.CharField(max_length=10, required=True)


class TestResultForm(forms.ModelForm):

    class Meta:
        model = TestResult
        fields = ['testcase', 'comment', 'result']


class TestReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('features', 'title', 'is_done')
        widgets = {
            'is_done': forms.Select(choices=CHOICES)
        }

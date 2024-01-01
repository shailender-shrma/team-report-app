from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, UpdateView, ListView, DetailView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms.models import model_to_dict
from .forms import UserCreationForm, TestResultForm, TestReportForm
from .models import User, TestCase, Feature, TestResult, Report
from django.db.models import Q


class UserRegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            registerform = UserCreationForm
            return render(request, "report/templates/register.html",
                          {'registerform': registerform})

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        if password1 == password2:
            User.objects.create_user(username, email,
                                     password=password1, mobile=mobile)
            return redirect('login')
        else:
            return render(request, 'report/templates/register.html')


class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'report/templates/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            user = login(request, user)
            return redirect('home')
        else:
            return render(request, 'report/templates/login.html')


class UserLogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


@method_decorator(login_required(login_url='login'), name='dispatch')
class TestCaseView(CreateView):
    model = TestCase
    fields = ['description',
              'title', 'app',
              'feature']
    template_name = "report/templates/add_testcase.html"

    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
            form.save()
            return super().form_valid(form)
        except Exception:
            return redirect('login')


@method_decorator(login_required(login_url='login'), name='dispatch')
class HomePageView(TemplateView):
    template_name = "report/templates/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        search_query = self.request.GET.get('search_query')

        search_date = self.request.GET.get('search_date')
        context["testcase"] = TestCase.objects.filter(created_by=user.id)\
            .order_by('-updated_at')
        if search_query:
            context['testcase'] = TestCase.objects.filter(
                title__icontains=search_query)
        elif search_date:
            search_date = datetime.combine(datetime.strptime(
                    search_date, "%Y-%m-%d"), datetime.min.time())
            start_date = search_date
            end_date = search_date + timedelta(days=1)
            context['testcase'] = TestCase.objects.filter(
                Q(created_at__lte=end_date) & Q(created_at__gte=start_date))

        context['test'] = TestResult.objects.filter(
            tested_by=user).order_by('-created_at')
        context['reqment'] = Feature.objects.select_related('created_by').all()
        context['report'] = Report.objects.filter(created_by=user,
                                                created_at__gte=timezone.now().replace(hour=0, minute=0, second=0),
                                                created_at__lte=timezone.now().replace(hour=23, minute=59, second=59))
        return context




@method_decorator(login_required(login_url='login'), name='dispatch')
class TaskUpdateView(UpdateView):
    model = TestCase
    fields = ['description']
    template_name = 'report/templates/update.html'
    success_url = '/'
    context_object_name = 'testcase'


# shows task which added in today


@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateFeatureView(CreateView):
    model = Feature
    fields = ['title', 'description']
    template_name = "report/templates/add_requirement.html"
    success_url = "/"

    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
            form.save()
            return super().form_valid(form)
        except Exception:
            return redirect('login')


@login_required
def featuredetails(request, pk):
    user = Feature.objects.get(id=pk)
    task = TestCase.objects.filter(feature_id=user)
    return render(request, 'report/templates/usertaskdetails.html',
                  {'task': task})


@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateTestResultView(CreateView):
    model = TestResult
    template_name = 'report/templates/addresult.html'
    form_class = TestResultForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.tested_by = self.request.user
        report = Report.objects.get(pk=self.kwargs['pk'])
        form.instance.report = report
        form.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ShowTestResultView(ListView):
    model = TestResult
    template_name = 'report/templates/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        test = TestCase.objects.get(pk=pk)
        test = TestResult.objects.filter(testcase=TestCase.objects.get(
            pk=self.kwargs["pk"])).order_by('-created_at')
        context['task'] = test

        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateReportView(CreateView):
    model = Report
    form_class = TestReportForm
    template_name = 'report/templates/report.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)




@method_decorator(login_required(login_url='login'), name='dispatch')
class ReportDetailView(DetailView):
    model = Report
    template_name = 'report/templates/reportdetails.html'
    context_object_name = 'results'

    def get_object(self):
        report = Report.objects.get(pk=self.kwargs['pk'])
        result = TestResult.objects.filter(report=report).order_by('-created_at')
        return result


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateReportView(UpdateView):
    model = Report
    fields = ['is_done']
    template_name = 'report/templates/updatereport.html'
    success_url = '/'
    context_object_name = 'report'


@method_decorator(login_required(login_url='login'), name='dispatch')
class ReportListView(ListView):
    model = Report
    template_name = "report/templates/allreports.html"
    context_object_name = 'report'
    paginate_by = 10
    ordering = '-created_at'

    def get_queryset(self):
        if self.request.GET.get('page_obj'):
            self.paginate_by = self.request.GET.get('page_obj')
        
        search_query = self.request.GET.get('search_query')

        search_date = self.request.GET.get('search_date')
        if search_query:
            d = datetime.now()
            report= Report.objects.filter(title__icontains=search_query)
            return report
            


        elif search_date:
            search_date = datetime.combine(datetime.strptime(
                    search_date, "%Y-%m-%d"), datetime.min.time())
            start_date = search_date
            end_date = search_date + timedelta(days=1)
            report = Report.objects.filter(
                Q(created_at__lte=end_date) & Q(created_at__gte=start_date))
        
            return report
        else:
            return Report.objects.all()


def custom_404(request, exception):
    return render(request, 'report/templates/custom_404.html', status=400)


def custom_500(request):
    return render(request, 'report/templates/custom_404.html', status=500)

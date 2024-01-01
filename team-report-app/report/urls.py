from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('signup/', views.UserRegisterView.as_view(), name="signup"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogOutView.as_view(), name='logout'),
    path('testcase/add/', views.TestCaseView.as_view(), name="addtestcase"),
    path('testcase/update/<int:pk>/', views.TaskUpdateView.as_view(), name="updatetestcases"),
    path('feature/add/', views.CreateFeatureView.as_view(), name="addrequirements"),
    path('feature/details/<int:pk>/', views.featuredetails, name="reqdetails"),
    path('testresult/<int:pk>/', views.ShowTestResultView.as_view(), name="showtestresult"),
    path('testresult/add/<int:pk>', views.CreateTestResultView.as_view(), name="createresult"),
    path('report/add/', views.CreateReportView.as_view(), name="createreport"),
    path('report/details/<int:pk>/', views.ReportDetailView.as_view(), name="reportdetails"),
    path('report/update/<int:pk>/', views.UpdateReportView.as_view(), name="updatereport"),
    path('report/all/', views.ReportListView.as_view(), name="allreport"),

]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('handleSignup/', views.SignupHandlerView.as_view(), name='handleSignup'),
    path('handlelogin/', views.LoginHandlerView.as_view(), name='handlelogin'),
    path('handleLogout/', views.LogoutHandlerView.as_view(), name='handleLogout'),

    # Password reset views (Django built-in)
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="home/reset_password.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="home/reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="home/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="home/password_reset_done.html"), name='password_reset_complete'),

    path('addmoney/', views.AddMoneyView.as_view(), name='addmoney'),
    path('addmoney_submission/', views.AddMoneySubmitView.as_view(), name='addmoney_submission'),

    path('charts/', views.ChartsView.as_view(), name='charts'),
    path('tables/', views.TablesView.as_view(), name='tables'),

    path('expense_edit/<int:pk>/', views.ExpenseEditView.as_view(), name='expense_edit'),
    path('<int:pk>/addmoney_update/', views.AddMoneyUpdateView.as_view(), name='addmoney_update'),
    path('expense_delete/<int:pk>/', views.ExpenseDeleteView.as_view(), name='expense_delete'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('<int:pk>/profile_edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('<int:pk>/profile_update/', views.ProfileUpdateView.as_view(), name='profile_update'),

    path('expense_month/', views.MonthlyExpenseView.as_view(), name='expense_month'),
    path('stats/', views.StatsView.as_view(), name='stats'),
    path('expense_week/', views.WeeklyExpenseView.as_view(), name='expense_week'),
    path('weekly/', views.WeeklySummaryView.as_view(), name='weekly'),

    path('check/', views.CheckView.as_view(), name='check'),
    path('search/', views.SearchView.as_view(), name='search'),

    path('info/', views.InfoView.as_view(), name='info'),
    path('info_year/', views.YearlyInfoView.as_view(), name='info_year'),
]

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as dj_login
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Addmoney_info, UserProfile
from .forms import ProfileForm
import datetime
from django.db.models import Sum


class HomeView(View):
    def get(self, request):
        if request.session.get('is_logged'):
            return redirect('dashboard')
        return render(request, 'home/login.html')


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id=request.session["user_id"])
        addmoney_info = Addmoney_info.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney_info, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/dashboard.html', {'page_obj': page_obj})


class RegisterView(View):
    def get(self, request):
        return render(request, 'home/register.html')


class SignupHandlerView(View):
    def post(self, request):
        uname = request.POST["uname"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        profession = request.POST['profession']
        Savings = request.POST['Savings']
        income = request.POST['income']
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        # Validate
        try:
            User.objects.get(username=uname)
            messages.error(request, "Username already taken, try something else!")
            return redirect("register")
        except User.DoesNotExist:
            if len(uname) > 15:
                messages.error(request, "Username must be max 15 characters, please try again")
                return redirect("register")
            if not uname.isalnum():
                messages.error(request, "Username should only contain letters and numbers, please try again")
                return redirect("register")
            if pass1 != pass2:
                messages.error(request, "Passwords do not match, please try again")
                return redirect("register")

        user = User.objects.create_user(uname, email, pass1)
        user.first_name = fname
        user.last_name = lname
        user.save()

        profile = UserProfile(user=user, Savings=Savings, profession=profession, income=income)
        profile.save()

        messages.success(request, "Your account has been successfully created")
        return redirect("home")


class LoginHandlerView(View):
    def post(self, request):
        loginuname = request.POST["loginuname"]
        loginpassword1 = request.POST["loginpassword1"]
        user = authenticate(username=loginuname, password=loginpassword1)
        if user is not None:
            dj_login(request, user)
            request.session['is_logged'] = True
            request.session["user_id"] = user.id
            messages.success(request, "Successfully logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials, please try again")
            return redirect('home')


class LogoutHandlerView(View):
    def get(self, request):
        request.session.flush()
        logout(request)
        messages.success(request, "Successfully logged out")
        return redirect('home')


class AddMoneyView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home/addmoney.html')


class AddMoneySubmitView(LoginRequiredMixin, View):
    def post(self, request):
        user = get_object_or_404(User, id=request.session["user_id"])
        add_money = request.POST["add_money"]
        quantity = request.POST["quantity"]
        Date = request.POST["Date"]
        Category = request.POST["Category"]

        Addmoney_info.objects.create(user=user, add_money=add_money, quantity=quantity, Date=Date, Category=Category)

        addmoney_info = Addmoney_info.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney_info, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/dashboard.html', {'page_obj': page_obj})


class AddMoneyUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        add = get_object_or_404(Addmoney_info, id=pk)
        add.add_money = request.POST["add_money"]
        add.quantity = request.POST["quantity"]
        add.Date = request.POST["Date"]
        add.Category = request.POST["Category"]
        add.save()
        return redirect('dashboard')


class ExpenseEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        addmoney_info = get_object_or_404(Addmoney_info, id=pk)
        return render(request, 'home/expense_edit.html', {'addmoney_info': addmoney_info})


class ExpenseDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        addmoney_info = get_object_or_404(Addmoney_info, id=pk)
        addmoney_info.delete()
        return redirect('dashboard')


class ChartsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home/charts.html')


class TablesView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id=request.session["user_id"])
        addmoney = Addmoney_info.objects.filter(user=user).order_by('-Date')
        return render(request, 'home/tables.html', {'addmoney': addmoney})

    def post(self, request):
        # If you want to handle POST separately, keep it here,
        # or just call get() if you want same behavior:
        return self.get(request)


class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id=request.session["user_id"])
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        addmoney = Addmoney_info.objects.filter(user=user, Date__range=[fromdate, todate]).order_by('-Date')
        return render(request, 'home/tables.html', {'addmoney': addmoney})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home/profile.html')



class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        profile = get_object_or_404(UserProfile, user_id=pk)
        form = ProfileForm(instance=profile)
        return render(request, 'home/profile_edit.html', {'form': form})

    def post(self, request, pk):
        profile = get_object_or_404(UserProfile, user_id=pk)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or any success URL
        return render(request, 'home/profile_edit.html', {'form': form})



class ProfileUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        user.first_name = request.POST["fname"]
        user.last_name = request.POST["lname"]
        user.email = request.POST["email"]
        user.userprofile.Savings = request.POST["Savings"]
        user.userprofile.income = request.POST["income"]
        user.userprofile.profession = request.POST["profession"]
        user.userprofile.save()
        user.save()
        return redirect('profile')


# Utility function for expense category sums
def get_expense_category_data(user, days=None):
    today = datetime.date.today()
    if days:
        start_date = today - datetime.timedelta(days=days)
        queryset = Addmoney_info.objects.filter(user=user, Date__gte=start_date, Date__lte=today)
    else:
        queryset = Addmoney_info.objects.filter(user=user)

    categories = set(queryset.values_list('Category', flat=True))
    data = {}

    for category in categories:
        total = queryset.filter(Category=category, add_money="Expense").aggregate(Sum('quantity'))['quantity__sum'] or 0
        data[category] = total

    return data


class MonthlyExpenseView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id=request.session["user_id"])
        data = get_expense_category_data(user, days=30)
        return JsonResponse({'expense_category_data': data}, safe=False)


class WeeklyExpenseView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id=request.session["user_id"])
        data = get_expense_category_data(user, days=7)
        return JsonResponse({'expense_category_data': data}, safe=False)


class YearlyInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id=request.session["user_id"])
        data = get_expense_category_data(user, days=365)
        return JsonResponse({'expense_category_data': data}, safe=False)


class StatsView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id=request.session["user_id"])
        today = datetime.date.today()
        one_month_ago = today - datetime.timedelta(days=30)
        addmoney_info = Addmoney_info.objects.filter(user=user, Date__gte=one_month_ago, Date__lte=today)

        total_expense = addmoney_info.filter(add_money='Expense').aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_income = addmoney_info.filter(add_money='Income').aggregate(Sum('quantity'))['quantity__sum'] or 0

        savings = user.userprofile.Savings
        balance = savings + total_income - total_expense

        warning = None
        if balance < 0:
            warning = 'Your expenses exceeded your savings'
            balance = 0

        context = {
            'addmoney': addmoney_info,
            'total_expense': total_expense,
            'total_income': total_income,
            'balance': balance,
            'warning': warning,
        }
        return render(request, 'home/stats.html', context)


class WeeklySummaryView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id=request.session["user_id"])
        today = datetime.date.today()
        one_week_ago = today - datetime.timedelta(days=7)
        addmoney_info = Addmoney_info.objects.filter(user=user, Date__gte=one_week_ago, Date__lte=today)

        total_expense = addmoney_info.filter(add_money='Expense').aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_income = addmoney_info.filter(add_money='Income').aggregate(Sum('quantity'))['quantity__sum'] or 0

        savings = user.userprofile.Savings
        balance = savings + total_income - total_expense

        warning = None
        if balance < 0:
            warning = 'Your expenses exceeded your savings'
            balance = 0

        context = {
            'addmoney_info': addmoney_info,
            'total_expense': total_expense,
            'total_income': total_income,
            'balance': balance,
            'warning': warning,
        }
        return render(request, 'home/weekly.html', context)


class InfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home/info.html')


class CheckView(View):
    def post(self, request):
        email = request.POST.get('email')
        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            messages.error(request, "Email not registered, TRY AGAIN!!!")
        return redirect("reset_password")

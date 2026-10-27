from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import ExpenseForm
from .models import Expense

def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to SpendWise! Your account is ready.")
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    today = timezone.localdate()
    month_expenses = expenses.filter(date__year=today.year, date__month=today.month)
    month_total = month_expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    all_total = expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    category_totals = list(
        month_expenses.values("category").annotate(total=Sum("amount")).order_by("-total")
    )
    recent_expenses = expenses[:8]
    return render(request, "expenses/dashboard.html", {
        "month_total": month_total,
        "all_total": all_total,
        "month_count": month_expenses.count(),
        "recent_expenses": recent_expenses,
        "category_totals": category_totals,
        "month_name": today.strftime("%B %Y"),
    })

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    category = request.GET.get("category", "")
    if category:
        expenses = expenses.filter(category=category)
    return render(request, "expenses/expense_list.html", {
        "expenses": expenses,
        "categories": Expense.CATEGORY_CHOICES,
        "selected_category": category,
    })

@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully.")
            return redirect("expense_list")
    else:
        form = ExpenseForm(initial={"date": timezone.localdate()})
    return render(request, "expenses/expense_form.html", {"form": form, "page_title": "Add an expense"})

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated.")
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "expenses/expense_form.html", {"form": form, "page_title": "Edit expense"})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted.")
        return redirect("expense_list")
    return render(request, "expenses/expense_confirm_delete.html", {"expense": expense})

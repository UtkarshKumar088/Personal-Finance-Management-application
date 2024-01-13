from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Expense
from .forms import ExpenseForm
from django.contrib import messages

def create_admin_user():
    # Check if the admin user already exists
    if not User.objects.filter(username='admin_username').exists():
        # Create the admin user only if it doesn't exist
        admin_user = User.objects.create_user(username='admin_username', password='admin_password', is_staff=True)
        print('Admin user created successfully')
    else:
        print('Admin user already exists')

def create_member_user():
    # Check if the member user already exists
    if not User.objects.filter(username='member_username').exists():
        # Create the member user only if it doesn't exist
        member_user = User.objects.create_user(username='member_username', password='member_password')
        print('Member user created successfully')
    else:
        print('Member user already exists')

# Uncomment the lines below to create Admin and Member users when needed
create_admin_user()
create_member_user()

@login_required
def view_expense(request):
    if request.user.is_staff:
        # Admin can view all members' expenses
        expenses = Expense.objects.all()
    else:
        # Member can only view their own expenses
        expenses = Expense.objects.filter(user=request.user)

    # Filtering by date
    date_filter = request.GET.get('date_filter')
    if date_filter:
        expenses = expenses.filter(date=date_filter)

    # Searching by expense name
    search_query = request.GET.get('search_query')
    if search_query:
        expenses = expenses.filter(name__icontains=search_query)

    context = {'expenses': expenses}
    return render(request, 'base/view_expense.html', context)

@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.created_by = request.user
            expense.save()
            messages.success(request, 'Expense created successfully!')
            return redirect('create_expense')
        else:
            messages.error(request, 'Expense creation failed. Please check the form for errors.')
    else:
        form = ExpenseForm()

    return render(request, 'base/create_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    # Ensure only the creator of the expense can edit it
    if expense.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this expense.')
        return redirect('view_expense')

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('view_expense')
        else:
            messages.error(request, 'Expense update failed. Please check the form for errors.')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'base/edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('view_expense')

    return render(request, 'base/delete_expense.html', {'expense': expense})

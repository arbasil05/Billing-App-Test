from django.shortcuts import render, redirect
from .models import *
from datetime import date
from django.db.models import Sum

def home(request):
    return render(request, 'home.html')

def billing(request):
    if request.method == 'GET':
        product_name = request.GET.get('product_name')
        product_price = request.GET.get('product_price')
        product_discount = request.GET.get('product_discount')

        if product_name and product_price and product_discount:
            try:
                product_price = float(product_price) if product_price else 0
                product_discount = float(product_discount) if product_discount else 0
            except ValueError:
                product_price = 0
                product_discount = 0

            total = product_price - product_discount  # Calculate the total

            # Check if the product already exists in the cart
            existing_item = cart_data.objects.filter(cart_product_name=product_name).first()
            if not existing_item:
                cart_item = cart_data(
                    cart_product_name=product_name,
                    cart_product_price=product_price,
                    cart_product_discount=product_discount,
                    cart_product_total=total  # Save the calculated total
                )
                cart_item.save()

        # Retrieve all cart items to display in the template
        cart_items = cart_data.objects.all()
        # Calculate the total amount of the cart
        cart_total = sum(item.cart_product_total for item in cart_items)
        
        today_sales = Sales.objects.filter(sale_date=date.today())
        expense_items = Expense.objects.all()

        # Calculate total expenses
        expense_total = sum(expense.expense_amount for expense in expense_items)

        # Calculate total sales
        sales_total = sum(sale.sale_product_total for sale in today_sales)

        # Calculate the total register amount before UPI deduction
        total_register = sales_total - expense_total

        # Calculate the total amount of UPI sales
        upi_sales = Sales.objects.filter(sale_upi=True)
        upi_total = sum(sale.sale_product_total for sale in upi_sales)

        # Calculate the total register amount after UPI deduction
        total_register_after_upi = total_register - upi_total

        # Ensure total_register_after_upi is not negative
        total_register_after_upi = max(total_register_after_upi, 0)

        context = {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'today_sales': today_sales,
            'sales_total': sales_total,
            'expense_items': expense_items,
            'expense_total': expense_total,
            'total_register': int(total_register),
            'total_register_after_upi': int(total_register_after_upi),
            'upi_total': upi_total
        }

        return render(request, 'billing.html', context)
    return render(request, 'billing.html')


def add_to_sales(request):
    if request.method == 'POST':
        cart_items = cart_data.objects.all()
        upi = request.POST.get("upi")
        upi = True if upi else False
        for item in cart_items:
            Sales.objects.create(
                sale_product_name=item.cart_product_name,
                sale_product_price=item.cart_product_price,
                sale_product_discount=item.cart_product_discount,
                sale_product_total=item.cart_product_total,
                sale_upi = upi,
                sale_date=date.today()
            )
        

        for item in cart_items:
            Sales_Backup.objects.create(
                sale_product_name=item.cart_product_name,
                sale_product_price=item.cart_product_price,
                sale_product_discount=item.cart_product_discount,
                sale_product_total=item.cart_product_total,
                sale_upi = upi,
                sale_date=date.today()
            )
        cart_data.objects.all().delete()

        return redirect('billing')
    return redirect('billing')

def add_to_expense(request):
    if request.method == 'GET':
        expense_name = request.GET.get('expense_name')
        expense_amount = request.GET.get('expense_amount')

        if expense_name and expense_amount:
            try:
                expense_amount = float(expense_amount) if expense_amount else 0
            except ValueError:
                expense_amount = 0
        
            existing_item = Expense.objects.filter(expense_name=expense_name).first()
            if not existing_item:
                Expense.objects.create(
                    expense_name=expense_name,
                    expense_amount=expense_amount
                )
                Expense_Backup.objects.create(
                    expense_name=expense_name,
                    expense_amount=expense_amount
                )

        return redirect('billing')



def remove_expense(request, expense_id):
    expense = Expense.objects.filter(id=expense_id).first()
    if expense:
        expense.delete()
    return redirect('billing')

def remove_item(request, item_id):
    cart_item = cart_data.objects.filter(id=item_id).first()
    if cart_item:
        cart_item.delete()
    return redirect('billing')

def remove_sales(request, sale_id):
    sale = Sales.objects.filter(id=sale_id).first()
    
    if sale:
        # Find the corresponding Sales_Backup record
        sales_backup = Sales_Backup.objects.filter(
            sale_product_name=sale.sale_product_name,
            sale_product_price=sale.sale_product_price,
            sale_product_discount=sale.sale_product_discount,
            sale_product_total=sale.sale_product_total,
            sale_upi=sale.sale_upi,
            sale_date=sale.sale_date
        ).first()
        
        if sales_backup:
            sales_backup.delete()
        
        sale.delete()
    
    return redirect('billing')

def close_sales(request):
    today_sales = Sales.objects.filter(sale_date = date.today())
    expense_items = Expense.objects.all()
    upi_select = Sales.objects.filter(sale_upi=True)
    upi_total = 0

    for i in upi_select:
        upi_total += i.sale_product_total

    expense_total = sum(expense.expense_amount for expense in expense_items)
    sales_total = sum(sale.sale_product_total for sale in today_sales)
    total_register = sales_total - expense_total
    existing_entry = sales_by_date.objects.filter(date=date.today()).first()
    
    if existing_entry:
            # Update the existing entry
            existing_entry.sales_amount = sales_total
            existing_entry.expense_amount = expense_total
            existing_entry.upi_amount = upi_total
            existing_entry.register_amount = total_register
            existing_entry.save()
    else:
        
        sales_entry = sales_by_date(
            sales_amount=sales_total,
            expense_amount=expense_total,
            register_amount=total_register,
            upi_amount = upi_total,
            date= date.today()
        )
        sales_entry.save()

    Sales.objects.all().delete()
    Expense.objects.all().delete()

    return redirect('billing')



def history(request):
    date_input = request.GET.get('date')
    saless_total = 0
    expenses_amount = 0
    registers_amount = 0
    upi_total = 0

    if date_input:
        try:
            # Filter the sales_by_date object for the given date
            sales_by_dates = sales_by_date.objects.filter(date=date_input).first()

            if sales_by_dates:
                saless_total = sales_by_dates.sales_amount
                expenses_amount = sales_by_dates.expense_amount
                upi_total = sales_by_dates.upi_amount

                # Calculate the registers_amount by deducting the UPI amount
                registers_amount = sales_by_dates.register_amount - upi_total
        except ValueError:
            pass

    # Fetch the sales and expense reports for the given date
    sales_report = Sales_Backup.objects.filter(sale_date=date_input)
    expense_report = Expense_Backup.objects.filter(expense_date=date_input)

    # Prepare context for rendering the template
    context = {
        'date_input': date_input,  # Added for displaying in the template
        'saless_total': saless_total,
        'expenses_total': expenses_amount,
        'sale_report': sales_report,
        'expense_items': expense_report,
        'upis_total': upi_total,
        'registers_total': registers_amount
    }
    return render(request, 'history.html', context)


def debt(request):
    return render(request, 'debt.html')

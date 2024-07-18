from django.db import models
from django.utils import timezone

class cart_data(models.Model):
    cart_product_name = models.CharField(max_length=100)
    cart_product_price = models.FloatField(max_length=100)
    cart_product_discount = models.FloatField(max_length=100)
    cart_product_total = models.FloatField(max_length=100,default=0)

    def __str__ (self):
        return self.cart_product_name
    

class Sales(models.Model):
    sale_product_name = models.CharField(max_length=100)
    sale_product_price = models.FloatField()
    sale_product_discount = models.FloatField()
    sale_product_total = models.FloatField()
    sale_date = models.DateField(auto_now_add=True) 
    sale_upi = models.BooleanField(default=False)

    def __str__(self):        
        return self.sale_product_name
    
class Sales_Backup(models.Model):
    sale_product_name = models.CharField(max_length=100)
    sale_product_price = models.FloatField()
    sale_product_discount = models.FloatField()
    sale_product_total = models.FloatField()
    sale_date = models.DateField(auto_now_add=True) 
    sale_upi = models.BooleanField(default=False)

    def __str__(self):        
        return self.sale_product_name

class Expense(models.Model):
    expense_name = models.CharField(max_length=100)
    expense_amount = models.IntegerField()
    expense_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.expense_name
    
class Expense_Backup(models.Model):
    expense_name = models.CharField(max_length=100)
    expense_amount = models.IntegerField()
    expense_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.expense_name

class sales_by_date(models.Model):
    sales_amount = models.IntegerField()
    expense_amount = models.IntegerField()
    upi_amount = models.IntegerField(default=0)
    register_amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date)

    

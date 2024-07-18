from django.urls import path
from billing import views

urlpatterns = [
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('billing/',views.billing,name='billing'),
    path('history/',views.history,name='history'),
    path('debt/',views.debt,name='debt'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('remove_sales/<int:sale_id>/', views.remove_sales, name='remove_sales'), 
    path('remove_expense/<int:expense_id>/', views.remove_expense, name='remove_expense'),
    path('add_to_sales/',views.add_to_sales,name='add_to_sales'),
    path('add_to_expense/',views.add_to_expense,name='add_to_expense'),
    path('close_sales/',views.close_sales,name='close_sales')
    

]
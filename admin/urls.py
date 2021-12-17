from django.urls import path
from .views import (
    dashboard_view,
    login_view,
    logout_view,
    products_list_view,
    product_create_view,
    product_edit_view,
    customer_create_view,
    customer_detail_view,
    customers_list_view,
    delete_resource_view,
    order_create_view,
    order_detail_view,
    orders_list_view,
    # project_create_view,
    # project_edit_view,
    # projects_list_view,
    solution_edit_view,
    solution_create_view,
    solutions_list_view,
)

app_name = 'wasi_admin'

urlpatterns = [
    path('', dashboard_view, name="dashboard"),
    path('login/', login_view, name="login-page"),
    path('logout/', logout_view, name="logout"),
    path('delete/<resource>/<arg>/', delete_resource_view, name="delete"),

    path('customers/', customers_list_view, name="customers-list"),
    path('customers/add/', customer_create_view, name="add-customer"),
    path('customers/<pk>/change/', customer_detail_view, name="edit-customer"),
    
    path('orders/', orders_list_view, name="orders-list"),
    path('orders/add/', order_create_view, name="add-order"),
    path('orders/<invoice>/', order_detail_view, name="order-detail"),
    
    path('products/', products_list_view, name="products-list"),
    path('products/add/', product_create_view, name="add-product"),
    path('products/<product_id>/change/', product_edit_view, name="edit-product"),
    
    # path('projects/', projects_list_view, name="projects"),
    # path('projects/add/', project_create_view, name="add-project"),
    # path('projects/<pk>/change/', project_edit_view, name="edit-project"),
    
    path('solutions/', solutions_list_view, name="solutions"),
    path('solutions/add/', solution_create_view, name="add-solution"),
    path('solutions/<pk>/change/', solution_edit_view, name="edit-solution"),
]

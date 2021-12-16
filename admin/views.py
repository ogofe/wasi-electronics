from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required
)
from store.models import (
    Product,
    ProductImage,
    Customer,
    CheckoutOrder,
    DeliveryLog,
    OrderItem,
    get_categories,
    generate_invoice,
    generate_product_id
)
from core.models import (
    Project,
    ProjectFile,
    Solution,
    FileObject
)


def logout_view(request):
    logout(request)
    return redirect('wasi_admin:login-page')


def login_view(request):
    if request.method == "POST":
        data = request.POST
        try:
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                print(f"loging {user.username} in")
                login(request, user)
                messages.info(request, "Welcome back %s" % user.username)
                print("successfuly logged in")
                return redirect('wasi_admin:dashboard')
            print("login error")
            messages.error(request, "Invalid username / password")
            return redirect('wasi_admin:login-page')
        except:
            return redirect('wasi_admin:login-page')
    return render(request, 'admin/auth/login.html', {})


@login_required(login_url='wasi_admin:login-page')
def delete_resource_view(request, resource, arg):
    resources = {
        'product': {
            'model': Product,
        },
        'project': {
            'model': Project,
        },
        'solution': {
            'model': Solution,
        },
        'customer': {
            'model': Customer,
        },
        'order': {
            'model': CheckoutOrder,
        },
    }
    model = resources[resource]['model']
    object_ = model.objects.get(pk=arg)
    object_.delete()
    messages.success(request, f"Successfully deleted {resource.capitalize()}")
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='wasi_admin:login-page')
def dashboard_view(request):
    return render(request, 'admin/pages/dashboard.html', {})


@login_required(login_url='wasi_admin:login-page')
def products_list_view(request):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'admin/pages/products/list.html', context)


@login_required(login_url='wasi_admin:login-page')
def product_create_view(request):
    if request.method == "POST":
        data = request.POST
        new_product = Product(
            name=data['name'],
            price=data['price'],
            quantity=data['quantity'],
            category=data['category'],
            description=data['description'],
        )
        new_product.save()
        uploads = request.FILES
        for img in uploads:
            image = ProductImage(product=new_product, image=img)
            image.save()
            new_product.images.add(image)
        new_product.save()
        messages.success(request, "Successfully added a new product")

        return redirect('wasi_admin:products-list')
    context = {
        'categories': get_categories()
    }
    return render(request, 'admin/pages/products/add.html', context)


@login_required(login_url='wasi_admin:login-page')
def product_edit_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    if request.method == "POST":
        data, files = request.POST, request.FILES
        product.name=data['name']
        product.price=data['price']
        product.category=data['category']
        product.quantity=data['quantity']
        product.description=data['description']
        product.save()
        if files.getlist('image'):
            product.override_images(files.getlist('image'))
        messages.success(request, "Successfully changed %s" % product.name)
        return redirect('wasi_admin:products-list')
    context = {
        'categories': get_categories(),
        'product': product,
    }
    return render(request, 'admin/pages/products/edit.html', context)


@login_required(login_url='wasi_admin:login-page')
def customers_list_view(request):
    context = {
        'customers': Customer.objects.all(),
    }
    return render(request, 'admin/pages/customers/list.html', context)


@login_required(login_url='wasi_admin:login-page')
def customer_create_view(request):
    if request.method == "POST":
        data = request.POST
        new_customer = Customer(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            address=data.get('address', "No address specified"),
        )
        new_customer.save()
        messages.success(request, "Successfully added new customer")
        return redirect('wasi_admin:customers-list')
    return render(request, 'admin/pages/customers/add.html', {})
    

@login_required(login_url='wasi_admin:login-page')
def customer_detail_view(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        data = request.POST
        customer.first_name=data['first_name']
        customer.last_name=data['last_name']
        customer.email=data['email']
        customer.phone_number=data['phone_number']
        customer.address=data['address']
        customer.save()
        messages.success(request, "Successfully changed customer info")
        return redirect('wasi_admin:customers-list')
    context = {
        'person': customer,
    }
    return render(request, 'admin/pages/customers/edit.html', context)


@login_required(login_url='wasi_admin:login-page')
def orders_list_view(request):
    tab = request.GET.get('tab', None)
    orders = CheckoutOrder.objects.all()
    if tab:
        orders = orders.filter(status=tab)
    context = {
        'orders': orders,
    }
    return render(request, 'admin/pages/orders/list.html', context)


@login_required(login_url='wasi_admin:login-page')
def order_create_view(request):
    if request.method == "POST":
        order_items = []
        boolean = {'on': True, 'off': False}
        data = request.POST
        new_order = CheckoutOrder(
            owner=Customer.objects.get(id=data['customer']),
            delivery_on=boolean[data['delivery']]
        )
        new_order.save()
        for item in data.getlist('item'):
            order_item = OrderItem.objects.create(
                item=Product.objects.get(id=item.split(':')[0]),
                quantity=item.split(':')[1]
            )
            new_order.items.add(order_item)
        new_order.save()
        messages.success(request, "Successfully added new order")
        return redirect('wasi_admin:orders-list')
    context = {
        'customers': Customer.objects.all(),
        'products': list({'item': product.name, 'id': product.id} for product in Product.objects.all()),
    }
    return render(request, 'admin/pages/orders/add.html', context)


@login_required(login_url='wasi_admin:login-page')
def order_detail_view(request, invoice):
    order = CheckoutOrder.objects.get(invoice=invoice)
    if request.method == "POST":
        data = request.POST
        order.status = data['status']
        order.save()
        messages.success(request, "Successfully changed order %s" % order.invoice)
        return redirect(request.META['HTTP_REFERER'])
    context = {
        'order': order,
    }
    return render(request, 'admin/pages/orders/detail.html', context)


@login_required(login_url='wasi_admin:login-page')
def projects_list_view(request):
    context = {
        'projects': Project.objects.all(),
    }
    return render(request, 'admin/pages/projects/list.html', context)


@login_required(login_url='wasi_admin:login-page')
def project_create_view(request):
    if request.method == "POST":
        data, uploads = request.POST, request.FILES
        new_project = Project(
            title = data['title'],
            description = data['description'],
            complete = data['completed']
        )
        new_project.save()
        if uploads.getlist('upload'):
            for file in uploads.getlist('upload'):
                if file.split('.')[-1] == '.jpg' or file.split('.')[-1] == '.png' or file.split('.')[-1] == '.jpeg':
                    pass
                elif file.split('.')[-1] == '.mp4' or file.split('.')[-1] == '.mpeg':
                    pass
                pass
            new_project.save()
        messages.success(request, "Successfully added new project")
        return redirect('wasi_admin:projects')
    return render(request, 'admin/pagesprojects/add.html', {})


@login_required(login_url='wasi_admin:login-page')
def project_edit_view(request, pk):
    project = Projects.objects.get(id=pk)
    if request.method == "POST":
        data, uploads = request.POST, request.FILES
        project.title=data['title']
        project.description=data['description']
        project.completed=data['completed']
        project.save()
        if uploads.getlist('upload'):
            for file in uploads.getlist('upload'):
                if file.split('.')[-1] == '.jpg' or file.split('.')[-1] == '.png' or file.split('.')[-1] == '.jpeg':
                    pass
                elif file.split('.')[-1] == '.mp4' or file.split('.')[-1] == '.mpeg':
                    pass
                pass
            new_project.save()
        messages.success(request, "Successfully changed project %s " % project.title)
        return redirect('wasi_admin:home')
    context = {
        'project': Project.objects.all(),
    }
    return render(request, 'admin/pages/projects/edit.html', context)


@login_required(login_url='wasi_admin:login-page')
def solutions_list_view(request):
    context = {
        'solutions': Solution.objects.all(),
    }
    return render(request, 'admin/pages/solutions/list.html', context)


@login_required(login_url='wasi_admin:login-page')
def solution_create_view(request):
    if request.method == "POST":
        data, uploads = request.POST, request.FILES
        files = uploads.getlist('file', None)
        new_solution = Solution(
            name=data['name'],
            description=data['about']
        )
        new_solution.save()
        if files:
            for file in files:
                upload = FileObject(file=file)
                upload.save()
                new_solution.files.add(upload)
        new_solution.save()
        messages.success(request, "Successfully added new solution %s" % new_solution.name)
        return redirect('wasi_admin:solutions')
    return render(request, 'admin/pages/solutions/add.html', {})


@login_required(login_url='wasi_admin:login-page')
def solution_edit_view(request, pk):
    solution = Solution.objects.get(id=pk)
    if request.method == "POST":
        data, uploads = request.POST, request.FILES
        solution.name=data['name']
        solution.about_solution=data['about_solution']
        files = uploads.getlist('file', None)
        if files:
            for file in files:
                upload = FileObject(file=file)
                upload.save()
                solution.files.add(upload)
            solution.save()
        messages.success(request, "Successfully changed solution %s" % solution.name)
        return redirect('wasi_admin:home')
    context = {
        'solutions': solution,
    }
    return render(request, 'admin/pages/solutions/edit.html', context)

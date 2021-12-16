from django.shortcuts import render, redirect



def homepage_view(request):
    context = {
        'page_title': "Shop",
    }
    return render(request, 'store/homepage.html', context)



def cart_view(request):
    # cart is already provided in template
    context = {
        'page_title': "Your Cart",
    }
    return render(request, 'store/product-page.html', context)



def product_view(request, product_id):
    product = None
    context = {
        'product': product,
        'page_title': "",
    }
    return render(request, 'store/product-page.html', context)



def checkout_view(request):
    context = {
        'product': product,
        'page_title': "",
    }
    if request.method == "POST":
        return redirect('store:checkout_success')
    return render(request, 'store/product-page.html', context)
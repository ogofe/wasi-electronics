from store.models import (
    Product,
)
from core.models import (
    Solution,

)


def cart_context(request):
    context = {
        
    }
    return context


def global_context(request):
    context = {
        'all_products': Product.objects.all(),
        'all_solutions': Solution.objects.all(),
    }
    return context
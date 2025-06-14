from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# 🔁 Shared dummy product list
# 🔄 Product Data with Categories
PRODUCTS = [
    {   
        'id':1,
        'name': 'Smart Watch',
        'price': 499,
        'image': 'https://example.com/smartwatch.jpg',
        'category': 'Electronics'
    },
    {
        'id':2,
        'name': 'Formal Shoes',
        'price': 899,
        'image': 'https://example.com/formalshoes.jpg',
        'category': 'Shoes - Formal'
    },
    {
        'id':3,
        'name': 'Casual Shoes',
        'price': 799,
        'image': 'https://example.com/casualshoes.jpg',
        'category': 'Shoes - Casual'
    },
    {
        'id':4,
        'name': 'Men’s Dress',
        'price': 1199,
        'image': 'https://example.com/mensdress.jpg',
        'category': 'Dress - Men'
    },
    {
        'id':5,
        'name': 'Women’s Dress',
        'price': 1299,
        'image': 'https://example.com/womensdress.jpg',
        'category': 'Dress - Women'
    },
    {
        'id':6,
        'name': 'Sofa Set',
        'price': 4999,
        'image': 'https://example.com/sofa.jpg',
        'category': 'Furniture'
    },
    {
        'id':7,
        'name': 'Mixer Grinder',
        'price': 1999,
        'image': 'https://example.com/mixer.jpg',
        'category': 'Household Items'
    }
]
   


# 🔐 Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Temporary logic — no real authentication yet
        if username and password:
            return redirect('ecommerce')  # Name used in urls.py
        else:
            error = "Please enter both username and password."
            return render(request, 'login/login.html', {'error': error})

    return render(request, 'login/login.html')

# 🛒 Ecommerce homepage
def ecommerce_view(request):
    all_products = [
        # your full product list with 'name', 'price', 'category', 'image', 'id'
    ]

    # Get query parameters
    selected_category = request.GET.get('category', 'all').lower()
    search_query = request.GET.get('query', '').lower()

    # Start with all products
    products = all_products

    # 🔍 Filter by category
    if selected_category != 'all':
        products = [p for p in products if p['category'].lower() == selected_category]

    # 🔍 Filter by search query (if any)
    if search_query:
        products = [p for p in products if search_query in p['name'].lower()]

    return render(request, 'login/ecommerce.html', {
        'products': products,
        'selected_category': selected_category,
        'search_query': search_query,
    })


# 🧾 Product detail page
def product_detail_view(request, product_id):
    for product in PRODUCTS:
        if product['id'] == product_id:
            return render(request, 'login/product_detail.html', {'product': product})
    return HttpResponse("Product not found", status=404)

# 🚪 Logout view
def logout_view(request):
    logout(request)
    return redirect('login')


# ➕ Add to Cart view
@csrf_exempt
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])

        for product in PRODUCTS:
            if product['id'] == product_id:
                cart.append(product)
                break

        request.session['cart'] = cart
        return redirect('ecommerce')
    else:
        return HttpResponse("Invalid request method", status=405)

# 🛍️ View Cart
def cart_view(request):
    cart = request.session.get('cart', [])
    return render(request, 'login/cart.html', {'cart': cart})

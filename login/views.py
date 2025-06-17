from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Static Product Data
PRODUCTS = [
    {
        'id': 1,
        'name': 'Smart Watch',
        'price': 499,
        'image': 'images/smart watch.jpeg',
        'category': 'Electronics',
        'description': 'Stay connected and track your health with this stylish and affordable smartwatch.'
    },
    {
        'id': 2,
        'name': 'Formal Shoes',
        'price': 899,
        'image': 'images/formalshoes.jpg',
        'category': 'Shoes - Formal',
        'description': 'Elegant and comfortable formal shoes perfect for office wear and events.'
    },
    {
        'id': 3,
        'name': 'Casual Shoes',
        'price': 799,
        'image': 'images/casualshoemen.jpg',
        'category': 'Shoes - Casual',
        'description': 'Trendy and durable casual shoes for everyday comfort and style.'
    },
    {
        'id': 4,
        'name': 'Men’s Dress',
        'price': 1199,
        'image': 'images/mendress cas shirt.jpg',
        'category': 'Dress - Men',
        'description': 'Stylish men’s dress that combines traditional elegance with modern design.'
    },
    {
        'id': 5,
        'name': 'Women’s Dress',
        'price': 1299,
        'image': 'images/womdresscastop.jpg',
        'category': 'Dress - Women',
        'description': 'Graceful and fashionable women’s dress for any special occasion or party.'
    },
    {
        'id': 6,
        'name': 'Sofa Set',
        'price': 4999,
        'image': 'images/sofaset.jpg',
        'category': 'Furniture',
        'description': 'Luxurious and spacious sofa set that adds comfort and style to your living room.'
    },
    {
        'id': 7,
        'name': 'Mixer Grinder',
        'price': 1999,
        'image': 'images/mixergrinder.jpg',
        'category': 'Household Items',
        'description': 'Powerful mixer grinder with multiple jars for all your kitchen needs.'
    }
]


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            request.session['user'] = username
            return redirect('ecommerce')
        return render(request, 'login/login.html', {'error': 'Please enter both username and password.'})

    return render(request, 'login/login.html')

# ---------------- HOME ----------------
def ecommerce_view(request):
    selected_category = request.GET.get('category', 'all')
    search_query = request.GET.get('query', '').strip().lower()

    # Get all unique categories
    categories = sorted(set(p['category'] for p in PRODUCTS))

    # Filter by category
    if selected_category != 'all':
        filtered_products = [p for p in PRODUCTS if p['category'] == selected_category]
    else:
        filtered_products = PRODUCTS.copy()

    # Apply search filter
    if search_query:
        filtered_products = [p for p in filtered_products if search_query in p['name'].lower()]
        request.session['last_search'] = search_query
    else:
        request.session.pop('last_search', None)

    cart = request.session.get('cart', {})

    context = {
        'products': filtered_products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'cart_count': sum(cart.values()),
        'last_search': request.session.get('last_search', '')
    }
    return render(request, 'login/ecommerce.html', context)


# ---------------- PRODUCT DETAIL ----------------
def product_detail_view(request, product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return render(request, 'login/product_detail.html', {'product': product})
    return HttpResponse("Product not found", status=404)

# ---------------- LOGOUT ----------------
def logout_view(request):
    request.session.flush()
    return redirect('login')

# ---------------- ADD TO CART ----------------
@csrf_exempt
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_ids = [p['id'] for p in PRODUCTS]

        if product_id in product_ids:
            cart[str(product_id)] = cart.get(str(product_id), 0) + 1
            request.session['cart'] = cart
            request.session.modified = True
            return redirect('ecommerce')

        return HttpResponse("Product not found", status=404)
    return HttpResponse("Invalid request method", status=405)

# ---------------- REMOVE FROM CART ----------------
@csrf_exempt
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
            request.session.modified = True
        return redirect('cart')
    return HttpResponse("Invalid request method", status=405)

# ---------------- VIEW CART ----------------
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for pid, qty in cart.items():
        product = next((p for p in PRODUCTS if str(p['id']) == pid), None)
        if product:
            item = product.copy()
            item['quantity'] = qty
            item['total'] = qty * product['price']
            total_price += item['total']
            cart_items.append(item)

    return render(request, 'login/cart.html', {'cart': cart_items, 'total': total_price})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login/register.html', {'error': 'All fields are required.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'login/register.html', {'error': 'Username already exists.'})

        User.objects.create(username=username, password=make_password(password))
        return redirect('login')

    return render(request, 'login/register.html')
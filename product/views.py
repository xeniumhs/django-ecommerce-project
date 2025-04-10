from django.shortcuts import render,redirect
from .models import Cart, Product, CartItem,Order, OrderItem
from django.core.paginator import Paginator
from .forms import productForm,categoryForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.db import transaction


# Home page view with pagination
def index(request):
    products = Product.objects.all().order_by('product_ID')  # Fetch all products
    paginator = Paginator(products, 16)  # Show 16 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/index.html', {'page_obj': page_obj})

# Product list view with pagination
def product_list(request):
    products = Product.objects.all().order_by('product_ID')  # Fetch all products
    paginator = Paginator(products, 16)  # Show 16 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/product_list.html', {'page_obj': page_obj})


def home(request):
    products = Product.objects.all().order_by('product_ID')  # Fetch all products
    paginator = Paginator(products, 16)  # Show 16 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/home.html', {'page_obj': page_obj})


def shop(request):
    products = Product.objects.all().order_by('product_ID')  # Fetch all products
    paginator = Paginator(products, 20)  # Show 16 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/shop.html', {'page_obj': page_obj})

@login_required
def inventory(request):
    products = Product.objects.all().order_by('product_ID')  # Fetch all products
    paginator = Paginator(products, 20)  # Show 16 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/inventory.html', {'page_obj': page_obj})

def view_product(request,id):
    Product=Product.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

from django.shortcuts import render
from .forms import productForm
from .models import Product

def add(request):
    if request.method == 'POST':
        # Remove the trailing comma here to properly assign the form instance
        form = productForm(request.POST, request.FILES)  
        
        if form.is_valid():
            # Extract cleaned data
            new_product_ID = form.cleaned_data['product_ID']
            new_product_name = form.cleaned_data['product_name']
            new_description = form.cleaned_data['product_description']
            new_price = form.cleaned_data['price']
            new_quantity_in_stock = form.cleaned_data['quantity_in_stock']
            new_product_image = form.cleaned_data['product_image']

            # Create and save the new product instance
            new_product = Product(
                product_ID=new_product_ID,
                product_name=new_product_name,
                product_description=new_description,
                price=new_price,
                quantity_in_stock=new_quantity_in_stock,
                product_image=new_product_image
            )
            new_product.save()

            # Render the template with success message
            return render(request, 'product/add.html', {
                'form': productForm(),
                'success': True
            })

    else:
        form = productForm()

    # Render the form in case of GET request or invalid POST data
    return render(request, 'product/add.html', {
        'form': form
    })

# def add(request):
#     if request.method == 'POST':
#         form=productForm(request.POST,request.FILES)

#         if form.is_valid():
#             new_product_ID= form.cleaned_data['product_ID']
#             new_product_name= form.cleaned_data['product_name']
#             new_description= form.cleaned_data['product_description']
#             new_price= form.cleaned_data['price']
#             new_quantity_in_stock= form.cleaned_data['quantity_in_stock']
#             new_product_image= form.cleaned_data['product_image']

#             new_product = Product(
#                 product_ID = new_product_ID,
#                 product_name = new_product_name,
#                 product_description = new_description,
#                 price = new_price,
#                 quantity_in_stock=new_quantity_in_stock,
#                 product_image=new_product_image
#                 )
#             new_product.save()
#             return render(request, 'product/add.html',{
#                 'form': productForm(),
#                 'success':True
#             })
#     else:
#         form=productForm()
#     return render(request, 'product/add.html',{
#         'form': productForm()
#     })


def add_category(request):
    if request.method == "POST":
        form = categoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product/add_category.html')  # Change this to the appropriate URL name
    else:
        form = categoryForm()
    
    return render(request, 'product/add_category.html', {'form': form})


def product_details(request, id):
    # Fetch the product by its unique identifier (product_ID)
    product = get_object_or_404(Product, product_ID=id)  # Assuming product_ID is the unique field
    
    return render(request, 'product/product_details.html', {'product': product})

@login_required
def edit(request, id):
    # Fetch the product instance or raise a 404 error if not found
    product_instance = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        # Pass the instance to the form for editing
        form = productForm(request.POST, request.FILES, instance=product_instance)
        if form.is_valid():
            form.save()
            return render(request, 'product/edit.html', {
                'form': form,
                'success': True
            })
    else:
        # Prepopulate the form with the product instance
        form = productForm(instance=product_instance)

    return render(request, 'product/edit.html', {
        'form': form
    })



def delete(request, id):
    product = get_object_or_404(Product, pk=id)  # Get the product by ID
    if request.method == 'POST':
        product.delete()  # Delete the product from the database
    return redirect('product:home')  # Redirect to the product list or another view

def about(request):
    return render(request, 'product/about.html')
    

def search(request):
    search_query = request.GET.get('q', '')
    category_query = request.GET.get('category', '')

    # Filter products based on the search query and category query
    products = Product.objects.all()

    if search_query:
        products = products.filter(product_name__icontains=search_query)

    if category_query:
        products = products.filter(category__icontains=category_query)  # Adjust if your category field is named differently

    # Pagination
    paginator = Paginator(products, 16)  # Show 16 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if the user is a superuser (admin)
    if request.user.is_authenticated and request.user.is_superuser:
        # Admin (superuser) view format (inventory-style)
        return render(request, 'product/search_inventory.html', {'page_obj': page_obj, 'search_query': search_query, 'category_query': category_query})
    else:
        # Regular user view format (shop-style)
        return render(request, 'product/search_shop.html', {'page_obj': page_obj, 'search_query': search_query, 'category_query': category_query})
    
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, product_ID=id)
    
    # Get the user's cart or create a new one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)  # No need for 'user.id', use 'request.user'

    # Get the quantity from the form (default to 1)
    quantity = int(request.POST.get('quantity', 1))

    # Check if enough stock is available
    if product.quantity_in_stock < quantity:
        messages.error(request, f"Not enough stock available for {product.product_name}.")
        return redirect('product:product_details', id=product.product_ID)

    # Create or update the CartItem (don't reduce stock here)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if created:
        # New item added to the cart
        cart_item.quantity = quantity
    else:
        # Update the quantity of the existing item in the cart
        cart_item.quantity += quantity  # Increment the quantity

    # Save changes to the cart item
    cart_item.save()

    messages.success(request, f"{product.product_name} has been added to your cart.")
    return redirect('product:cart_view')


@login_required
def cart_view(request):
    # Use get_or_create to avoid DoesNotExist error
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'product/cart_view.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('product:cart_view')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # Optionally remove the item if quantity is 1 and user clicks "decrease"
        cart_item.delete()
    return redirect('product:cart_view')

@login_required
def remove_from_cart(request, cart_item_id):
    # Get the user's cart, then fetch the cart item from the cart
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)

    # Restore stock
    cart_item.product.quantity_in_stock += cart_item.quantity
    cart_item.product.save()

    # Remove the item from the cart
    cart_item.delete()

    messages.success(request, "Item removed from cart.")
    return redirect('product:cart_view')



@login_required
def checkout(request):
    # Fetch the user's cart and associated items
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('product:cart_view')

    # Calculate total price of the cart
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Create an order
    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        status='pending',
    )

    # Process the cart items and reduce stock
    try:
        with transaction.atomic():  # Ensures atomicity for stock updates
            for cart_item in cart_items:
                product = cart_item.product
                cart_item_quantity = cart_item.quantity  # User's cart quantity

                # Check if the product has enough stock
                if product.quantity_in_stock >= cart_item_quantity:
                    # Deduct the purchased quantity from stock
                    product.quantity_in_stock -= cart_item_quantity
                    product.save()  # Save the updated product stock

                    # Add the cart item to the order
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item_quantity,
                        price_at_purchase=cart_item.product.price
                    )
                else:
                    # If not enough stock, raise an error and abort checkout
                    messages.error(request, f"Not enough stock for {product.product_name}.")
                    return redirect('product:cart_view')

            # Clear the cart after processing the order
            cart.cartitem_set.all().delete()

        # Redirect to the order confirmation view
        return redirect('product:order_confirmation', order_id=order.id)

    except Exception as e:
        messages.error(request, f"An error occurred during checkout: {str(e)}")
        return redirect('product:cart_view')

from .forms import ShippingAddressForm
from django.contrib.auth.decorators import login_required

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()

    # Prepare data for the template
    for item in order_items:
        item.total_price = item.quantity * item.price_at_purchase

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=order)
        if form.is_valid():
            form.save()  # Save the updated shipping address
            return redirect('product:order_confirmation', order_id=order.id)  # Redirect to the same page to reflect changes
    else:
        form = ShippingAddressForm(instance=order)

    return render(request, 'product/order_confirmation.html', {
        'order': order,
        'order_items': order_items,
        'form': form,
    })


@login_required
def customer_orders(request):
    # Filter orders by the logged-in user
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "product/customer_orders.html", {"orders": orders})

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "product/order_details.html", {"order": order})

@login_required
def order_list(request):
    orders = Order.objects.all()
    
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("status")
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        return redirect('product:order_list')
    
    return render(request, 'product/order_list.html', {'orders': orders})
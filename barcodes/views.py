# views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .forms import ProductForm
# from django.http import JsonResponse
from .forms import BarcodeSearchForm
from .models import Product, Cart, CartItem
from django.urls import reverse


def add_product(request):
  if request.method == 'POST':
    form = ProductForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      barcode = form.cleaned_data['barcode']
      description = form.cleaned_data['description']
      date_added = form.cleaned_data.get('date_added')

      existing_product = Product.objects.filter(barcode=barcode).first()

      if existing_product:
        return render(request, 'product_exists.html', {'product': existing_product})

      new_product = Product(name=name, barcode=barcode, description=description, date_added=date_added)
      new_product.save()

      # return redirect('all_products', barcode=barcode)
      return redirect(reverse('all_products'), barcode=barcode)
  else:
    form = ProductForm()

  return render(request, 'add_product.html', {'form': form})


def all_products(request):
  products = Product.objects.all()
  return render(request, 'all_products.html', {'products': products})


def product_detail(request, barcode):
  product = get_object_or_404(Product, barcode=barcode)

  if request.method == 'POST':
    form = ProductForm(request.POST)
    if form.is_valid():
      product.name = form.cleaned_data['name']
      product.description = form.cleaned_data['description']
      product.date_added = form.cleaned_data['date_added']  # Update other fields as needed
      product.save()
      return redirect('product_detail', barcode=product.barcode)
  else:
    form = ProductForm(
      initial={'name': product.name, 'description': product.description, 'date_added': product.date_added})
  return render(request, 'product_detail.html', {'product': product, 'form': form})


# def search_product_by_barcode(request):
#
#     if request.method == 'POST':
#       form = BarcodeSearchForm(request.POST)
#       if form.is_valid():
#         barcode = form.cleaned_data['barcode']
#         product = get_object_or_404(Product, barcode=barcode)
#         return render(request, 'product_detail.html', {'product': product})
#     else:
#       form = BarcodeSearchForm()
#
#     return render(request, 'search_product_by_barcode.html', {'form': form})


def search_product_by_barcode(request):
  products = None

  if request.method == 'POST':
    form = BarcodeSearchForm(request.POST)
    if form.is_valid():
      barcode = form.cleaned_data['barcode']
      products = Product.objects.filter(barcode=barcode)

      # # if request.is_ajax():
      # if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
      #   product_data = [{'name': product.name, 'barcode': product.barcode, 'description': product.description,
      #                    'date_added': product.date_added} for product in products]
      #   return JsonResponse({'products': product_data}, safe=False)

  else:
    form = BarcodeSearchForm()

  return render(request, 'search_results.html', {'form': form, 'products': products})

# def delete_product(request, barcode):
#     product = get_object_or_404(Product, barcode=barcode)
#     product.delete()
#     return redirect('all_products')

def edit_product(request, barcode):
    product = get_object_or_404(Product, barcode=barcode)

    if request.method == 'POST':
      form = ProductForm(request.POST, instance=product)
      if form.is_valid():
        form.save()
        return redirect('all_products')
    else:
      form = ProductForm(instance=product)

    return render(request, 'add_product.html', {'form': form})


def delete_product(request, barcode):
  product = get_object_or_404(Product, barcode=barcode)

  if request.method == 'POST':
    # Handle the confirmation of the deletion
    product.delete()
    return redirect('all_products')

  return render(request, 'confirm_delete.html', {'product': product})

@login_required
def search_and_add_to_cart(request, barcode):
  # product = get_object_or_404(Product, barcode=barcode)
    #
    # # Assuming the user is logged in, you can customize this based on your authentication system
    # user = request.user
    #
    # # Get or create a cart for the user
    # cart, created = Cart.objects.get_or_create(user=user)
    #
    # # Check if the product is already in the cart
    # cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    #
    # # If the product is already in the cart, increase the quantity
    # if not created:
    #   cart_item.quantity += 1
    #   cart_item.save()
    #
    # return redirect('cart_view')

    # the code commented above is same as the code below

  if request.user.is_authenticated:
    product = get_object_or_404(Product, barcode=barcode)

    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # If the product is already in the cart, increase the quantity
    if not created:
      cart_item.quantity += 1
      cart_item.save()

    return redirect('cart_view')
  else:
    # Handle the case where the user is not authenticated (optional)
    return render(request, 'not_authenticated_error.html')


def cart_view(request):
  user = request.user
  cart = Cart.objects.get(user=user)
  cart_items = cart.cartitem_set.all()

  return render(request, 'cart_view.html', {'cart_items': cart_items})


def handlesignup(request):
  if request.method == 'POST':
    username = request.POST.get("username")
    password = request.POST.get("password")

    myuser = User.objects.create_user(username, password)
    myuser.save()
  return render(request, 'signup.html')


def handlelogin(request):
  if request.method == 'POST':
    username = request.POST.get("username")
    password = request.POST.get("password")
    myuser = authenticate(username=username, password=password)

    if myuser is not None:
      login(request, myuser)
      return redirect('all_products')
    else:
      return redirect('/login')
    return render(request, 'login.html')


def handlelogout(request):
  logout(request)
  return redirect('/signup')


@login_required
def checkout_view(request):
    # Retrieve the user's cart
    cart = Cart.objects.get(user=request.user)

    # You may want to perform additional logic here, such as calculating the total

    # for item in cart.cartitem_set.all():
    #   product = item.product
    #   product.status = 'Sold'  # Update the status (adjust based on your model)
    #   product.save()

    for item in cart.cartitem_set.all():
      product = item.product
      product.delete()

    cart.cartitem_set.all().delete()

    return render(request, 'checkout.html', {'cart': cart})

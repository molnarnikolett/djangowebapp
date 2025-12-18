from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Item
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .forms import BidForm
from .forms import ItemForm

def base(request):
    return render(request, "auction/base.html")

def home(request):
    return render(request, "auction/home.html")

def staff(request):
    return render(request, "auction/staff.html")

def contact(request):
    return render(request, "auction/contact.html")

def items(request):
    item_list = Item.objects.all().order_by("auction_time")

    paginator = Paginator(item_list, 5)  # 5 darab / oldal
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "auction/items.html", {
        "page_obj": page_obj
    })
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def custom_logout(request):
    logout(request)
    return redirect("home")

def is_auctioneer(user):
    return user.is_authenticated and user.groups.filter(name="arverezo").exists()

def is_site_admin(user):
    return user.is_authenticated and user.is_superuser

def items(request):
    item_list = Item.objects.all().order_by("auction_time")
    paginator = Paginator(item_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    is_auctioneer = False
    if request.user.is_authenticated:
        is_auctioneer = request.user.groups.filter(name="arverezo").exists()

    return render(request, "auction/items.html", {
        "page_obj": page_obj,
        "is_auctioneer": is_auctioneer,
    })

@login_required
def start_auction(request, item_id):
    if not is_auctioneer(request.user):
        return HttpResponseForbidden("Nincs jogosultságod aukciót indítani.")

    item = get_object_or_404(Item, id=item_id)
    item.is_active = True
    item.is_closed = False
    item.current_price = item.starting_price
    item.winner = None
    item.save()
    return redirect("items")


@login_required
def stop_auction(request, item_id):
    if not is_auctioneer(request.user):
        return HttpResponseForbidden("Nincs jogosultságod aukciót leállítani.")

    item = get_object_or_404(Item, id=item_id)
    item.is_active = False
    item.is_closed = True
    item.save()
    return redirect("items")

@login_required
def bid(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if not item.is_active:
        return HttpResponseForbidden("Erre a tárgyra jelenleg nem lehet licitálni, az aukció nem aktív.")

    current_price = item.current_price or item.starting_price

    if request.method == "POST":
        form = BidForm(request.POST, current_price=current_price)
        if form.is_valid():
            amount = form.cleaned_data["amount"]

            item.current_price = amount
            item.winner = request.user
            item.save()

            return redirect("items")
    else:
        form = BidForm(current_price=current_price)

    return render(request, "auction/bid.html", {
        "item": item,
        "form": form,
        "current_price": current_price,
    })

@login_required
def manage_items(request):
    if not is_site_admin(request.user):
        return HttpResponseForbidden("Nincs jogosultságod a tárgyak kezeléséhez.")

    items = Item.objects.all().order_by("auction_time")
    return render(request, "auction/manage_items.html", {"items": items})


@login_required
def create_item(request):
    if not is_site_admin(request.user):
        return HttpResponseForbidden("Nincs jogosultságod új tárgyat létrehozni.")

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("manage_items")
    else:
        form = ItemForm()

    return render(request, "auction/item_form.html", {
        "form": form,
        "title": "Új tárgy hozzáadása",
    })


@login_required
def edit_item(request, item_id):
    if not is_site_admin(request.user):
        return HttpResponseForbidden("Nincs jogosultságod a tárgyak szerkesztéséhez.")

    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("manage_items")
    else:
        form = ItemForm(instance=item)

    return render(request, "auction/item_form.html", {
        "form": form,
        "title": f"Tárgy szerkesztése: {item.name}",
    })


@login_required
def delete_item(request, item_id):
    if not is_site_admin(request.user):
        return HttpResponseForbidden("Nincs jogosultságod a tárgyak törléséhez.")

    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        item.delete()
        return redirect("manage_items")

    return render(request, "auction/item_confirm_delete.html", {"item": item})
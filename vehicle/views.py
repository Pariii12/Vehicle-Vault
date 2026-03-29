from math import radians, sin, cos, sqrt, atan2

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from core.models import User
from .decorators import role_required
from .models import (
    Vehicle,
    VehicleImage,
    TestDrive,
    VehicleInspection,
    Message,
    Favourite,
    Offer,
    Transaction,
)
from .forms import (
    VehicleForm,
    VehicleFilterForm,
    TestDriveForm,
    VehicleInspectionForm,
    MessageForm,
    OfferForm,
    TransactionForm
)


def distance(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def home_view(request):
    vehicles = Vehicle.objects.filter(featured=True)[:6]  # only featured cars
    return render(request, 'home/index.html', {'vehicles': vehicles})

@role_required(allowed_roles=["admin"])
def adminDashboardView(request):
    return render(request, "vehicles/admin/admin_dashboard.html")


@role_required(allowed_roles=["seller"])
def sellerDashboardView(request):
    return render(request, "vehicles/seller/seller_dashboard.html")


@role_required(allowed_roles=["buyer"])
def buyerDashboardView(request):
    return render(request, "vehicles/buyer/buyer_dashboard.html")

def vehicle_list(request):
    # Start with all active vehicles
    vehicles_qs = (
        Vehicle.objects.filter(status="Active")
        .select_related("seller")
        .prefetch_related("images")
        .order_by("-listed_at")
    )

    # -----------------------------
    # 1. FORM FILTERS
    # -----------------------------
    form = VehicleFilterForm(request.GET or None)

    if form.is_valid():
        brand = form.cleaned_data.get("brand")
        model = form.cleaned_data.get("model")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        min_year = form.cleaned_data.get("min_year")
        max_year = form.cleaned_data.get("max_year")
        fuel_type = form.cleaned_data.get("fuel_type")
        transmission = form.cleaned_data.get("transmission")
        body_type = form.cleaned_data.get("body_type")
        city = form.cleaned_data.get("city")
        state = form.cleaned_data.get("state")
        radius = form.cleaned_data.get("radius")
        user_lat = form.cleaned_data.get("user_lat")
        user_lon = form.cleaned_data.get("user_lon")

        if brand:
            vehicles_qs = vehicles_qs.filter(brand__icontains=brand)

        if model:
            vehicles_qs = vehicles_qs.filter(model__icontains=model)

        if min_price:
            vehicles_qs = vehicles_qs.filter(price__gte=min_price)

        if max_price:
            vehicles_qs = vehicles_qs.filter(price__lte=max_price)

        if min_year:
            vehicles_qs = vehicles_qs.filter(year__gte=min_year)

        if max_year:
            vehicles_qs = vehicles_qs.filter(year__lte=max_year)

        if fuel_type:
            vehicles_qs = vehicles_qs.filter(fuel_type=fuel_type)

        if transmission:
            vehicles_qs = vehicles_qs.filter(transmission=transmission)

        if body_type:
            vehicles_qs = vehicles_qs.filter(body_type=body_type)

        if city:
            vehicles_qs = vehicles_qs.filter(location__icontains=city)

        if state:
            vehicles_qs = vehicles_qs.filter(location__icontains=state)

        # Radius filter (distance-based)
        if radius and user_lat and user_lon:
            radius = float(radius)
            filtered_ids = []
            for v in vehicles_qs:
                if v.latitude and v.longitude:
                    d = distance(user_lat, user_lon, v.latitude, v.longitude)
                    if d <= radius:
                        filtered_ids.append(v.id)
            vehicles_qs = vehicles_qs.filter(id__in=filtered_ids)

    # -----------------------------
    # 2. MANUAL FILTERS (brand, city, budget)
    # -----------------------------
    brand = request.GET.get("brand")
    if brand:
        vehicles_qs = vehicles_qs.filter(brand__icontains=brand)

    city = request.GET.get("city")
    if city:
        vehicles_qs = vehicles_qs.filter(location__icontains=city)

    budget = request.GET.get("budget")
    if budget == "under-5":
        vehicles_qs = vehicles_qs.filter(price__lte=500000)
    elif budget == "5-10":
        vehicles_qs = vehicles_qs.filter(price__gte=500000, price__lte=1000000)
    elif budget == "10-20":
        vehicles_qs = vehicles_qs.filter(price__gte=1000000, price__lte=2000000)
    elif budget == "20-40":
        vehicles_qs = vehicles_qs.filter(price__gte=2000000, price__lte=4000000)
    elif budget == "above-40":
        vehicles_qs = vehicles_qs.filter(price__gte=4000000)

    # -----------------------------
    # 3. SORTING
    # -----------------------------
    sort = request.GET.get("sort")
    if sort == "price_asc":
        vehicles_qs = vehicles_qs.order_by("price")
    elif sort == "price_desc":
        vehicles_qs = vehicles_qs.order_by("-price")
    elif sort == "year_desc":
        vehicles_qs = vehicles_qs.order_by("-year")
    elif sort == "year_asc":
        vehicles_qs = vehicles_qs.order_by("year")
    else:
        vehicles_qs = vehicles_qs.order_by("-listed_at")

    # -----------------------------
    # 4. PAGINATION
    # -----------------------------
    paginator = Paginator(vehicles_qs, 12)
    page_number = request.GET.get("page")
    vehicles_page = paginator.get_page(page_number)

    return render(
        request,
        "vehicles/vehicle_list.html",
        {
            "vehicles": vehicles_page,
            "filter_form": form,
            "sort": sort,
        },
    )



def vehicle_detail(request, pk):
    vehicle = (
        Vehicle.objects.select_related("seller")
        .prefetch_related("images", "offers", "testdrives")
        .get(pk=pk)
    )

    related_vehicles = (
        Vehicle.objects.filter(
            brand=vehicle.brand, body_type=vehicle.body_type, status="Active"
        )
        .exclude(id=vehicle.id)
        .select_related("seller")
        .prefetch_related("images")[:4]
    )

    return render(
        request,
        "vehicles/vehicle_detail.html",
        {"vehicle": vehicle, "related_vehicles": related_vehicles},
    )


@login_required
def add_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.seller = request.user
            vehicle.save()

            for img in request.FILES.getlist("images"):
                VehicleImage.objects.create(vehicle=vehicle, image=img)

            messages.success(request, "Vehicle listed successfully.")
            return redirect("vehicle_detail", pk=vehicle.pk)
    else:
        form = VehicleForm()

    return render(request, "vehicles/add_vehicle.html", {"form": form})


@login_required
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, seller=request.user)

    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()

            for img in request.FILES.getlist("images"):
                VehicleImage.objects.create(vehicle=vehicle, image=img)

            delete_ids = request.POST.getlist("delete_images")
            if delete_ids:
                VehicleImage.objects.filter(
                    vehicle=vehicle, id__in=delete_ids
                ).delete()

            messages.success(request, "Vehicle updated successfully.")
            return redirect("vehicle_detail", pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)

    images = vehicle.images.all()
    return render(
        request,
        "vehicles/edit_vehicle.html",
        {"form": form, "vehicle": vehicle, "images": images},
    )


@login_required
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, seller=request.user)

    if request.method == "POST":
        vehicle.delete()
        messages.success(request, "Vehicle deleted successfully.")
        return redirect("vehicle_list")

    return render(request, "vehicles/confirm_delete_vehicle.html", {"vehicle": vehicle})


def compare_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    other_id = request.GET.get("other")
    other_vehicle = None
    if other_id and other_id != str(pk):
        other_vehicle = get_object_or_404(Vehicle, pk=other_id)
    return render(
        request,
        "vehicles/compare_vehicle.html",
        {"vehicle": vehicle, "other_vehicle": other_vehicle},
    )


@login_required
def schedule_testdrive(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if vehicle.seller == request.user:
        messages.error(request, "You cannot schedule a test drive for your own vehicle.")
        return redirect("vehicle_detail", pk=pk)

    if request.method == "POST":
        form = TestDriveForm(request.POST)
        if form.is_valid():
            td = form.save(commit=False)
            td.vehicle = vehicle
            td.buyer = request.user
            td.seller = vehicle.seller
            td.save()
            messages.success(request, "Test drive scheduled successfully.")
            return redirect("my_testdrive")
    else:
        form = TestDriveForm()

    return render(
        request,
        "testdrives/schedule_testdrive.html",
        {"form": form, "vehicle": vehicle},
    )


@login_required
def my_testdrive(request):
    testdrives = (
        TestDrive.objects.filter(buyer=request.user)
        .select_related("vehicle", "seller")
        .order_by("-scheduled_date")
    )
    return render(
        request, "testdrives/my_testdrive.html", {"testdrives": testdrives}
    )


@login_required
def inspection_report(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    inspection = VehicleInspection.objects.filter(vehicle=vehicle).first()

    if request.method == "POST":
        form = VehicleInspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            report = form.save(commit=False)
            report.vehicle = vehicle
            report.save()
            messages.success(request, "Inspection report saved.")
            return redirect("inspection_report", pk=vehicle.pk)
    else:
        form = VehicleInspectionForm(instance=inspection)

    return render(
        request,
        "inspections/inspection_report.html",
        {"form": form, "vehicle": vehicle, "inspection": inspection},
    )


@login_required
def inbox(request):
    msgs = (
        Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .select_related("sender", "receiver", "vehicle")
        .order_by("-sent_at")
    )
    return render(request, "messages/inbox.html", {"messages": msgs})


@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)

    conversation = (
        Message.objects.filter(
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user],
        )
        .select_related("sender", "receiver", "vehicle")
        .order_by("sent_at")
    )

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect("chat", user_id=other_user.id)
    else:
        form = MessageForm()

    return render(
        request,
        "messages/chat.html",
        {
            "conversation": conversation,
            "form": form,
            "other_user": other_user,
        },
    )


@login_required
def add_favourite(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    Favourite.objects.get_or_create(buyer=request.user, vehicle=vehicle)
    messages.success(request, "Added to favourites.")
    return redirect("favourite_list")


@login_required
def remove_favourite(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    Favourite.objects.filter(buyer=request.user, vehicle=vehicle).delete()
    messages.success(request, "Removed from favourites.")
    return redirect("favourite_list")


@login_required
def favourite_list(request):
    favourites = (
        Favourite.objects.filter(buyer=request.user)
        .select_related("vehicle")
        .order_by("-saved_at")
    )
    return render(
        request, "favourites/favourite_list.html", {"favourites": favourites}
    )


@login_required
def make_offer(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if vehicle.seller == request.user:
        messages.error(request, "You cannot make an offer on your own vehicle.")
        return redirect("vehicle_detail", pk=pk)

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.vehicle = vehicle
            offer.buyer = request.user
            offer.save()
            messages.success(request, "Offer submitted.")
            return redirect("my_offer")
    else:
        form = OfferForm()

    return render(
        request, "offers/make_offer.html", {"form": form, "vehicle": vehicle}
    )


@login_required
def my_offer(request):
    offers = (
        Offer.objects.filter(buyer=request.user)
        .select_related("vehicle")
        .order_by("-created_at")
    )
    return render(request, "offers/my_offer.html", {"offers": offers})


@login_required
def offer_details(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, "offers/offer_details.html", {"offer": offer})


@login_required
def transaction_list(request):
    transactions = (
        Transaction.objects.filter(
            Q(buyer=request.user) | Q(seller=request.user)
        )
        .select_related("vehicle", "buyer", "seller")
        .order_by("-transaction_date")
    )
    return render(
        request,
        "transactions/transaction_list.html",
        {"transactions": transactions},
    )


@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(
        request,
        "transactions/transaction_detail.html",
        {"transaction": transaction},
    )



def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  # or wherever you want
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})
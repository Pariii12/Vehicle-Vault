from django.urls import path
from . import views

urlpatterns = [

    # ---------------------------
    # HOME & DASHBOARDS
    # ---------------------------

    path('admin-dashboard/', views.adminDashboardView, name='admin_dashboard'),
    path('seller-dashboard/', views.sellerDashboardView, name='seller_dashboard'),
    path('buyer-dashboard/', views.buyerDashboardView, name='buyer_dashboard'),

    # ---------------------------
    # VEHICLES
    # ---------------------------
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/<int:pk>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),
    path('vehicles/<int:pk>/compare/', views.compare_vehicle, name='compare_vehicle'),

    # ---------------------------
    # TEST DRIVE
    # ---------------------------
    path('vehicles/<int:pk>/testdrive/', views.schedule_testdrive, name='schedule_testdrive'),
    path('my-testdrives/', views.my_testdrive, name='my_testdrive'),

    # ---------------------------
    # INSPECTION
    # ---------------------------
    path('vehicles/<int:pk>/inspection/', views.inspection_report, name='inspection_report'),

    # ---------------------------
    # MESSAGING
    # ---------------------------
    path('inbox/', views.inbox, name='inbox'),
    path('chat/<int:user_id>/', views.chat, name='chat'),

    # ---------------------------
    # FAVOURITES
    # ---------------------------
    path('favourites/', views.favourite_list, name='favourite_list'),
    path('favourites/add/<int:pk>/', views.add_favourite, name='add_favourite'),
    path('favourites/remove/<int:pk>/', views.remove_favourite, name='remove_favourite'),

    # ---------------------------
    # OFFERS
    # ---------------------------
    path('vehicles/<int:pk>/offer/', views.make_offer, name='make_offer'),
    path('my-offers/', views.my_offer, name='my_offer'),
    path('offers/<int:pk>/', views.offer_details, name='offer_details'),

    # ---------------------------
    # TRANSACTIONS
    # ---------------------------
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),

]

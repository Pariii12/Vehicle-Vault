from django.contrib import admin
from .models import Vehicle,VehicleImage,Offer,Transaction,TestDrive,Message,VehicleInspection,Favourite,Payment

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(VehicleImage)
admin.site.register(Offer)
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        'vehicle',
        'buyer',
        'seller',
        'final_price',
        'transaction_date',
        'updated_at',
    )
    readonly_fields = ('transaction_date','updated_at')
admin.site.register(TestDrive)
admin.site.register(Message)
admin.site.register(VehicleInspection)
admin.site.register(Favourite)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "currency", "status", "payment_date")


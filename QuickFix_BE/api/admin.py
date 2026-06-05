from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(AuditLog)
admin.site.register(User, UserAdmin)
admin.site.register(CustomerProfile)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(ProductBatch)
admin.site.register(StockMovement)
admin.site.register(Prescription)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Notification)
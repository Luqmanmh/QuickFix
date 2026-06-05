from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
import uuid
from django.conf import settings

# =====================================================
# USER MANAGEMENT
# =====================================================


class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        PHARMACIST = "PHARMACIST", "Pharmacist"
        CASHIER = "CASHIER", "Cashier"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class CustomerProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    date_of_birth = models.DateField(null=True, blank=True)

    gender = models.CharField(
        max_length=1, choices=[("M", "Male"), ("F", "Female")], blank=True, null=True
    )
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    
    allergies = models.TextField(blank=True)

    chronic_conditions = models.TextField(blank=True)
    
    address = models.TextField(blank=True)


# =====================================================
# PRODUCT & INVENTORY
# =====================================================


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):

    name = models.CharField(max_length=255)

    phone = models.CharField(max_length=30)

    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )

    name = models.CharField(max_length=255)

    sku = models.CharField(max_length=50, unique=True)

    generic_name = models.CharField(max_length=255, blank=True)

    description = models.TextField()

    dosage_form = models.CharField(max_length=100)

    strength = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    minimum_stock = models.PositiveIntegerField(default=10)

    requires_prescription = models.BooleanField(default=False)

    image = models.ImageField(upload_to="products/", blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductBatch(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="batches"
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    batch_number = models.CharField(max_length=100)

    expiry_date = models.DateField()

    stock_qty = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "batch_number")
        ordering = ["expiry_date"]

    def __str__(self):
        return f"{self.product.name} ({self.batch_number})"


class StockMovement(models.Model):

    class MovementType(models.TextChoices):
        PURCHASE = "PURCHASE", "Purchase"
        SALE = "SALE", "Sale"
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"
        EXPIRED = "EXPIRED", "Expired"
        DELETED = "DELETED", "Deleted"

    batch = models.ForeignKey(
        ProductBatch, on_delete=models.SET_NULL, related_name="movements",
        blank=True, null=True
    )

    movement_type = models.CharField(max_length=20, choices=MovementType.choices)

    quantity = models.IntegerField()

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


# =====================================================
# PRESCRIPTION
# =====================================================


class Prescription(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="prescriptions"
    )

    uploaded_file = models.FileField(upload_to="prescriptions/")

    doctor_name = models.CharField(max_length=255, blank=True)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_prescriptions",
    )

    verified_at = models.DateTimeField(null=True, blank=True)

    rejection_reason = models.TextField(blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class PrescriptionItem(models.Model):

    cart = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)


# =====================================================
# CART
# =====================================================


class Cart(models.Model):

    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")

    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)


# =====================================================
# ORDERS
# =====================================================


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING_PAYMENT = "PENDING_PAYMENT", "Pending Payment"
        PAID = "PAID", "Paid"
        ORDER_CREATED = "ORDER_CREATED", "OrderCreated" 
        PRESCRIPTION_REVIEW = "PRESCRIPTION_REVIEW", "Prescription Review"
        PREPARING = "PREPARING", "Preparing"
        READY = "READY", "Ready"
        SHIPPED = "SHIPPED", "Shipped"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    class Channel(models.TextChoices):
        ONLINE = "ONLINE", "Online"
        COUNTER = "COUNTER", "Counter"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")

    prescription = models.ForeignKey(
        Prescription, on_delete=models.SET_NULL, null=True, blank=True
    )

    channel = models.CharField(
        max_length=20, choices=Channel.choices, default=Channel.ONLINE
    )

    status = models.CharField(
        max_length=30, choices=Status.choices, default=Status.PENDING_PAYMENT
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    batch = models.ForeignKey(
        ProductBatch, on_delete=models.PROTECT, null=True, blank=True
    )

    quantity = models.PositiveIntegerField()

    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)


# =====================================================
# PAYMENT
# =====================================================


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESSFUL = "SUCCESSFUL", "Successful"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    order = models.OneToOneField(
        Order, on_delete=models.PROTECT, related_name="payment"
    )

    transaction_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )

    payment_method = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    paid_at = models.DateTimeField(null=True, blank=True)


# =====================================================
# NOTIFICATIONS
# =====================================================


class Notification(models.Model):

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


# =====================================================
# AUDIT LOGS
# =====================================================


class AuditLog(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    action = models.CharField(max_length=255)

    entity_type = models.CharField(max_length=100)

    entity_id = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

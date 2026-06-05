
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from decimal import Decimal
from random import randint, choice
from datetime import timedelta
from django.utils import timezone
from django.db import transaction

from api.models import (
    CustomerProfile,
    Category,
    Supplier,
    Product,
    ProductBatch,
    StockMovement,
    Cart,
    CartItem,
    Prescription,
    Order,
    OrderItem,
    Payment,
    Notification,
    AuditLog,
)

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with sample pharmacy data"
    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Cleaning database...")

        AuditLog.objects.all().delete()
        Notification.objects.all().delete()
        Payment.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Prescription.objects.all().delete()
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        StockMovement.objects.all().delete()
        ProductBatch.objects.all().delete()
        Product.objects.all().delete()
        Supplier.objects.all().delete()
        Category.objects.all().delete()
        CustomerProfile.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Database cleaned.")

        self.stdout.write("Seeding database...")

        # ===============================
        # USERS
        # ===============================

        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@apotek.com",
                "role": User.Role.ADMIN,
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        admin.set_password("password123")
        admin.save()

        pharmacists = []

        for i in range(2):
            user = User.objects.create_user(
                username=f"pharmacist{i}",
                email=f"pharmacist{i}@apotek.com",
                password="password123",
                role=User.Role.PHARMACIST,
                is_active=True,
            )
            pharmacists.append(user)

        cashiers = []

        for i in range(2):
            user = User.objects.create_user(
                username=f"cashier{i}",
                email=f"cashier{i}@apotek.com",
                password="password123",
                role=User.Role.CASHIER,
                is_active=True,
            )
            cashiers.append(user)

        customers = []

        for i in range(20):
            user = User.objects.create_user(
                username=f"customer{i}",
                email=f"customer{i}@mail.com",
                password="password123",
                role=User.Role.CUSTOMER,
                is_active=True,
            )

            CustomerProfile.objects.create(
                user=user,
                date_of_birth=fake.date_of_birth(),
                gender=choice(["M", "F"]),
                phone_number=fake.phone_number(),
                allergies=fake.word(),
                chronic_conditions=fake.word(),
                address=fake.address(),
            )

            Cart.objects.create(customer=user)

            customers.append(user)

        # ===============================
        # CATEGORIES
        # ===============================

        categories = []

        category_data = [
            ("Obat Bebas", "obat-bebas"),
            ("Obat Resep", "obat-resep"),
            ("Suplemen", "suplemen"),
            ("Alat Kesehatan", "alat-kesehatan"),
        ]

        for name, slug in category_data:
            category = Category.objects.create(
                name=name,
                slug=slug,
                description=f"{name} category",
            )
            categories.append(category)

        # ===============================
        # SUPPLIERS
        # ===============================

        suppliers = []

        for i in range(5):
            supplier = Supplier.objects.create(
                name=fake.company(),
                phone=fake.phone_number(),
                email=fake.company_email(),
            )
            suppliers.append(supplier)

        # ===============================
        # PRODUCTS
        # ===============================

        medicine_names = [
            "Paracetamol",
            "Amoxicillin",
            "Vitamin C",
            "Ibuprofen",
            "Cetirizine",
            "Omeprazole",
            "Antangin",
            "Bodrex",
            "Promag",
            "Panadol",
        ]

        products = []

        for medicine in medicine_names:

            product = Product.objects.create(
                category=choice(categories),
                name=medicine,
                sku=f"SKU-{randint(10000,99999)}",
                generic_name=medicine,
                description=fake.text(),
                dosage_form=choice(
                    ["Tablet", "Capsule", "Syrup"]
                ),
                strength=choice(
                    ["250mg", "500mg", "1000mg"]
                ),
                price=Decimal(randint(5000, 50000)),
                minimum_stock=10,
                requires_prescription=choice([True, False]),
                is_active=True,
            )

            products.append(product)

        # ===============================
        # BATCHES
        # ===============================

        batches = []

        for product in products:

            for batch_no in range(2):

                batch = ProductBatch.objects.create(
                    product=product,
                    supplier=choice(suppliers),
                    batch_number=f"BATCH-{randint(1000,9999)}",
                    expiry_date=timezone.now().date()
                    + timedelta(days=randint(90, 720)),
                    stock_qty=randint(50, 300),
                )

                batches.append(batch)

                StockMovement.objects.create(
                    batch=batch,
                    movement_type=StockMovement.MovementType.PURCHASE,
                    quantity=batch.stock_qty,
                    notes="Initial stock",
                )

        # ===============================
        # PRESCRIPTIONS
        # ===============================

        prescriptions = []

        for customer in customers[:10]:

            prescription = Prescription.objects.create(
                customer=customer,
                uploaded_file="prescriptions/sample.pdf",
                doctor_name=fake.name(),
                status=choice(
                    [
                        Prescription.Status.PENDING,
                        Prescription.Status.APPROVED,
                    ]
                ),
            )

            prescriptions.append(prescription)

        # ===============================
        # ORDERS
        # ===============================

        for i in range(30):

            customer = choice(customers)

            order = Order.objects.create(
                customer=customer,
                channel=choice(
                    [
                        Order.Channel.ONLINE,
                        Order.Channel.COUNTER,
                    ]
                ),
                status=choice(
                    [
                        Order.Status.PAID,
                        Order.Status.PREPARING,
                        Order.Status.COMPLETED,
                    ]
                ),
                total_amount=0,
            )

            total = Decimal("0")

            for _ in range(randint(1, 4)):

                product = choice(products)

                batch = choice(
                    ProductBatch.objects.filter(
                        product=product
                    )
                )

                qty = randint(1, 5)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    batch=batch,
                    quantity=qty,
                    price_at_purchase=product.price,
                )

                total += product.price * qty

            order.total_amount = total
            order.save()

            Payment.objects.create(
                order=order,
                transaction_id=f"TX-{randint(100000,999999)}",
                payment_method=choice(
                    [
                        "Midtrans",
                        "Bank Transfer",
                        "Cash",
                    ]
                ),
                status=Payment.Status.SUCCESSFUL,
                amount=total,
                paid_at=timezone.now(),
            )

        # ===============================
        # NOTIFICATIONS
        # ===============================

        for customer in customers[:10]:

            Notification.objects.create(
                recipient=customer,
                title="Pesanan Diproses",
                message="Pesanan Anda sedang diproses",
            )

        # ===============================
        # AUDIT LOGS
        # ===============================

        for user in customers[:10]:

            AuditLog.objects.create(
                user=user,
                action="LOGIN",
                entity_type="User",
                entity_id=str(user.id),
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Database seeded successfully!"
            )
        )


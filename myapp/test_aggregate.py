import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from myapp.models import Order, Customer
from django.db.models import Sum, Count

def create_data():
    customer1 = Customer.objects.create(name="Ali")
    customer2 = Customer.objects.create(name="Vali")

    Order.objects.create(customer=customer1, price=1000)
    Order.objects.create(customer=customer1, price=2000)
    Order.objects.create(customer=customer2, price=1500)

    print("Ma'lumotlar bazaga qo‘shildi!")

def test_aggregate():
    total_price = Order.objects.aggregate(Sum("price"))
    print("Jami buyurtma summasi:", total_price["price__sum"])

def test_annotate():
    customers = Customer.objects.annotate(order_count=Count("orders"))
    for customer in customers:
        print(f"{customer.name} ning buyurtmalari soni: {customer.order_count}")

if __name__ == "__main__":
    # create_data()
    test_aggregate()
    test_annotate()
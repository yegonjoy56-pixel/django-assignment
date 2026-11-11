
from decimal import Decimal

from plants.models import Plant


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if cart is None:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, plant, quantity=1, override_quantity=False):
        plant_id = str(plant.id)

        if plant_id not in self.cart:
            self.cart[plant_id] = {
                "quantity": 0,
                "price": str(plant.price or Decimal("0.00")),
            }

        if override_quantity:
            self.cart[plant_id]["quantity"] = quantity
        else:
            self.cart[plant_id]["quantity"] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, plant):
        plant_id = str(plant.id)

        if plant_id in self.cart:
            del self.cart[plant_id]
            self.save()

    def __iter__(self):
        plant_ids = self.cart.keys()
        plants = Plant.objects.filter(id__in=plant_ids)

        for plant in plants:
            item = self.cart[str(plant.id)].copy()
            item["plant"] = plant
            item["price"] = Decimal(item["price"])
            item["total_price"] = (
                item["price"] * item["quantity"]
            )
            yield item

    def __len__(self):
        return sum(
            item["quantity"] for item in self.cart.values()
        )

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

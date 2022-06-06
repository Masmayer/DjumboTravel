from django.db import models


class Planes(models.Model):
    STATUS_CHOICES = (
        ('air', 'Air'),
        ('land', 'Land'),
    )
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'PLANES'

    def __str__(self):
        return self.name

    @property
    def get_actual_stock(self):
        total_stock = 0
        for stock in self.planestock.all():
            total_stock += stock.maximum_quantity
        return total_stock


class Base(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'BASE'

    def __str__(self):
        return self.name


class Attendants(models.Model):
    user_id = models.OneToOneField(
        "customauth.User", on_delete=models.SET_NULL, null=True,
        related_name="attendants",
    )
    plane_id = models.ForeignKey(
        "inventory.Planes", on_delete=models.SET_NULL, null=True,
        related_name="attendants",
    )

    class Meta:
        db_table = 'ATTENDANTS'

    def __str__(self):
        return f"{self.user_id.nif}"


class Providers(models.Model):
    user_id = models.OneToOneField(
        "customauth.User", on_delete=models.SET_NULL, null=True,
        related_name="providers"
    )
    base = models.ForeignKey(
        "inventory.Base", on_delete=models.SET_NULL, null=True,
        related_name="providers_base"
    )

    class Meta:
        db_table = "PROVIDERS"

    def __str__(self):
        return f"{self.user_id.nif}"


class Routes(models.Model):
    plane_id = models.ForeignKey(
        "inventory.Planes", on_delete=models.SET_NULL, null=True,
        related_name="routes"
    )
    origin = models.CharField(max_length=5)
    destination = models.CharField(max_length=5)

    class Meta:
        db_table = "ROUTES"

    def __str__(self):
        return f"{self.origin}-{self.destination}"


class Products(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "PRODUCTS"

    def __str__(self):
        return self.name


class PlaneStock(models.Model):
    plane_id = models.ForeignKey(
        "inventory.Planes", on_delete=models.SET_NULL, null=True,
        related_name="planestock"
    )
    product_id = models.ForeignKey(
        "inventory.Products", on_delete=models.SET_NULL, null=True,
        related_name="planestock"
    )
    quantity = models.PositiveIntegerField()
    maximum_quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "planeSTOCK"

    def __str__(self):
        return f"{self.plane_id}"


class Orders(models.Model):
    attendant_id = models.ForeignKey(
        "inventory.Attendants", on_delete=models.SET_NULL, null=True,
        related_name="orders"
    )
    providers = models.ForeignKey(
        "inventory.Providers", on_delete=models.SET_NULL, null=True,
        related_name="orders"
    )
    base = models.ForeignKey(
        "inventory.Base", on_delete=models.SET_NULL, null=True,
        related_name="orders"
    )
    date = models.DateField()
    status = models.CharField(max_length=10)

    class Meta:
        db_table = "ORDERS"

    def __str__(self):
        return f"{self.id}"


class OrderLine(models.Model):
    product_id = models.ForeignKey(
        "inventory.Products", on_delete=models.SET_NULL, null=True,
        related_name="orderline"
    )
    order_id = models.ForeignKey(
        "inventory.Orders", on_delete=models.SET_NULL, null=True,
        related_name="orderline"
    )
    quantity = models.PositiveIntegerField()
    fill_quantity = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        db_table = "ORDERLINES"

    def __str__(self):
        return f"{self.product_id}"

    @property
    def total_product_price(self):
        if self.product_id and self.quantity:
            return self.product_id.price * self.quantity
        else:
            return 0


class Notifications(models.Model):
    user_id = models.ForeignKey(
        "customauth.User", on_delete=models.SET_NULL, null=True,
        related_name="notifications"
    )
    description = models.CharField(max_length=255)
    order_id = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "NOTIFICATIONS"

    def __str__(self):
        return f"{self.user_id}"

from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.text import slugify

from accounts.models import User


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Campaign(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="campaign/")
    end_date = models.DateField()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=False, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["-id"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Menu(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=False, unique=True)
    image = models.ImageField(upload_to="menus/")
    price = models.FloatField()
    description = models.TextField()
    cook_time = models.IntegerField()
    offer_price = models.FloatField()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Order(BaseModel):
    total_price = models.FloatField()
    tax = models.FloatField()
    is_paid = models.BooleanField(default=False)
    is_served = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.user.email


class OrderItem(BaseModel):
    quantity = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to="OrderItems/", blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.menu.title


class Resarvation(BaseModel):
    RESERVATION_STATUS = (
        ("pending", "pending"),
        ("confirmed", "confirmed"),
        ("cancelled", "cancelled"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    person = models.IntegerField(
        default=2,
        validators=[MaxValueValidator(12)],
        help_text="Maximum 12 person reservation allowed.",
    )
    status = models.CharField(choices=RESERVATION_STATUS, max_length=10)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.email


class Review(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    comment = models.TextField()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.product.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.email

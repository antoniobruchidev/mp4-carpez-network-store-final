from django.contrib import admin

from .models import Order, OrderLineItem

# Register your models here.


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = (
        "lineitem_total",
        "discounted_price",
    )


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        "order_number",
        "date",
        "full_name",
        "email",
        "shipping",
        "delivery_cost",
        "order_total",
        "discount",
        "grand_total",
        "stripe_pid",
    )

    fields = (
        "order_number",
        "full_name",
        "email",
        "shipping",
        "delivery_cost",
        "order_total",
        "discount",
        "grand_total",
        "stripe_pid",
    )

    list_display = (
        "order_number",
        "date",
        "full_name",
        "email",
        "shipping",
        "order_total",
        "delivery_cost",
        "grand_total",
        "stripe_pid",
    )

    ordering = ("-date",)


admin.site.register(Order, OrderAdmin)

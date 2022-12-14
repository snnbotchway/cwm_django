from django.db.models import Count
from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['id', 'first_name', 'last_name',
                    'membership', 'email', 'order_count']
    list_editable = ['membership']
    list_per_page = 100
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']

    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = reverse(
            'admin:store_order_changelist') + \
            '?' + \
            'customer=' + \
            str(customer.id)
        return format_html('<a href={}>{}</a>', url, customer.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count=Count('orders'))


class InventoryListFilter(admin.SimpleListFilter):
    title = _('Inventory')
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return (
            ('<10', 'LOW'),
            ('>=10', 'OK'),
        )

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(
                inventory__lt=10,
            )
        if self.value() == '>=10':
            return queryset.filter(
                inventory__gte=10,
            )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['thumbnail']
    extra = 0
    min_num = 1
    max_num = 10

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f"<img src={instance.image.url} class='thumbnail'>")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # exclude title and slug from a product form:
    # exclude = ['title', 'slug']

    # make fields readonly with readonly_fields = ['field_name']

    # pre-populate slug field
    prepopulated_fields = {
        'slug': ['title']
    }
    # autocomplete category field so user can search for category in the form
    # help django find the category by defining search_fields in CategoryAdmin
    actions = ['clear_inventory']
    autocomplete_fields = ['category']
    search_fields = ['title__icontains']
    list_display = ['title', 'id', 'unit_price',
                    'inventory', 'inventory_status', 'category_title']
    list_editable = ['unit_price', 'inventory']
    list_select_related = ['category']
    list_filter = ['category', 'last_updated', InventoryListFilter]

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_products = queryset.update(inventory=0)
        self.message_user(request,
                          _(f'''{updated_products} product's inventory has been set to zero'''),
                          messages.SUCCESS
                          )

    @admin.display(ordering='inventory')
    def category_title(self, product):
        return product.category.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    class Media:
        css = {
            'all': ['store/styles.css']
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'product_count']
    search_fields = ['title']
    autocomplete_fields = ['featured_product']

    @admin.display(ordering='product_count')
    def product_count(self, category):
        url = reverse(
            'admin:store_product_changelist') + \
            '?' + \
            'category=' + \
            str(category.id)
        return format_html('<a href={}>{}</a>', url, category.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('products'))


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['customer', 'id', 'payment_status', 'placed_at']
    list_editable = ['payment_status']
    autocomplete_fields = ['customer']


class CartItemInline(admin.TabularInline):
    model = CartItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ['id', 'created_at']


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['product', 'quantity', 'unit_price', 'customer']
#     list_editable = ['quantity']
#     list_select_related = ['order', 'order__customer',
#                            'product']
#     autocomplete_fields = ['product']

#     @admin.display(ordering='order__customer')
#     def customer(self, order_item):
#         return order_item.order.customer

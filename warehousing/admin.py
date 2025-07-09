from django.contrib import admin, messages
from django.utils.html import format_html
from jalali_date import date2jalali

from .models import (
    QuarantineWarehouse,
    RawMaterialWarehouse,
    ProductWarehouse,
    ProductRawMaterial,
    ReturnedProduct,
    ResponsibleForTesting,
    ResponsibleForQC,
    ProductCode,
    ProductPart,
    SecondryWarehouse,
    SecondryWarehouseRawMaterial,
    ProductSecondryProduct,
    ProductDelivery,
    ProductDeliveryProduct,
    ProductDeliverySecondryProduct,
    ProductDeliveryRawMaterial,
    ReturnedFromCustomer,
    ExternalProductDelivery,
    ExternalProductDeliveryProduct,
    ExternalProductDeliverySecondryProduct,
    ExternalProductDeliveryRawMaterial,
    BorrowedProduct
)

# گروه مجاز برای افزودن داده
ALLOWED_GROUP = 'warehouse_creators'
class ReadOnlyUnlessSuperuser(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name=ALLOWED_GROUP).exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# ====== action ======
@admin.action(description="انتقال به انبار مواد اولیه")
def transfer_to_raw_material(modeladmin, request, queryset):
    transferred, skipped = 0, 0
    for item in queryset:
        if item.test_date and item.qc_date and item.destination != 'raw_material':
            RawMaterialWarehouse.objects.create(
                quarantine_reference=item,
                piece_name=item.piece_name,
                item_code=item.item_code,
                part_number=item.part_number,
                quantity=item.quantity,
                entry_date=item.exit_date or item.qc_date,
                price=item.unit_price,
                unit=item.unit,
                serial_number=item.serial_number,
                created_by=item.created_by,
            )
            item.destination = 'raw_material'
            item.save()
            transferred += 1
        else:
            skipped += 1
    if transferred:
        messages.success(request, f"{transferred} قطعه منتقل شد.")
    if skipped:
        messages.warning(request, f"{skipped} قطعه نادیده گرفته شد.")

@admin.action(description="انتقال به انبار بازگشتی‌ها")
def send_to_returned_products(modeladmin, request, queryset):
    transferred, already_returned = 0, 0
    for item in queryset:
        if item.destination != 'returned':
            ReturnedProduct.objects.create(
                piece_name=item.piece_name,
                item_code=item.item_code,
                part_number=item.part_number,
                supplier=item.supplier,
                return_date=item.exit_date or item.qc_date or item.test_date or item.entry_date,
                reason_for_return=item.qc_description or item.test_description or "نامشخص",
                price=item.unit_price,
                unit=item.unit,
                serial_number=item.serial_number,
                created_by=item.created_by,
            )
            item.destination = 'returned'
            item.save()
            transferred += 1
        else:
            already_returned += 1
    if transferred:
        messages.success(request, f"{transferred} قطعه منتقل شد.")
    if already_returned:
        messages.warning(request, f"{already_returned} قبلاً منتقل شده بودند.")

# ====== admin models======
@admin.register(QuarantineWarehouse)
class QuarantineWarehouseAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='تاریخ ورود')
    def j_entry_date(self, obj):
        return date2jalali(obj.entry_date) if obj.entry_date else "-"

    @admin.display(description='تاریخ تست')
    def j_test_date(self, obj):
        return date2jalali(obj.test_date) if obj.test_date else "-"

    @admin.display(description='تاریخ QC')
    def j_qc_date(self, obj):
        return date2jalali(obj.qc_date) if obj.qc_date else "-"

    @admin.display(description="وضعیت", ordering="status")
    def colored_status(self, obj):
        if obj.status == 'used_in_product':
            color, label = 'blue', 'استفاده شده در محصول'
        elif obj.destination == 'raw_material':
            color, label = 'green', 'منتقل شده به مواد اولیه'
        elif obj.destination == 'returned':
            color, label = 'red', 'منتقل شده به بازگشتی'
        elif not obj.test_date and not obj.qc_date:
            color, label = 'orange', 'در انتظار تست و QC'
        else:
            color, label = 'gray', 'در حال بررسی'
        return format_html('<span style="background-color:{}; color:white; padding:2px 6px; border-radius:4px;">{}</span>', color, label)

    list_display = (
        'piece_name', 'item_code', 'part_number', 'quantity',
        'j_entry_date', 'supplier', 'j_test_date', 'j_qc_date', 'destination', 'created_by', 'colored_status'
    )
    list_filter = ('piece_name', 'item_code', 'part_number', 'destination')
    search_fields = ('piece_name', 'item_code__product_code', 'part_number__product_part', 'supplier')
    ordering = ['-entry_date']
    actions = [transfer_to_raw_material, send_to_returned_products]

@admin.register(RawMaterialWarehouse)
class RawMaterialWarehouseAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='تاریخ ورود')
    def j_entry_date(self, obj):
        return date2jalali(obj.entry_date) if obj.entry_date else "-"

    list_display = (
        'piece_name', 'item_code', 'part_number', 'quantity',
        'j_entry_date', 'price', 'unit', 'serial_number', 'created_by'
    )
    list_filter = ('piece_name', 'item_code', 'part_number', 'unit')
    search_fields = ('piece_name', 'item_code__product_code', 'part_number__product_part', 'serial_number')
    ordering = ['-entry_date']

class ProductRawMaterialInline(admin.TabularInline):
    model = ProductRawMaterial
    extra = 1
    fields = ['raw_material_source', 'quantity', 'user_who_used']
    readonly_fields = [
        'raw_material_name', 'item_code', 'part_number',
        'raw_material_entry_date', 'raw_material_price',
        'unit', 'serial_number',
    ]


@admin.register(ReturnedProduct)
class ReturnedProductAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='تاریخ بازگشت')
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'piece_name', 'item_code', 'part_number',
        'j_return_date', 'supplier', 'created_by'
    )
    search_fields = ('piece_name', 'item_code__product_code', 'part_number__product_part', 'serial_number')
    ordering = ['-return_date']

@admin.register(ResponsibleForTesting)
class ResponsibleForTestingAdmin(admin.ModelAdmin):
    list_display = ('first_last_name',)
    search_fields = ('first_last_name',)

@admin.register(ResponsibleForQC)
class ResponsibleForQCAdmin(admin.ModelAdmin):
    list_display = ('first_last_name',)
    search_fields = ('first_last_name',)

@admin.register(ProductCode)
class ProductCodeAdmin(ReadOnlyUnlessSuperuser):
    list_display = ('product_code',)
    search_fields = ('product_code',)

@admin.register(ProductPart)
class ProductPartAdmin(ReadOnlyUnlessSuperuser):
    list_display = ('product_part',)
    search_fields = ('product_part',)

class SecondryWarehouseRawMaterialInline(admin.TabularInline):
    model = SecondryWarehouseRawMaterial
    extra = 1
    fields = ['raw_material_source', 'quantity', 'user_who_used']
    readonly_fields = [
        'raw_material_name', 'item_code', 'part_number',
        'raw_material_entry_date', 'raw_material_price',
        'unit', 'serial_number',
    ]
@admin.register(SecondryWarehouse)
class SecondryWarehouseAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='تاریخ شروع ساخت')
    def j_start(self, obj):
        return date2jalali(obj.manufacturing_start_date) if obj.manufacturing_start_date else "-"

    @admin.display(description='تاریخ اتمام ساخت')
    def j_end(self, obj):
        return date2jalali(obj.manufacturing_end_date) if obj.manufacturing_end_date else "-"

    @admin.display(description='تاریخ شروع تست و QC')
    def j_test_qc_start(self, obj):
        return date2jalali(obj.test_qc_start_date) if obj.test_qc_start_date else "-"

    @admin.display(description='تاریخ پایان تست و QC')
    def j_test_qc_end(self, obj):
        return date2jalali(obj.test_qc_end_date) if obj.test_qc_end_date else "-"

    @admin.display(description='تاریخ خروج محصول')
    def j_exit(self, obj):
        return date2jalali(obj.product_exit_date) if obj.product_exit_date else "-"

    list_display = (
        'product_name', 'product_serial_number',
        'j_start', 'j_end',
        'j_test_qc_start', 'j_test_qc_end',
        'j_exit', 'exit_type', 'created_by'
    )
    list_filter = ('product_name', 'product_serial_number', 'exit_type', 'created_by',)
    search_fields = ('product_name', 'product_serial_number')
    ordering = ['-manufacturing_start_date']
    inlines = [SecondryWarehouseRawMaterialInline]



class ProductSecondryProductInline(admin.TabularInline):
        model = ProductSecondryProduct
        extra = 1
        fields = ['secondry_product', 'quantity']
        # readonly_fields = ['secondry_product']


@admin.register(ProductWarehouse)
class ProductWarehouseAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='تاریخ شروع ساخت')
    def j_start(self, obj):
        return date2jalali(obj.manufacturing_start_date) if obj.manufacturing_start_date else "-"

    @admin.display(description='تاریخ اتمام ساخت')
    def j_end(self, obj):
        return date2jalali(obj.manufacturing_end_date) if obj.manufacturing_end_date else "-"

    @admin.display(description='تاریخ شروع تست و QC')
    def j_test_qc_start(self, obj):
        return date2jalali(obj.test_qc_start_date) if obj.test_qc_start_date else "-"

    @admin.display(description='تاریخ پایان تست و QC')
    def j_test_qc_end(self, obj):
        return date2jalali(obj.test_qc_end_date) if obj.test_qc_end_date else "-"

    @admin.display(description='تاریخ خروج محصول')
    def j_exit(self, obj):
        return date2jalali(obj.product_exit_date) if obj.product_exit_date else "-"

    list_display = (
        'product_name', 'product_serial_number',
        'j_start', 'j_end',
        'j_test_qc_start', 'j_test_qc_end',
        'j_exit', 'exit_type', 'created_by'
    )
    list_filter = ('exit_type',)
    search_fields = ('product_name', 'product_serial_number')
    ordering = ['-manufacturing_start_date']
    inlines = [ProductRawMaterialInline, ProductSecondryProductInline]



@admin.register(ProductDelivery)
class ProductDeliveryAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.deliverer = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="محصولات اصلی")
    def display_main_products(self, obj):
        return ", ".join([
            f"{item.product.product_name} (×{item.quantity})"
            for item in obj.product_items.all()
        ]) or "-"

    @admin.display(description="محصولات ثانویه")
    def display_secondary_products(self, obj):
        return ", ".join([
            f"{item.secondry_product.product_name} (×{item.quantity})"
            for item in obj.secondry_items.all()
        ]) or "-"

    @admin.display(description="مواد اولیه")
    def display_raw_materials(self, obj):
        return ", ".join([
            f"{item.raw_material.piece_name} (×{item.quantity})"
            for item in obj.raw_material_items.all()
        ]) or "-"

    @admin.display(description='تاریخ تحویل')
    def j_delivery_date(self, obj):
        return date2jalali(obj.delivery_date) if obj.delivery_date else "-"

    @admin.display(description='تاریخ بازگشت')
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'receiver_name',
        'j_delivery_date',
        'j_return_date',
        'deliverer',
        'display_main_products',
        'display_secondary_products',
        'display_raw_materials',
    )

    search_fields = ('receiver_name',)
    ordering = ['-delivery_date']
    inlines = [
        type('ProductDeliveryProductInline', (admin.TabularInline,), {
            'model': ProductDeliveryProduct,
            'extra': 1,
        }),
        type('ProductDeliverySecondryProductInline', (admin.TabularInline,), {
            'model': ProductDeliverySecondryProduct,
            'extra': 1,
        }),
        type('ProductDeliveryRawMaterialInline', (admin.TabularInline,), {
            'model': ProductDeliveryRawMaterial,
            'extra': 1,
        }),
    ]


class ExternalProductDeliveryProductInline(admin.TabularInline):
    model = ExternalProductDeliveryProduct
    extra = 1


class ExternalProductDeliverySecondryProductInline(admin.TabularInline):
    model = ExternalProductDeliverySecondryProduct
    extra = 1


class ExternalProductDeliveryRawMaterialInline(admin.TabularInline):
    model = ExternalProductDeliveryRawMaterial
    extra = 1


@admin.register(ExternalProductDelivery)
class ExternalProductDeliveryAdmin(ReadOnlyUnlessSuperuser):
    @admin.display(description="تاریخ تحویل")
    def j_delivery_date(self, obj):
        return date2jalali(obj.delivery_date) if obj.delivery_date else "-"

    @admin.display(description="تاریخ بازگشت")
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'receiver_name', 'j_delivery_date', 'j_return_date', 'deliverer'
    )
    search_fields = ('receiver_name',)
    ordering = ['-delivery_date']
    inlines = [
        ExternalProductDeliveryProductInline,
        ExternalProductDeliverySecondryProductInline,
        ExternalProductDeliveryRawMaterialInline
    ]




@admin.register(ReturnedFromCustomer)
class ReturnedFromCustomerAdmin(ReadOnlyUnlessSuperuser):
    @admin.display(description='تاریخ بازگشت')
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'customer_name',
        'product_name',
        'product_serial_number',
        'product_part_number',
        'product_item_code',
        'j_return_date',
        'received_by',
    )
    search_fields = ('customer_name', 'product_name', 'product_part_number', 'product_item_code', 'product_serial_number')
    list_filter = ('customer_name', 'product_name', 'product_part_number', 'product_item_code', 'product_serial_number')
    ordering = ['-return_date']



@admin.register(BorrowedProduct)
class BorrowedProductAdmin(ReadOnlyUnlessSuperuser):
    @admin.display(description="تاریخ تحویل")
    def j_delivery_date(self, obj):
        return date2jalali(obj.delivery_date) if obj.delivery_date else "-"

    @admin.display(description="تاریخ بازگرداندن")
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'product_name', 'serial_number', 'giver_company', 'receiver_person', 'j_delivery_date', 'j_return_date'
    )
    search_fields = ('product_name', 'serial_number', 'giver_company', 'receiver_person')
    ordering = ['-delivery_date']

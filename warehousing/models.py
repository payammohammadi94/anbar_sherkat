from django.db import models

# Create your models here.
from django.db import models

from django.conf import settings
# Create your models here.

class ResponsibleForTesting(models.Model):
    first_last_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی مسئول تست")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    def __str__(self):
        return f"{self.first_last_name}"

    class Meta:
        verbose_name = "مسئول تست"
        verbose_name_plural = "مسئول تست"

class ResponsibleForQC(models.Model):
    first_last_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی مسئول QC")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    def __str__(self):
        return f"{self.first_last_name}"

    class Meta:
        verbose_name = "مسئول QC"
        verbose_name_plural = "مسئول QC"

class ProductPart(models.Model):
    product_part = models.CharField(max_length=255, verbose_name="پارت کالا")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    def __str__(self):
        return f"{self.product_part}"

    class Meta:
        verbose_name = "پارت کالا"
        verbose_name_plural = "پارت کالا"

class ProductCode(models.Model):
    product_code = models.CharField(max_length=255, verbose_name="کد کالا")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    def __str__(self):
        return f"{self.product_code}"

    class Meta:
        verbose_name = "کد کالا"
        verbose_name_plural = "کد کالا"

class QuarantineWarehouse(models.Model):
    DESTINATION_CHOICES = [
    ('raw_material', 'انبار مواد اولیه'),
    ('returned', 'محصول بازگشتی'),
]
    STATUS_CHOICES = [
    ('waiting_test', 'در انتظار تست'),
    ('testing', 'در حال تست'),
    ('testing_done', 'تست شده'),
    ('qc_pending', 'در انتظار QC'),
    ('approved', 'تایید شده'),
    ('rejected', 'رد شده'),
    ('transferred', 'منتقل شده'),
    ('used_in_product', 'استفاده شده در محصول'),
    ('used_in_secondry_warehouse', 'استفاده شده در انبار ثانویه'),
]
    
    UNIT_PRICE_CHOICES = [
        ('dollar','دلار'),
        ('toman','تومان')
    ]
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    piece_name = models.CharField(max_length=255, verbose_name="نام قطعه")
    part_number = models.ForeignKey(ProductPart, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کد کالا")
    quantity = models.IntegerField(verbose_name="تعداد")
    entry_date = models.DateField(verbose_name="تاریخ ورود")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت (واحد)")
    unit = models.CharField(max_length=50, verbose_name="واحد", choices=UNIT_PRICE_CHOICES)
    supplier = models.CharField(max_length=255, verbose_name="تامین کننده")
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='waiting_test', verbose_name="وضعیت قطعه")
    test_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تست")
    test_responsible = models.ForeignKey(ResponsibleForTesting,blank=True, null=True, verbose_name="مسئول تست",on_delete=models.SET_NULL,)
    # test_responsible = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسئول تست")
    test_description = models.TextField(blank=True, null=True, verbose_name="شرح تست")
    qc_date = models.DateField(blank=True, null=True, verbose_name="تاریخ QC")
    qc_responsible = models.ForeignKey(ResponsibleForQC,blank=True, null=True, verbose_name="مسئول QC", on_delete=models.SET_NULL,)
    # qc_responsible = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسئول QC")
    qc_description = models.TextField(blank=True, null=True, verbose_name="شرح QC")
    exit_date = models.DateField(blank=True, null=True, verbose_name="تاریخ خروج")
    destination = models.CharField(max_length=50, choices=DESTINATION_CHOICES, blank=True, null=True, verbose_name="مقصد")


    def __str__(self):
        return f"{self.piece_name} ({self.item_code})"

    class Meta:
        verbose_name = "موجودیت انبار قرنطینه"
        verbose_name_plural = "انبار قرنطینه"

class RawMaterialWarehouse(models.Model):
    UNIT_PRICE_CHOICES = [
        ('dollar','دلار'),
        ('toman','تومان')
    ]
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    quarantine_reference = models.ForeignKey(QuarantineWarehouse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ارجاع به قرنطینه")
    piece_name = models.CharField(max_length=255, verbose_name="نام قطعه")
    part_number = models.ForeignKey(ProductPart, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کد کالا")
    quantity = models.IntegerField(verbose_name="تعداد")
    entry_date = models.DateField(verbose_name="تاریخ ورود")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    unit = models.CharField(max_length=50, verbose_name="واحد",choices=UNIT_PRICE_CHOICES)
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")

    def __str__(self):
        return f"{self.piece_name} - {self.serial_number} - {self.item_code} - {self.part_number}"

    class Meta:
        verbose_name = "موجودیت انبار مواد اولیه"
        verbose_name_plural = "انبار مواد اولیه"

class ProductWarehouse(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    product_name = models.CharField(max_length=255, verbose_name="محصول")
    product_serial_number = models.CharField(max_length=255, unique=True, verbose_name="شماره سریال محصول")
    manufacturing_start_date = models.DateField(verbose_name="تاریخ شروع ساخت")
    manufacturing_end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ اتمام ساخت")
    test_qc_start_date = models.DateField(blank=True, null=True, verbose_name="تاریخ شروع تست و QC")
    test_qc_end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پایان تست و QC")
    test_approver = models.CharField(max_length=255, blank=True, null=True, verbose_name="تایید کننده تست")
    qc_responsible = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسئول QC")
    product_exit_date = models.DateField(blank=True, null=True, verbose_name="تاریخ خروج محصول")
    exit_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="نوع خروج")
    deliverer = models.CharField(max_length=255, blank=True, null=True, verbose_name="تحویل دهنده")
    receiver = models.CharField(max_length=255, blank=True, null=True, verbose_name="تحویل گیرنده")
    finished_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="قیمت تمام شده")

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "موجودیت انبار محصولات"
        verbose_name_plural = "انبار محصولات"

class ReturnedProduct(models.Model):
    UNIT_PRICE_CHOICES = [
        ('dollar','دلار'),
        ('toman','تومان')
    ]
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    piece_name = models.CharField(max_length=255, verbose_name="نام قطعه")
    part_number = models.ForeignKey(ProductPart, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کد کالا")
    supplier = models.CharField(max_length=255, blank=True, null=True, verbose_name="تامین کننده")
    return_date = models.DateField(verbose_name="تاریخ بازگشت")
    reason_for_return = models.TextField(verbose_name="دلیل بازگشت")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="قیمت")
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name="واحد", choices=UNIT_PRICE_CHOICES)
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")

    def __str__(self):
        return f"بازگشتی: {self.piece_name} ({self.item_code})"

    class Meta:
        verbose_name = "محصول برگشتی به فروشنده"
        verbose_name_plural = "محصولات برگشتی به فروشنده"

class ProductRawMaterial(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    product = models.ForeignKey(ProductWarehouse, on_delete=models.CASCADE, related_name='raw_materials', verbose_name="محصول")
    raw_material_source = models.ForeignKey(
        RawMaterialWarehouse, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="انتخاب از انبار مواد اولیه"
    )
    raw_material_name = models.CharField(max_length=255, verbose_name="ماده اولیه")
    part_number = models.ForeignKey(ProductPart, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کد کالا")
    quantity = models.IntegerField(verbose_name="مقدار")
    user_who_used = models.CharField(max_length=255, verbose_name="استفاده کننده")
    raw_material_entry_date = models.DateField(verbose_name="تاریخ ورود ماده اولیه")
    raw_material_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت ماده اولیه")
    unit = models.CharField(max_length=50, verbose_name="واحد", choices=[
        ('dollar', 'دلار'),
        ('toman', 'تومان')
    ])
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")

    def save(self, *args, **kwargs):
        raw = self.raw_material_source
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = ProductRawMaterial.objects.get(pk=self.pk)

            if old.raw_material_source == self.raw_material_source:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if raw and raw.quantity >= diff:
                        raw.quantity -= diff
                        raw.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if raw:
                        raw.quantity += abs(diff)
                        raw.save()
            else:
                # منبع تغییر کرده
                if old.raw_material_source:
                    old.raw_material_source.quantity += old.quantity
                    old.raw_material_source.save()
                if raw:
                    if raw.quantity >= self.quantity:
                        raw.quantity -= self.quantity
                        raw.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if raw:
                if raw.quantity >= self.quantity:
                    raw.quantity -= self.quantity
                    raw.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # پر کردن اطلاعات از منبع در صورت خالی بودن
        if raw and not self.raw_material_name:
            self.raw_material_name = raw.piece_name
            self.item_code = raw.item_code
            self.part_number = raw.part_number
            self.raw_material_entry_date = raw.entry_date
            self.raw_material_price = raw.price
            self.unit = raw.unit
            self.serial_number = raw.serial_number

        # وضعیت قرنطینه
        if raw and raw.quarantine_reference:
            print(raw.quarantine_reference.status)
            raw.quarantine_reference.status = 'used_in_product'
            print(raw.quarantine_reference.status)
            raw.quarantine_reference.save()

        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if self.raw_material_source:
            self.raw_material_source.quantity += self.quantity
            self.raw_material_source.save()

            # بازگرداندن وضعیت قرنطینه اگر دیگر استفاده نشده باشد
            quarantine_ref = self.raw_material_source.quarantine_reference
            if quarantine_ref:
                others = ProductRawMaterial.objects.filter(
                    raw_material_source=self.raw_material_source
                ).exclude(pk=self.pk)

                if not others.exists():
                    quarantine_ref.status = 'transferred'
                    quarantine_ref.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.raw_material_name} for {self.product.product_name}"

    class Meta:
        verbose_name = "ماده اولیه محصول"
        verbose_name_plural = "مواد اولیه محصول"

class SecondryWarehouse(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    product_name = models.CharField(max_length=255, verbose_name="محصول ثانویه")
    product_serial_number = models.CharField(max_length=255, unique=True, verbose_name="شماره سریال محصول ثانویه")
    manufacturing_start_date = models.DateField(verbose_name="تاریخ شروع ساخت")
    manufacturing_end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ اتمام ساخت")
    test_qc_start_date = models.DateField(blank=True, null=True, verbose_name="تاریخ شروع تست و QC")
    test_qc_end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پایان تست و QC")
    test_approver = models.CharField(max_length=255, blank=True, null=True, verbose_name="تایید کننده تست")
    qc_responsible = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسئول QC")
    product_exit_date = models.DateField(blank=True, null=True, verbose_name="تاریخ خروج محصول")
    exit_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="نوع خروج")
    deliverer = models.CharField(max_length=255, blank=True, null=True, verbose_name="تحویل دهنده")
    receiver = models.CharField(max_length=255, blank=True, null=True, verbose_name="تحویل گیرنده")
    finished_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="قیمت تمام شده")

    def __str__(self):
        return f"{self.product_name} - {self.product_serial_number}"

    class Meta:
        verbose_name = "انبار ثانویه"
        verbose_name_plural = "انبار ثانویه"

class SecondryWarehouseRawMaterial(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ایجادکننده"
    )
    secondryWarehouse = models.ForeignKey(SecondryWarehouse, on_delete=models.CASCADE, related_name='raw_materials', verbose_name="محصول انبار ثانویه")
    raw_material_source = models.ForeignKey(
        RawMaterialWarehouse, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="انتخاب از انبار مواد اولیه"
    )
    raw_material_name = models.CharField(max_length=255, verbose_name="ماده اولیه", null=True, blank=True)
    part_number = models.ForeignKey(ProductPart, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="پارت کالا")
    item_code = models.ForeignKey(ProductCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کد کالا")
    serial_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="شماره سریال")
    quantity = models.IntegerField(verbose_name="مقدار")
    user_who_used = models.CharField(blank=True, null=True, max_length=255, verbose_name="استفاده کننده")
    raw_material_entry_date = models.DateField(verbose_name="تاریخ ورود ماده اولیه", null=True, blank=True)
    raw_material_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت ماده اولیه", null=True, blank=True)
    unit = models.CharField(max_length=50, verbose_name="واحد", choices=[
        ('dollar', 'دلار'),
        ('toman', 'تومان')
    ], null=True, blank=True)

    def save(self, *args, **kwargs):
        raw = self.raw_material_source
        # بررسی اینکه رکورد جدید است یا ویرایش شده
        if self.pk:
            old = SecondryWarehouseRawMaterial.objects.get(pk=self.pk)

            if old.raw_material_source == self.raw_material_source:
                diff = self.quantity - old.quantity

                if diff > 0:  # افزایش مصرف
                    if raw and raw.quantity >= diff:
                        raw.quantity -= diff
                        raw.save()
                    else:
                        raise ValueError("مقدار جدید بیشتر از موجودی انبار است.")
                elif diff < 0:  # کاهش مصرف
                    if raw:
                        raw.quantity += abs(diff)
                        raw.save()
            else:
                # منبع تغییر کرده
                if old.raw_material_source:
                    old.raw_material_source.quantity += old.quantity
                    old.raw_material_source.save()
                if raw:
                    if raw.quantity >= self.quantity:
                        raw.quantity -= self.quantity
                        raw.save()
                    else:
                        raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")
        else:
            # رکورد جدید است
            if raw:
                if raw.quantity >= self.quantity:
                    raw.quantity -= self.quantity
                    raw.save()
                else:
                    raise ValueError("مقدار وارد شده بیشتر از موجودی انبار است.")

        # پر کردن اطلاعات از منبع در صورت خالی بودن
        if raw and not self.raw_material_name:
            self.raw_material_name = raw.piece_name
            self.item_code = raw.item_code
            self.part_number = raw.part_number
            self.raw_material_entry_date = raw.entry_date
            self.raw_material_price = raw.price
            self.unit = raw.unit
            self.serial_number = raw.serial_number

        # وضعیت قرنطینه
        if raw and raw.quarantine_reference:     
            raw.quarantine_reference.status = 'used_in_secondry_warehouse'
            raw.quarantine_reference.save()

        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if self.raw_material_source:
            self.raw_material_source.quantity += self.quantity
            self.raw_material_source.save()

            # بازگرداندن وضعیت قرنطینه اگر دیگر استفاده نشده باشد
            quarantine_ref = self.raw_material_source.quarantine_reference
            if quarantine_ref:
                others = SecondryWarehouseRawMaterial.objects.filter(
                    raw_material_source=self.raw_material_source
                ).exclude(pk=self.pk)

                if not others.exists():
                    quarantine_ref.status = 'transferred'
                    quarantine_ref.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.raw_material_name} for {self.secondryWarehouse.product_name}"

    class Meta:
        verbose_name = "مواد اولیه انبار ثانویه"
        verbose_name_plural = "مواد اولیه انبار ثانویه"

class ProductSecondryProduct(models.Model):
    product = models.ForeignKey(
        'ProductWarehouse',
        on_delete=models.CASCADE,
        related_name='secondry_products',
        verbose_name="محصول نهایی"
    )
    secondry_product = models.ForeignKey(
        SecondryWarehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="محصول ثانویه مصرف‌شده"
    )
    quantity = models.IntegerField(verbose_name="تعداد مصرف‌شده از محصول ثانویه")

    def __str__(self):
        return f"{self.secondry_product} در {self.product}"

    class Meta:
        verbose_name = "محصول ثانویه در محصول نهایی"
        verbose_name_plural = "محصولات ثانویه در محصول نهایی"

class ProductDelivery(models.Model):
    receiver_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی تحویل گیرنده")
    user_name = models.CharField(blank=True, null=True,max_length=255, verbose_name="شناسه کاربری تحویل گیرنده")
    delivery_date = models.DateField(verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")
    deliverer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="تحویل دهنده"
    )

    def __str__(self):
        return f"{self.receiver_name} - {self.delivery_date}"

    class Meta:
        verbose_name = "تحویل محصول به افراد داخل شرکت"
        verbose_name_plural = "تحویل محصولات به افراد داخل شرکت"

class ProductDeliveryProduct(models.Model):
    delivery = models.ForeignKey(ProductDelivery, on_delete=models.CASCADE, related_name="product_items")
    product = models.ForeignKey(ProductWarehouse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="محصول")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ برگشت")

class ProductDeliverySecondryProduct(models.Model):
    delivery = models.ForeignKey(ProductDelivery, on_delete=models.CASCADE, related_name="secondry_items")
    secondry_product = models.ForeignKey(SecondryWarehouse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="محصول ثانویه")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ برگشت")

class ProductDeliveryRawMaterial(models.Model):
    delivery = models.ForeignKey(ProductDelivery, on_delete=models.CASCADE, related_name="raw_material_items")
    raw_material = models.ForeignKey(RawMaterialWarehouse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ماده اولیه")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ برگشت")

class ExternalProductDelivery(models.Model):
    receiver_name = models.CharField(max_length=255, verbose_name="تحویل گیرنده (خارج از شرکت)")
    delivery_date = models.DateField(verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")
    deliverer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="تحویل دهنده"
    )

    def __str__(self):
        return f"{self.receiver_name} - {self.delivery_date}"

    class Meta:
        verbose_name = "تحویل محصول به خارج از شرکت"
        verbose_name_plural = "تحویل محصولات به خارج از شرکت"

class ExternalProductDeliveryProduct(models.Model):
    delivery = models.ForeignKey(ExternalProductDelivery, on_delete=models.CASCADE, related_name="product_items")
    product = models.ForeignKey(ProductWarehouse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="محصول")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True,verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")

class ExternalProductDeliverySecondryProduct(models.Model):
    delivery = models.ForeignKey(ExternalProductDelivery, on_delete=models.CASCADE, related_name="secondry_items")
    secondry_product = models.ForeignKey(SecondryWarehouse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="محصول ثانویه")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True,verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")

class ExternalProductDeliveryRawMaterial(models.Model):
    delivery = models.ForeignKey(ExternalProductDelivery, on_delete=models.CASCADE, related_name="raw_material_items")
    raw_material = models.ForeignKey(RawMaterialWarehouse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ماده اولیه")
    quantity = models.IntegerField(verbose_name="تعداد")
    delivery_date = models.DateField(blank=True, null=True,verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگشت")

class ReturnedFromCustomer(models.Model):
    customer_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی کارفرما")
    product_name = models.CharField(max_length=255, verbose_name="نام محصول برگشتی")
    product_serial_number = models.CharField(max_length=255, verbose_name="شماره سریال محصول")
    product_part_number = models.CharField(max_length=255, verbose_name="پارت کالا",null=True,blank=True)
    product_item_code = models.CharField(max_length=255, verbose_name="کد کالا",null=True,blank=True)
    return_reason = models.TextField(verbose_name="دلیل برگشت")
    return_date = models.DateField(verbose_name="تاریخ بازگشت")
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="تحویل گیرنده"
    )

    def __str__(self):
        return f"{self.product_name} - {self.customer_name}"

    class Meta:
        verbose_name = "محصول برگشتی از کارفرما"
        verbose_name_plural = "محصولات برگشتی از کارفرما"
    
class BorrowedProduct(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="نام محصول")
    serial_number = models.CharField(max_length=255, verbose_name="شماره سریال محصول")
    giver_company = models.CharField(max_length=255, verbose_name="تحویل دهنده (شرکت دیگر)")
    receiver_person = models.CharField(max_length=255, verbose_name="تحویل گیرنده (داخل شرکت)")
    delivery_date = models.DateField(verbose_name="تاریخ تحویل")
    return_date = models.DateField(blank=True, null=True, verbose_name="تاریخ بازگرداندن")

    def __str__(self):
        return f"{self.product_name} - {self.serial_number}"

    class Meta:
        verbose_name = "محصول امانتی از شرکت دیگر"
        verbose_name_plural = "محصولات امانتی از شرکت‌های دیگر"

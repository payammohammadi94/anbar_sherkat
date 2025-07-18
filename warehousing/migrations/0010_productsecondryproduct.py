# Generated by Django 5.1.7 on 2025-07-09 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehousing', '0009_secondrywarehouse_secondrywarehouserawmaterial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSecondryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='تعداد مصرف\u200cشده از محصول ثانویه')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondry_products', to='warehousing.productwarehouse', verbose_name='محصول نهایی')),
                ('secondry_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehousing.secondrywarehouse', verbose_name='محصول ثانویه مصرف\u200cشده')),
            ],
            options={
                'verbose_name': 'محصول ثانویه در محصول نهایی',
                'verbose_name_plural': 'محصولات ثانویه در محصول نهایی',
            },
        ),
    ]

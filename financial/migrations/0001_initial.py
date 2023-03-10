# Generated by Django 4.1.7 on 2023-02-24 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0002_alter_product_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='کد  تخفیفی که کاربر باید وارد کند همین شناسه است و توجه داشته باشید به صورت متن و عدد باشد و عدد نمی تواند در ابتدا قرار بگیرد', max_length=255, unique=True, verbose_name='شناسه')),
                ('count', models.PositiveIntegerField(verbose_name='تعداد مجاز استفاده')),
                ('count_use', models.PositiveIntegerField(default=0, verbose_name='تعداد استفاده شده')),
                ('start', models.DateField(auto_now_add=True, verbose_name='تاریخ شروع')),
                ('end', models.DateField(blank=True, null=True, verbose_name='تاریخ انقضا')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('offer_price', models.CharField(default='0', max_length=11, verbose_name='مبلغ تخفیف')),
                ('active', models.BooleanField(default=True, verbose_name='وضعیت انتشار')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Item_offer', to='shop.product', verbose_name='آیتم')),
                ('users', models.ManyToManyField(blank=True, related_name='offer_users_item', to=settings.AUTH_USER_MODEL, verbose_name='کاربران')),
            ],
            options={
                'verbose_name': 'تخفیف',
                'verbose_name_plural': 'تخفیف ها',
                'ordering': ('id', 'created_date', 'slug'),
            },
        ),
        migrations.CreateModel(
            name='User_factor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.JSONField(default={'data': []}, verbose_name='آیتم ها')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('payment_status', models.CharField(choices=[('0', 'منتظر پرداخت'), ('1', 'منتظر تایید رسید'), ('2', 'پرداخت شده')], default='0', max_length=1, verbose_name='وضعیت پرداخت')),
                ('payment_date', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')),
                ('payment_method', models.CharField(choices=[('0', 'پرداخت نشده'), ('1', 'پرداخت با فیش واریز'), ('2', 'پرداخت اینترنتی'), ('3', 'پرداخت حضوری با دستگاه'), ('4', 'پرداخت حضوری نقد')], default='0', max_length=1, verbose_name='شیوه پرداخت')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/financial/factors/', verbose_name='تصویر رسید')),
                ('address', models.TextField(blank=True, null=True, verbose_name='آدرس')),
                ('msg', models.TextField(blank=True, null=True, verbose_name='متن ارسالی بعد از ثبت نهایی')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('fk_offer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_factor_item', to='financial.user_offer', verbose_name='کد تخفیف')),
                ('fk_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_item_factor', to=settings.AUTH_USER_MODEL, verbose_name='کاربر فاکتور')),
            ],
            options={
                'verbose_name': 'فاکتور',
                'verbose_name_plural': 'فاکتور ها',
                'ordering': ('id', 'created_date'),
            },
        ),
    ]

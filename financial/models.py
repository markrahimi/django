from django.db import models
from account.models import CustomUser
from shop.models import product
import json
# ---------------------------------------
# user_offer Model
# ---------------------------------------
class user_offer(models.Model):
    slug = models.SlugField(verbose_name='شناسه',max_length=255,unique=True, help_text="کد  تخفیفی که کاربر باید وارد کند همین شناسه است و توجه داشته باشید به صورت متن و عدد باشد و عدد نمی تواند در ابتدا قرار بگیرد")
    item = models.ForeignKey(product, verbose_name='آیتم', related_name='Item_offer', on_delete=models.SET_NULL, null=True, blank=True)
    count = models.PositiveIntegerField(verbose_name='تعداد مجاز استفاده')
    count_use = models.PositiveIntegerField(verbose_name='تعداد استفاده شده', default=0)
    start = models.DateField(verbose_name='تاریخ شروع',auto_now_add=True)
    end = models.DateField(verbose_name='تاریخ انقضا', blank=True, null=True)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    offer_price = models.CharField(verbose_name='مبلغ تخفیف', max_length=11, default='0') 
    users = models.ManyToManyField(CustomUser, verbose_name='کاربران', related_name='offer_users_item', blank=True)
    active = models.BooleanField(verbose_name='وضعیت انتشار', default=True)
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت',auto_now_add=True)

    def __str__(self):
        return "{}".format(self.slug)

    class Meta:
        ordering = ('id', 'created_date', 'slug')
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'


# ---------------------------------------
# User_factor Model
# ---------------------------------------
item_default = {
    "data" : [],
}
class User_factor(models.Model):
    fk_user = models.ForeignKey(CustomUser, verbose_name='کاربر فاکتور',related_name='user_item_factor', blank=True, null=True, on_delete=models.SET_NULL)
    items = models.JSONField(verbose_name='آیتم ها',default=item_default)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    STATUS_ITEMS = (
        ('0', 'منتظر پرداخت'),
        ('1', 'منتظر تایید رسید'),
        ('2', 'پرداخت شده'),
    )
    payment_status = models.CharField(verbose_name='وضعیت پرداخت', max_length=1, choices=STATUS_ITEMS,default='0')
    payment_date = models.DateTimeField(verbose_name='تاریخ پرداخت',null=True,blank=True)
    METHOD_ITEMS = (
        ('0', 'پرداخت نشده'),
        ('1', 'پرداخت با فیش واریز'),
        ('2', 'پرداخت اینترنتی'),
        ('3', 'پرداخت حضوری با دستگاه'),
        ('4', 'پرداخت حضوری نقد'),
    )
    payment_method = models.CharField(verbose_name='شیوه پرداخت', max_length=1, choices=METHOD_ITEMS,default='0')
    image = models.ImageField(verbose_name='تصویر رسید', upload_to='media/financial/factors/', blank=True, null=True)
    fk_offer = models.ForeignKey(user_offer, verbose_name='کد تخفیف',related_name='offer_factor_item', blank=True, null=True, on_delete=models.SET_NULL)
    address = models.TextField(verbose_name='آدرس', blank=True, null=True)
    msg = models.TextField(verbose_name='متن ارسالی بعد از ثبت نهایی', blank=True, null=True)
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)

    def __str__(self):
        return "{}, {}".format(self.id, self.payment_method)

    def get_total_price(self):
        try:
            total_price = 0
            data = self.items['data']
            for i in data:
                i = json.loads(i)
                if self.fk_offer == None :
                    price = int(i['price'])
                    count = int(i['count'])
                    item_total = price * count
                    total_price = total_price + item_total
                else : 
                    offer = user_offer.objects.get(id=self.fk_offer.id)
                    total_price += int(offer.offer_price)
            return int(total_price)
        except Exception as e :
            return e

    def auto_update_item(self):
        data = self.items['data']
        new_data = []
        for i in data:
            i = json.loads(i)
            itemObj = product.objects.get(id = int(i['id']))
            if int(itemObj.capacity) >= int(i['count']):
                i['price'] = itemObj.price
                i = json.dumps(i)
                new_data.append(i)

        self.items['data'] = new_data
        self.save()

    def add_item(self,item,price,count):
        # items = {'item_list': []}
        self.auto_update_item()
        data = self.items['data']
        new_data = []

        find = False
        for i in data:
            i = json.loads(i)
            if int(i['id']) == int(item):
                itemObj = product.objects.get(id = int(i['id']))
                if itemObj.one_pay :
                    i['count'] = 1
                else:
                    i['count'] = int(i['count']) + int(count)
                find = True
            i = json.dumps(i)
            new_data.append(i)
        self.items['data'] = new_data

        if find == False:
            itemJson = {
                "id" : item,
                "price" : price,
                "count" : count,
            }
            itemJson = json.dumps(itemJson)
            self.items['data'].append(itemJson)
        self.save()

    def remove_item(self,item):
        self.auto_update_item()
        data = self.items['data']
        new_data = []

        for i in data:
            i = json.loads(i)
            if int(i['id']) != int(item):
                new_data.append(i)
        self.items['data'] = new_data
        self.save()

    def minus_item(self,item):
        # items = {'item_list': []}
        self.auto_update_item()
        data = self.items['data']
        new_data = []

        for i in data:
            i = json.loads(i)
            if i['id'] == item:
                if int(i['count']) != 1 :
                    i['count'] = int(i['count']) - 1
                    new_data.append(i)
        self.items['data'] = new_data
        self.save()

    def need_addres(self):
        # items = {'item_list': []}
        self.auto_update_item()
        data = self.items['data']
        need = False
        for i in data:
            i = json.loads(i)
            itemObj = Items.objects.get(id = int(i['id']))
            if itemObj.address_require :
                need = True
        return need

    def show_items(self):
        # items = {'item_list': []}
        self.auto_update_item()
        data = self.items['data']
        new_data = []

        for i in data:
            i = json.loads(i)
            itemObj = product.objects.get(id =int(i['id']))
            i['id'] = itemObj.title
            new_data.append(i)
        return new_data

    def get_code(self):
        code = str(self.id)
        lengthID = len(code)
        return code.zfill(10 - lengthID)

    class Meta:
        ordering = ('id', 'created_date')
        verbose_name = 'فاکتور'
        verbose_name_plural = 'فاکتور ها'

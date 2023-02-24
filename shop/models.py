from django.db import models
from account.models import *

from django.utils.deconstruct import deconstructible
from datetime import datetime

from django_quill.fields import QuillField

# ---------------------------------------
# attribute Model
# ---------------------------------------
class attribute_product(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=255)
    unit=models.CharField(verbose_name='واحد ویژگی', max_length=127,null=True, blank=True)  
    active = models.BooleanField(verbose_name='وضعیت', default=True)
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)
    def __str__(self):
        return "{}".format(self.title,)
    class Meta:
        ordering = ('id', 'title')
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی  ها'


# ---------------------------------------
# product_category Model
# ---------------------------------------
class product_category(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=255)
    active = models.BooleanField(verbose_name='وضعیت', default=True)
    FK_category=models.ForeignKey('product_category',related_name='parent_category', on_delete=models.SET_NULL, verbose_name='دسته بندی والد', blank=True, null=True)
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)
    def __str__(self):
        return "{}".format(self.title,)
    
    def children(self):
        """Return replies of a comment."""
        return product_category.objects.filter(FK_category=self,active=True)

    class Meta:
        ordering = ('id', 'title')
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


# ---------------------------------------
# product Model
# ---------------------------------------
class product(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=255)
    image = models.ImageField(verbose_name='عکس اصلی', upload_to='media/blog/post/',
                                 default='static/post/default.jpg')
    header_img = models.ImageField(verbose_name='عکس', upload_to='media/blog/post/',
                                 default='static/post/default.jpg')
    text = QuillField(verbose_name='متن',null=True, blank=True)
    FK_category=models.ForeignKey(product_category,related_name='blog_category', on_delete=models.SET_NULL, verbose_name='دسته بندی', blank=True, null=True)
    pin = models.BooleanField(verbose_name='پین بودن', default=False)
    homeshow = models.BooleanField(verbose_name='نمایش در صفحه اصلی', default=False)
    my_order = models.PositiveIntegerField(
        verbose_name='ترتیب نمایش',
        default=0,
        blank=False,
        null=False,
    )
    price = models.BigIntegerField(verbose_name='قیمت', blank=True, null=True)
    active = models.BooleanField(verbose_name='وضعیت', default=True)
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)
    def __str__(self):
        return "{}".format(self.title,)

    def price_ok(self):
        p_new = self.price
        p_new = f'{p_new:,}'  
        return  p_new

    def attribute_list(self):
        attr_list = attr_product.objects.filter(FK_product=self)
        return attr_list

    def related_product(self):
        rel = product.objects.filter(FK_category = self.FK_category,FK_category_section = self.FK_category_section )[6]
        return rel


    class Meta:
        ordering = ['my_order']
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


# ---------------------------------------
# attr_product Model
# ---------------------------------------
class attr_product(models.Model):
    FK_product = models.ForeignKey(product, null=True, on_delete=models.SET_NULL, verbose_name='محصول', related_name='product_attr_part')
    FK_attribute = models.ForeignKey(attribute_product, null=True, on_delete=models.SET_NULL, verbose_name='نام ویژگی', related_name='attr_list_part')
    value = models.CharField(verbose_name='مقدار ویژگی', max_length=63)
    
    def __str__(self):
        return "{}".format(self.value)

    # Get Data - Attribute Title
    def get_attribute_title(self):
        return self.FK_attribute.title
    
    # Get Data - Attribute Unit
    def get_attribute_unit(self):
        return self.FK_attribute.unit

    # Ordering With DateCreate
    class Meta:
        verbose_name = "مقدار ویژگی"
        verbose_name_plural = "مقدار ویژگی ها"

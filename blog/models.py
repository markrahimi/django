from django.db import models
from account.models import CustomUser

from django.utils.deconstruct import deconstructible
from datetime import datetime

from django_quill.fields import QuillField

# ---------------------------------------
# category_blog Model
# ---------------------------------------
class category_blog(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=255)
    active = models.BooleanField(verbose_name='وضعیت', default=True)
    FK_category=models.ForeignKey('category_blog',related_name='parent_category', on_delete=models.SET_NULL, verbose_name='دسته بندی والد', blank=True, null=True)
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)
    def __str__(self):
        return "{}".format(self.title,)
    
    def children(self):
        """Return replies of a comment."""
        return category_blog.objects.filter(FK_category=self,active=True)

    class Meta:
        ordering = ('id', 'title')
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


# ---------------------------------------
# post_blog Model
# ---------------------------------------
class post_blog(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=255)
    image = models.ImageField(verbose_name='عکس اصلی', upload_to='media/blog/post/',
                                 default='static/post/default.jpg')
    header_img = models.ImageField(verbose_name='عکس', upload_to='media/blog/post/',
                                 default='static/post/default.jpg')
    text = QuillField(verbose_name='متن',null=True, blank=True)
    FK_category=models.ForeignKey(category_blog,related_name='blog_category', on_delete=models.SET_NULL, verbose_name='دسته بندی', blank=True, null=True)
    pin = models.BooleanField(verbose_name='پین بودن', default=False)
    homeshow = models.BooleanField(verbose_name='نمایش در صفحه اصلی', default=False)
    active = models.BooleanField(verbose_name='وضعیت', default=True)
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)
    def __str__(self):
        return "{}".format(self.title,)

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'نوشته ها'

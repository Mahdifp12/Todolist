from django.db import models
from django.urls import reverse
from slugify import slugify

from user_app.models import User


# Create your models here.

class ItemTodo(models.Model):
    title = models.CharField(max_length=250, verbose_name="عنوان")
    description = models.TextField(verbose_name="متن توصیف")
    completed = models.BooleanField(default=False, verbose_name="تکمیل شده")
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کاربر")
    slug = models.SlugField(db_index=True, max_length=200, unique=True, null=True, blank=True,
                            verbose_name="عنوان در url")

    class Meta:
        verbose_name = "آیتم تودو"
        verbose_name_plural = "آیتم های تودو"
        ordering = ['created_date']

    def get_absolute_url(self):
        return reverse('todo-detail-page', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, separator='-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

from django.db import models


# Create your models here.

class ItemTodo(models.Model):
    title = models.CharField(max_length=250, verbose_name="عنوان")
    description = models.TextField(verbose_name="متن توصیف")
    completed = models.BooleanField(default=False, verbose_name="تکمیل شده")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "آیتم تودو"
        verbose_name_plural = "آیتم های تودو"

    def __str__(self):
        return self.title

# Generated by Django 3.2.9 on 2021-12-14 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("commerce_api", "0003_auto_20211202_1112"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="books_category",
                to="commerce_api.category",
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="books_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

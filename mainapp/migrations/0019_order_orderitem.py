# Generated by Django 4.0.6 on 2022-07-28 04:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0018_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('total_price', models.IntegerField()),
                ('payment_mode', models.CharField(max_length=150, null=True)),
                ('payment_id', models.CharField(max_length=150, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Out for shipping', 'Out for shipping'), ('Completed', 'Completed')], default='Pending', max_length=150)),
                ('message', models.TextField(null=True)),
                ('tracking_num', models.CharField(max_length=150, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
            ],
        ),
    ]

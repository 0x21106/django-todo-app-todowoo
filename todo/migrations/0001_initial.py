# Generated by Django 3.0.7 on 2020-06-21 01:54

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Materiality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('color', colorfield.fields.ColorField(blank=True, default='#4FE152', max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('note', models.TextField(blank=True)),
                ('isActive', models.BooleanField(blank=True, default=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('lastModified', models.DateField(auto_now=True)),
                ('dateCompleted', models.DateField(null=True)),
                ('materiality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.Materiality')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

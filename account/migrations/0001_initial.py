# Generated by Django 3.1 on 2021-04-04 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, primary_key=True, serialize=False)),
                ('nik_name', models.SlugField(blank=True, max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('activation_code', models.CharField(blank=True, max_length=15)),
                ('status', models.CharField(choices=[('CS', 'Customer'), ('MS', 'Master')], default='CS', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

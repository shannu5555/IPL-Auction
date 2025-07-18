# Generated by Django 4.2.7 on 2023-11-29 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iplauction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='team_pics/')),
            ],
        ),
    ]

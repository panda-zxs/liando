# Generated by Django 2.2.2 on 2019-07-17 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('first_id', models.CharField(max_length=20, null=True)),
                ('second_id', models.CharField(max_length=20, null=True)),
                ('grade', models.CharField(max_length=5, null=True)),
            ],
            options={
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('tax', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('revenue', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('staff_num', models.IntegerField(null=True)),
                ('profit', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('statistic_time', models.DateField(null=True)),
                ('established_time', models.DateField(null=True)),
                ('parent', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('first_id', models.IntegerField(null=True)),
                ('grade', models.SmallIntegerField(null=True)),
            ],
            options={
                'db_table': 'industry',
            },
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='area_relate', to='watch_tower.Area')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_relate', to='watch_tower.Company')),
                ('industry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='industry_relate', to='watch_tower.Industry')),
            ],
            options={
                'db_table': 'relation',
            },
        ),
    ]
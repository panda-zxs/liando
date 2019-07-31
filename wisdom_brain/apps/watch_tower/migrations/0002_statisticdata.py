# Generated by Django 2.2.2 on 2019-07-18 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watch_tower', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_number', models.IntegerField(help_text='企业数量')),
                ('company_increase', models.IntegerField(help_text='相较于去年，企业新增数量')),
                ('date', models.CharField(help_text='统计年份', max_length=10)),
                ('revenue', models.DecimalField(decimal_places=4, help_text='营收', max_digits=20)),
                ('revenue_increase', models.DecimalField(decimal_places=4, help_text='相较于去年，营收新增额', max_digits=20)),
                ('tax', models.DecimalField(decimal_places=4, help_text='税收', max_digits=20)),
                ('tax_increase', models.DecimalField(decimal_places=4, help_text='相较于去年，税收新增', max_digits=20)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='watch_tower.Area')),
                ('industry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='watch_tower.Industry')),
            ],
            options={
                'db_table': 'statistic_data',
            },
        ),
    ]

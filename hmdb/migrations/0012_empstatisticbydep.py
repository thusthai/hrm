# Generated by Django 4.1.3 on 2023-09-22 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hmdb', '0011_timemast_tblshift_shift_cross_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='empstatisticbydep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workdate', models.CharField(blank=True, max_length=20, null=True)),
                ('n_work', models.IntegerField()),
                ('n_leave', models.IntegerField()),
                ('n_absent', models.IntegerField()),
                ('n_late', models.IntegerField()),
                ('dayofweek', models.CharField(blank=True, max_length=20, null=True)),
                ('dep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmdb.tbldepartment')),
                ('emp_type', models.ForeignKey(blank=True, db_column='emp_type', max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, to='hmdb.employeetype', to_field='cde')),
            ],
        ),
    ]

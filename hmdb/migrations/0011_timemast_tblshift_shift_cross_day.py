# Generated by Django 4.1.3 on 2023-09-21 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmdb', '0010_timeshift_tblleave_empstatistic_emp_type_tblot'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeMast',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emptype', models.CharField(blank=True, db_column='emp_type', max_length=20, null=True)),
                ('datetimescan', models.CharField(blank=True, max_length=50, null=True)),
                ('workdate', models.CharField(blank=True, max_length=20, null=True)),
                ('worktime', models.CharField(blank=True, max_length=20, null=True)),
                ('ampm', models.CharField(blank=True, max_length=10, null=True)),
                ('machineno', models.CharField(blank=True, max_length=10, null=True)),
                ('shift', models.CharField(blank=True, db_column='shiftcode', max_length=10, null=True)),
                ('period', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'ta_mast',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='tblshift',
            name='shift_cross_day',
            field=models.CharField(blank=True, db_column='crossday', max_length=10, null=True),
        ),
    ]
# Generated by Django 2.2.11 on 2020-04-02 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControlPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='포함 항목 물품')),
            ],
        ),
        migrations.RemoveField(
            model_name='postroom',
            name='parking',
        ),
        migrations.AddField(
            model_name='postroom',
            name='living_expenses',
            field=models.CharField(max_length=15, null=True, verbose_name='생활비'),
        ),
        migrations.AddField(
            model_name='postroom',
            name='living_expenses_detail',
            field=models.CharField(max_length=20, null=True, verbose_name='생활비 항목'),
        ),
        migrations.AlterField(
            model_name='postroom',
            name='option',
            field=models.ManyToManyField(to='posts.OptionItem', verbose_name='옵션 항목'),
        ),
        migrations.AlterField(
            model_name='postroom',
            name='parkingFee',
            field=models.IntegerField(null=True, verbose_name='주차 비용'),
        ),
        migrations.AlterField(
            model_name='postroom',
            name='title',
            field=models.CharField(max_length=20, null=True, verbose_name='제목'),
        ),
        migrations.CreateModel(
            name='MaintenanceFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalFee', models.IntegerField(verbose_name='관리비 합계')),
                ('controlPoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.ControlPoint', verbose_name='포함 항목')),
                ('postRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.PostRoom', verbose_name='해당 매물')),
            ],
        ),
        migrations.AddField(
            model_name='postroom',
            name='management',
            field=models.ManyToManyField(through='posts.MaintenanceFee', to='posts.ControlPoint'),
        ),
    ]

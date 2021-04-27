# Generated by Django 2.2.17 on 2021-04-27 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='активен'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('F', 'формируется'), ('S', 'отправлен'), ('P', 'оплачен'), ('M', 'доставляется'), ('D', 'отменен')], db_index=True, default='F', max_length=1, verbose_name='статус'),
        ),
    ]

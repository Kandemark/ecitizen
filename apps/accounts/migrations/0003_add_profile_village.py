from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_add_transaction_pin'),
        ('counties', '0002_add_village_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='village',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='residents',
                to='counties.village',
            ),
        ),
    ]

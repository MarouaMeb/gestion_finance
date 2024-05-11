# Generated by Django 5.0.3 on 2024-05-11 14:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devises', '0001_initial'),
        ('factures', '0002_remove_facture_commande_ligne_facture_commande_ligne'),
        ('paiements', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payer',
            fields=[
                ('id_paiement', models.AutoField(primary_key=True, serialize=False)),
                ('date_paiement', models.DateField(auto_now_add=True)),
                ('montant', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('montant_partiel', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('est_annule', models.BooleanField(default=False)),
                ('etat', models.CharField(choices=[('complet', 'Complet'), ('partiel', 'Partiel')], default='complet', max_length=20)),
                ('mode_reglement', models.CharField(blank=True, choices=[('Espèce', 'Espèce'), ('Chèque', 'Chèque'), ('CIB', 'CIB'), ('Avance', 'Avance'), ('Virement', 'Virement')], max_length=20, null=True)),
                ('commentaire', models.CharField(blank=True, max_length=255, null=True)),
                ('creer_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payer', to=settings.AUTH_USER_MODEL)),
                ('devise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='devises.devise')),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factures.facture')),
            ],
        ),
    ]

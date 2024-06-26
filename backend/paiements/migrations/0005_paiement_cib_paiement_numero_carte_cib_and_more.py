# Generated by Django 5.0.3 on 2024-06-01 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paiements', '0004_alter_paiement_montant_partiel_delete_payer'),
    ]

    operations = [
        migrations.AddField(
            model_name='paiement',
            name='cib',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='paiement',
            name='numero_carte_cib',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paiement',
            name='numero_cheque',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paiement',
            name='payer_timbre',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='paiement',
            name='preciser',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paiement',
            name='veuillez_choisir_banque_cheque',
            field=models.CharField(blank=True, choices=[('banque1', 'Banque 1'), ('banque2', 'Banque 2'), ('banque3', 'Banque 3')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='paiement',
            name='veuillez_choisir_banque_virement',
            field=models.CharField(blank=True, choices=[('banque1', 'Banque 1'), ('banque2', 'Banque 2'), ('banque3', 'Banque 3')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='paiement',
            name='virement',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='mode_reglement',
            field=models.CharField(choices=[('Espèce', 'Espèce'), ('Chèque', 'Chèque'), ('CIB', 'CIB'), ('Avance', 'Avance'), ('Virement', 'Virement'), ('Autre', 'Autre')], default='complet', max_length=20),
        ),
    ]

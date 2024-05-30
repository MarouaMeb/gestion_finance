from django.shortcuts import render
from rest_framework.generics import ListAPIView,  CreateAPIView, RetrieveAPIView
from rest_framework import generics
from .models import Facture
from .serializers import FactureSerializer , FactureAjoutSerializer
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from commandes.models import Commande
from commandes.models import Commande_ligne
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter , A4
from django.views.generic import View
from django.http import  HttpResponse
from .models import Facture
from .serializers import FactureSerializer
from rest_framework import generics
from io import BytesIO
from decimal import Decimal 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from clients.models import Client
from io import BytesIO

from rest_framework.views import APIView
from rest_framework.response import Response
from factures.models import Facture

class RapportFacturesVenteView(APIView):
    def get(self, request, *args, **kwargs):
        # Liste des colonnes
        # columns = [
        #     'ID Facture', 'Client', 'Date Création', 'Date Comptabilisation', 'Date Échéance', 
        #     'Non Payée', 'Montant', 'Lignes de Commande'
        # ]

        # Récupération des données des factures de vente
        factures_vente = Facture.objects.filter(type_facture='Vente')
        factures_data = []
        for facture in factures_vente:
            commande_lignes = ", ".join([f"{ligne.produit.nom} x {ligne.quantity}" for ligne in facture.commande_ligne.all()])
            facture_data = {
                'facture_id': facture.facture_id,
                'client': facture.client.nom,
                'date_creation': facture.date_creation.strftime('%Y-%m-%d'),
                'date_comptabilisation': facture.date_comptabilisation.strftime('%Y-%m-%d') if facture.date_comptabilisation else '',
                'date_decheance': facture.date_decheance.strftime('%Y-%m-%d') if facture.date_decheance else '',
                'non_payee': 'Oui' if facture.non_payee else 'Non',
                'montant': str(facture.montant),
                'commande_lignes': commande_lignes
            }
            factures_data.append(facture_data)

        # Envoi des données sous forme de JSON
        return Response({ 'data': factures_data})

class RapportFacturesServiceView(APIView):
    def get(self, request, *args, **kwargs):
        # Liste des colonnes
        # columns = [
        #     'ID Facture', 'Client', 'Date Création', 'Date Comptabilisation', 'Date Échéance', 
        #     'Non Payée', 'Montant', 'Lignes de Commande'
        # ]

        # Récupération des données des factures de vente
        factures_service = Facture.objects.filter(type_facture='Service')
        factures_data = []
        for facture in factures_service:
            commande_lignes = ", ".join([f"{ligne.produit.nom} x {ligne.quantity}" for ligne in facture.commande_ligne.all()])
            facture_data = {
                'facture_id': facture.facture_id,
                'client': facture.client.nom,
                'date_creation': facture.date_creation.strftime('%Y-%m-%d'),
                'date_comptabilisation': facture.date_comptabilisation.strftime('%Y-%m-%d') if facture.date_comptabilisation else '',
                'date_decheance': facture.date_decheance.strftime('%Y-%m-%d') if facture.date_decheance else '',
                'non_payee': 'Oui' if facture.non_payee else 'Non',
                'montant': str(facture.montant),
                'commande_lignes': commande_lignes
            }
            factures_data.append(facture_data)

        # Envoi des données sous forme de JSON
        return Response({ 'data': factures_data})


class PDFFactureView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            facture = Facture.objects.get(id=id)
            commande_lignes = facture.commande_ligne.all()

            # Préparation des données
            data = {
                'id_facture': facture.facture_id,
                'client': facture.client.nom,
                'raison_sociale' : facture.client.raison_sociale ,
                'rue': facture.client.rue,
                'ville': facture.client.ville,
                'pays': facture.client.pays,
                'nif': facture.client.nif,
                'nis': facture.client.nis,
                'date_creation': facture.date_creation,
                'date_comptabilisation': facture.date_comptabilisation,
                'date_decheance': facture.date_decheance,
                'produits': [],
                'total_ht': 0,
                'tva': facture.client.code_tva,
                
                'devise': str(facture.client.devise),
                
            }

            total_ht = Decimal('0')

            for commande_ligne in commande_lignes:
                produit = commande_ligne.produit
                commande = commande_ligne.commande
                # pht = Decimal(commande.pht)
                #tva = pht * Decimal(facture.client.code_tva) / Decimal('100')
                #ttc = pht + tva
                montant = produit.prix_unitaire * commande_ligne.quantity

                data['produits'].append({
                    'nom': produit.nom,
                    'prix_unitaire': f"{produit.prix_unitaire:.2f}",
                    'quantite': commande_ligne.quantity,
                    'montant' : f"{montant}",
                    'tva': f"{facture.client.code_tva}%",
                    # 'pht': f"{pht:.2f}",
                    # 'ttc': f"{ttc:.2f}"
                })

                total_ht += montant

            data['total_ht'] = f"{total_ht:.2f}"
            #data['tva'] = f"{total_ht * Decimal(facture.client.code_tva) / Decimal('100'):.2f}"
            #data['montant'] = f"{total_ht * Decimal(facture.client.code_tva) / Decimal('100'):.2f}"
            data['ttc'] = f"{total_ht + (total_ht * Decimal(facture.client.code_tva) / Decimal('100')):.2f}"

            return Response(data, status=status.HTTP_200_OK)
        except Facture.DoesNotExist:
            return Response({'error': 'La facture demandée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND)

# class PDFFactureView(View):
#     def get(self, request, id, *args, **kwargs):
#         try:
#             facture = Facture.objects.get(id=id)
#             commande_lignes = facture.commande_ligne.all()

#             buffer = BytesIO()

#             pdf = canvas.Canvas(buffer, pagesize=A4)
            
#             pdf.drawString(25, 800, f"ID Facture: {facture.facture_id}")
#             pdf.drawString(25, 780, f"Client: {facture.client.nom}")
#             pdf.drawString(25, 760, f"Date de création: {facture.date_creation}")
#             pdf.drawString(25, 740, f"Date de comptabilisation: {facture.date_comptabilisation}")
#             pdf.drawString(25, 720, f"Date de déchéance: {facture.date_decheance}")

           
#             pdf.drawString(25, 660, "Produit")
#             pdf.drawString(115, 660, "Prix unitaire")
#             pdf.drawString(205, 660, "Quantité")
#             pdf.drawString(295,660,"TVA")
#             pdf.drawString(385, 660, "PHT")
#             pdf.drawString(475, 660, "PTC") 

            
#             y_position = 630
#             total_pht = Decimal('0')

             
#             for commande_ligne in commande_lignes:
#                 produit = commande_ligne.produit
#                 commande = commande_ligne.commande

#                 pdf.drawString(20, y_position, produit.nom)
#                 pdf.drawString(125, y_position, f"{produit.prix_unitaire:.2f} ")
#                 pdf.drawString(230, y_position, str(commande_ligne.quantity))
#                 pdf.drawString(295, y_position, f"{facture.client.code_tva}%")
#                 pdf.drawString(380, y_position, f"{commande.pht:.2f} ")
#                 pdf.drawString(470, y_position, f"{commande.ttc:.2f} ")

#                 total_pht += Decimal(commande.pht)
#                 y_position -= 20  

#             pdf.drawString(385, y_position-10, "THT:")
#             pdf.drawString(385, y_position-25, "TVA:  ")
#             pdf.drawString(385, y_position-40, "TTC: ")

#             pdf.drawString(420, y_position-10, f" {total_pht:.2f} {facture.client.devise} ")
#             pdf.drawString(420, y_position-25, f" {total_pht * Decimal(facture.client.code_tva) / Decimal('100'):.2f} {facture.client.devise} ")
#             pdf.drawString(420, y_position-40, f" {total_pht + (total_pht * Decimal(facture.client.code_tva) / Decimal('100')):.2f} {facture.client.devise} ")
              
#             pdf.showPage()
#             pdf.save()

#             pdf_data = buffer.getvalue()

#             response = HttpResponse(pdf_data, content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename="facture.pdf"'
#             # pour le téléchargement automatique
#             #response['Content-Disposition'] = f'attachment; filename="facture_{id}.pdf"'

#             return response
#         except Facture.DoesNotExist:
#             return HttpResponse('La facture demandée n\'existe pas.', status=404)


class FactureListView(ListAPIView):
    
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer

# class FactureDetail(RetrieveAPIView):
#     queryset = Facture.objects.all()
#     serializer_class = FactureSerializer
#     lookup_field = 'id'

class FactureListCreate(CreateAPIView):
    queryset = Facture.objects.all()
    serializer_class = FactureAjoutSerializer


class FactureVenteList(generics.ListAPIView):
    queryset = Facture.objects.filter(type_facture='Vente')
    serializer_class = FactureSerializer

class FactureServiceList(generics.ListAPIView):
    queryset = Facture.objects.filter(type_facture='Service')
    serializer_class = FactureSerializer

class FactureNonPayeeList(generics.ListAPIView):
    serializer_class = FactureSerializer

    def get_queryset(self):
        return Facture.objects.filter(non_payee=True)
    



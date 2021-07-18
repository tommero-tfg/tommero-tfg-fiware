import datetime
import io

from django import forms
from django.contrib import admin
from django.contrib.messages import ERROR, info, warning
from django.core.files.base import ContentFile
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer, Paragraph, SimpleDocTemplate

from .models import Contract, Fine


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = '__all__'


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    form = FineForm
    list_display = ['id', 'guid', 'cost', 'contract', 'creation_datetime', 'modification_datetime']


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    form = ContractForm
    list_display = ['id', 'guid', 'user', 'car', 'status', 'monthly_cost', 'annual_mileage', 'duration', 'start_date',
                    'reject_date', 'bank_account', ]

    actions = ['process_contract']

    def process_contract(self, request, queryset):
        if len(queryset) == 1:
            contract = queryset.first()
            contract_ids_associated = [contract.id for contract in Contract.objects.filter(user_id=contract.user_id)]
            if contract.status != 'E':
                self.message_user(request, 'El contrato ya ha sido procesado.')
            elif Fine.objects.filter(contract_id__in=contract_ids_associated, pay_date__isnull=True):
                self.message_user(request,
                                  'El usuario tiene incidencias sin resolver, así que no se puede llevar a cabo el contrato',
                                  level='warning')
            else:
                buffer = io.BytesIO()

                my_doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50,
                                           bottomMargin=18)
                content = []

                user_info = contract.user.user_info

                user_name = user_info.user.first_name
                user_first_surname = user_info.first_surname
                user_second_surname = user_info.second_surname
                user_dni = user_info.dni
                request_datetime = '/'.join(contract.creation_datetime.date().isoformat().split('-')[::-1])
                response_datetime = '/'.join(datetime.datetime.now().date().isoformat().split('-')[::-1])

                sample_style_sheet = getSampleStyleSheet()
                paragraph_1 = Paragraph("Rent A Car", sample_style_sheet['Heading1'])
                paragraph_2 = Paragraph("Documento oficial de contrato oficializado.", sample_style_sheet['Heading2'])
                paragraph_3 = Paragraph(f"Por el presente documento queda grabado que el cliente {user_name} "
                                        f"{user_first_surname} {user_second_surname} con el siguiente número"
                                        f" identificativo  {user_dni} y la empresa Rent A Car formalizan"
                                        f" el siguiente contrato, solicitado a fecha de {request_datetime}, y formalizado"
                                        f" hoy, a {response_datetime}.")
                paragraph_4 = Paragraph(f"El modelo solicitado para el contrato es el siguiente:",
                                        sample_style_sheet['BodyText'])
                paragraph_5 = Paragraph(f"\t- La marca del coche: {contract.car.brand}", sample_style_sheet['BodyText'])

                paragraph_6 = Paragraph(f"Las condiciones para realizar este contrato son las siguentes: Una duración de"
                                        f" {contract.duration} meses, con un kilometraje anual de {contract.annual_mileage} y "
                                        f"una cuota mensual de {contract.monthly_cost}€", sample_style_sheet['BodyText'])
                paragraph_7 = Paragraph("Cualquier consulta contacte con nuestro soporte técnico",
                                         sample_style_sheet['BodyText'])
                paragraph_8 = Paragraph("Un fuerte abrazo, Rent A Car.", sample_style_sheet['Heading2'])

                content.append(paragraph_1)
                content.append(Spacer(1, 3))
                content.append(paragraph_2)
                content.append(Spacer(1, 10))
                content.append(Spacer(1, 3))
                content.append(paragraph_3)
                content.append(Spacer(1, 3))
                content.append(paragraph_4)
                content.append(Spacer(1, 5))
                content.append(paragraph_5)
                content.append(Spacer(1, 3))
                content.append(paragraph_6)
                content.append(Spacer(1, 3))
                content.append(paragraph_7)
                content.append(Spacer(1, 5))
                content.append(paragraph_8)
                my_doc.build(content)

                buffer.seek(0)
                doc = ContentFile(FileResponse(buffer, filename=f'contrato-{contract.guid}.pdf').getvalue())
                contract.document.save(f'contrato-{contract.guid}.pdf', doc, save=False)
                contract.status = 'A'
                contract.start_date = datetime.date.today()
                contract.save()
                self.message_user(request, 'Contrato procesado', level='info')
        else:
            self.message_user(request, 'Solo se puede procesar un contrato por acción', level=ERROR)

    process_contract.short_description = 'Procesar contrato'

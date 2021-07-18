import datetime
import io

from django import forms
from django.contrib import admin
from django.contrib.messages import ERROR
from django.core.files.base import ContentFile
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.platypus.para import Paragraph

from .models import UserInfo, Application


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = '__all__'


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    form = UserInfoForm
    list_display = ['id', 'user', 'first_surname', 'second_surname', 'birthdate']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationForm
    list_display = ['id', 'user_info', 'creation_datetime']
    actions = ['create_document']

    def create_document(self, request, queryset):
        if len(queryset) == 1:
            self.message_user(request, 'Se ha ejecutado la acción')
            buffer = io.BytesIO()

            my_doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50,
                                       bottomMargin=18)
            content = []

            application = queryset.first()
            user_info = application.user_info

            user_name = user_info.user.first_name
            user_first_surname = user_info.first_surname
            user_second_surname = user_info.second_surname
            user_dni = user_info.dni
            user_birthdate = '/'.join(user_info.birthdate.isoformat().split('-')[::-1])
            user_email = user_info.user.email
            user_phone = user_info.phone_number
            user_username = user_info.user.username
            request_datetime = '/'.join(queryset.first().creation_datetime.date().isoformat().split('-')[::-1])
            response_datetime = '/'.join(datetime.datetime.now().date().isoformat().split('-')[::-1])

            sample_style_sheet = getSampleStyleSheet()
            paragraph_1 = Paragraph("Rent A Car", sample_style_sheet['Heading1'])
            paragraph_2 = Paragraph("Documento informativo de datos personales.", sample_style_sheet['Heading2'])
            paragraph_3 = Paragraph(f"Este documento ha sido generado para responder a la solicitud del cliente "
                                    f"{user_name} {user_first_surname} {user_second_surname} realizada en fecha de "
                                    f"{request_datetime}.", sample_style_sheet['BodyText'])
            paragraph_4 = Paragraph(f"En este documento se va a exponer todos los datos que la empresa Rent A Car tiene"
                                    f" a fecha de {response_datetime}. Todos estos datos han sido recogidos bajo "
                                    f"consentimiento del cliente:", sample_style_sheet['BodyText'])
            paragraph_5 = Paragraph(f"\t- Nombre: {user_name}.", sample_style_sheet['BodyText'])
            paragraph_6 = Paragraph(f"\t- Primer apellido: {user_first_surname}.", sample_style_sheet['BodyText'])
            paragraph_7 = Paragraph(f"\t- Segundo apellido: {user_second_surname}.", sample_style_sheet['BodyText'])
            paragraph_8 = Paragraph(f"\t- DNI: {user_dni}.", sample_style_sheet['BodyText'])
            paragraph_9 = Paragraph(f"\t- Fecha de nacimiento: {user_birthdate}.", sample_style_sheet['BodyText'])
            paragraph_10 = Paragraph(f"\t- Email: {user_email}.", sample_style_sheet['BodyText'])
            paragraph_11 = Paragraph(f"\t- Número de teléfono: {user_phone}.", sample_style_sheet['BodyText'])
            paragraph_12 = Paragraph(f"\t- Nombre de usuario: {user_username}.", sample_style_sheet['BodyText'])
            paragraph_13 = Paragraph("Desde Rent A Car le ponemos en conocimiento de qué si alguno de estos datos no "
                                     "fuera correcto, puede modificarlos en cualquier momento desde su perfil y si "
                                     "quisiera eliminarlos puede darse de baja del sistema.",
                                     sample_style_sheet['BodyText'])
            paragraph_14 = Paragraph("Cualquier consulta contacte con nuestro soporte técnico",
                                     sample_style_sheet['BodyText'])
            paragraph_15 = Paragraph("Un fuerte abrazo, Rent A Car.", sample_style_sheet['Heading2'])

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
            content.append(Spacer(1, 3))
            content.append(paragraph_8)
            content.append(Spacer(1, 3))
            content.append(paragraph_9)
            content.append(Spacer(1, 3))
            content.append(paragraph_10)
            content.append(Spacer(1, 3))
            content.append(paragraph_11)
            content.append(Spacer(1, 3))
            content.append(paragraph_12)
            content.append(Spacer(1, 5))
            content.append(paragraph_13)
            content.append(Spacer(1, 3))
            content.append(paragraph_14)
            content.append(Spacer(1, 4))
            content.append(paragraph_15)
            my_doc.build(content)

            inst = queryset.first()
            buffer.seek(0)
            doc = ContentFile(FileResponse(buffer, filename='ejemplo.pdf').getvalue())
            inst.rights.save(f'derecho-{user_info.guid}.pdf', doc, save=False)
            inst.save()
        else:
            self.message_user(request, 'Solo se puede generar un documento por acción', level=ERROR)

    create_document.short_description = 'Crear documento'

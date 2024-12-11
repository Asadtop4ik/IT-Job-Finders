from rest_framework import viewsets
from answers.serializers import ContactSerializer
from answers.models import Contact


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer




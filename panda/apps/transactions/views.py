from datetime import datetime

from rest_framework import viewsets, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse

from panda.apps.transactions.models import Transaction
from panda.apps.transactions.serializers import TransactionSerializer, UploadsSerializer
from panda.apps.transactions.tasks import start_ingestion


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'transactions': reverse('api:transaction-list', request=request),
            'uploads': reverse(f"api:{UploadsView.name}", request=request),
        })


class TransactionViewSet(viewsets.ViewSet):
    filter_fields = ('date',)

    def list(self, request, **kwargs):
        queryset = self.get_query_set()
        pagination = PageNumberPagination()
        queryset = pagination.paginate_queryset(queryset, request)
        serializer = TransactionSerializer(queryset, many=True)
        return pagination.get_paginated_response(serializer.data)

    def get_query_set(self):
        """ TODO : https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html """
        queryset = Transaction.objects.all()
        params = self.request.query_params
        country, date = params.get("country", None), params.get("date", None)
        if country:
            queryset = queryset.filter(country=country)
        if date:
            date = datetime.strptime(date, '%Y/%m/%d')
            queryset = queryset.filter(date=date.strftime('%Y-%m-%d'))
        return queryset


class UploadsView(generics.CreateAPIView):
    name = 'uploads'
    serializer_class = UploadsSerializer

    def create(self, request, **kwargs):
        serializer = UploadsSerializer(data=request.data)
        if serializer.is_valid():
            upload = serializer.save()
            start_ingestion.delay(upload.file.path)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers

from panda.apps.transactions.models import Transaction, Uploads


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Transaction


class UploadsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Uploads

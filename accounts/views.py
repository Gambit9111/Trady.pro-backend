from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import AccountSerializer, TransactionSerializer, SymbolSerializer, Trading_SystemSerializer
from .models import Account, Transaction, Symbol, Trading_System
from rest_framework.parsers import MultiPartParser, FormParser

# account list and create view

class AccountListCreateView(GenericAPIView):
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# account detail view

class AccountDetailView(GenericAPIView):
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            account = Account.objects.get(pk=pk)
            if account.user == request.user:
                serializer = AccountSerializer(account)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            account = Account.objects.get(pk=pk)
            if account.user == request.user:
                serializer = AccountSerializer(account, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            account = Account.objects.get(pk=pk)
            if account.user == request.user:
                account.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# transaction list and create view

class TransactionListCreateView(GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        transactions = Transaction.get_all_transactions(request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        # check if account belongs to user
        try:
            account = Account.objects.get(pk=request.data['account'])
            if account.user == request.user:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# transaction detail view

class TransactionDetailView(GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            if transaction.account.user == request.user:
                serializer = TransactionSerializer(transaction)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            if transaction.account.user == request.user:
                transaction.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# symbol list create view

class SymbolListCreateView(ListCreateAPIView):
    serializer_class = SymbolSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Symbol.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# symbol detail view

class SymbolDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SymbolSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Symbol.objects.filter(user=self.request.user)

# trading system list create view

class Trading_SystemListCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        trading_systems = Trading_System.objects.filter(user=request.user)
        serializer = Trading_SystemSerializer(trading_systems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print(request.data)
        serializer = Trading_SystemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# trading system get update delete view

class Trading_SystemDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk):
        try:
            trading_system = Trading_System.objects.get(pk=pk)
            if trading_system.user == request.user:
                serializer = Trading_SystemSerializer(trading_system)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Trading_System.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            trading_system = Trading_System.objects.get(pk=pk)
            if trading_system.user == request.user:
                serializer = Trading_SystemSerializer(trading_system, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Trading_System.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            trading_system = Trading_System.objects.get(pk=pk)
            if trading_system.user == request.user:
                trading_system.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Trading_System.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        
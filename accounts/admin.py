from django.contrib import admin

from .models import Trading_System, Symbol, Account, Transaction

# extended admin panel
class Trading_SystemAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'created_at')
    list_filter = ('user', 'name', 'description', 'created_at')
    search_fields = ('user', 'name', 'description', 'created_at')

class SymbolAdmin(admin.ModelAdmin):
    list_display = ('label', 'user')
    list_filter = ('label', 'user')
    search_fields = ('label', 'user')

# display transactions in account panel
class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0

class AccountAdmin(admin.ModelAdmin):
    list_display = ('label', 'user', 'balance', 'created_at')
    list_filter = ('label', 'user', 'balance', 'created_at')
    search_fields = ('label', 'user', 'balance', 'created_at')
    inlines = [TransactionInline]

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'created_at')
    list_filter = ('account', 'transaction_type', 'amount', 'created_at')
    search_fields = ('account', 'transaction_type', 'amount', 'created_at')

admin.site.register(Trading_System, Trading_SystemAdmin)
admin.site.register(Symbol, SymbolAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)

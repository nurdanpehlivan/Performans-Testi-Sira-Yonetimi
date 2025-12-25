from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Tabloda hangi sütunlar görünsün?
    list_display = ('number', 'service_type', 'created_at', 'file_path')
    # Sağ tarafa filtreleme ekleyelim (İşlem türüne göre)
    list_filter = ('service_type', 'created_at')
    # Arama kutusu ekleyelim (Bilet numarasına göre)
    search_fields = ('number',)
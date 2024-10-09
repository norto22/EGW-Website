from .models import Player, Airline, Subsidiary, Transaction
from django.contrib import admin

# Inline form for Subsidiaries in Airline Admin
class SubsidiaryInline(admin.TabularInline):  # or use StackedInline for a more detailed layout
    model = Subsidiary
    extra = 1  # Shows 1 extra empty form for adding new subsidiaries
    fields = ('name', 'hub', 'date_formed')
    classes = ('collapse',)  # Makes it collapsible to keep things neat

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('discord_username', 'airlinesim_username', 'joined_date', 'balance', 'amount_owed')
    search_fields = ('discord_username', 'airlinesim_username')
    list_filter = ('joined_date',)
    ordering = ('discord_username',)
    exclude = ('balance', 'amount_owed')
    readonly_fields = ('joined_date', 'balance', 'amount_owed')

    actions = ['deduct_monthly_cost']

    def deduct_monthly_cost(self, request, queryset):
        monthly_cost = 360 / queryset.count()
        for player in queryset:
            player.balance -= monthly_cost
            player.save()
        self.message_user(request, f"Monthly cost of €{monthly_cost} deducted from each player's balance.")
    deduct_monthly_cost.short_description = 'Deduct Monthly Cost from Selected Players'


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'player', 'hub', 'date_formed')
    search_fields = ('name', 'hub', 'player__discord_username')
    list_filter = ('hub',)
    ordering = ('name',)

    # Include the Subsidiary Inline
    inlines = [SubsidiaryInline]

    fieldsets = (
        (None, {
            'fields': ('player', 'name', 'hub', 'date_formed')
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('player', 'payment_date', 'formatted_amount', 'transaction_type', 'description')
    list_filter = ('transaction_type',)
    search_fields = ('player__discord_username', 'description')

    def formatted_amount(self, obj):
        if obj.transaction_type == 'credit':
            return f"+€{obj.amount}"
        else:
            return f"-€{obj.amount}"
    formatted_amount.short_description = 'Amount'

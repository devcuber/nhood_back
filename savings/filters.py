from django.contrib import admin
class MovementPendingFilter(admin.SimpleListFilter):
    title = ("Status")
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("pending", ("Unassigned movements")),
            ("done", ("Assigned movements")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "pending":
            return queryset.filter(house__isnull=True)
        if self.value() == "done":
            return queryset.filter(house__isnull=False)

class BalanceHasCreditFilter(admin.SimpleListFilter):
    title = ("Balance")
    parameter_name = "has_balance"

    def lookups(self, request, model_admin):
        return [
            ("has_balance", ("Has Balance")),
            ("has_no_balance", ("Has No Balance")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "has_balance":
            return queryset.filter(balance__gt =0)
        if self.value() == "has_no_balance":
            return queryset.filter(balance=0)
        
class BalanceHasDebtFilter(admin.SimpleListFilter):
    title = ("Debt")
    parameter_name = "has_debt"

    def lookups(self, request, model_admin):
        return [
            ("has_debt", ("Has Debt")),
            ("has_no_debt", ("Has No Debt")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "has_debt":
            return queryset.filter(debt__gt =0)
        if self.value() == "has_no_debt":
            return queryset.filter(debt=0)
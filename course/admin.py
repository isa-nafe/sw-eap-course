from django.contrib import admin
from .models import CourseMaterial, UserPayment # Ensure both models are imported

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'uploaded_at', 'uploaded_by')
    list_filter = ('material_type', 'uploaded_by')
    search_fields = ('title', 'description')

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.uploaded_by:
            return ['uploaded_by']
        return []

@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_paid_for_course', 'payment_date', 'amount_paid', 'stripe_customer_id', 'stripe_payment_intent_id')
    list_filter = ('has_paid_for_course',)
    search_fields = ('user__username', 'stripe_customer_id', 'stripe_payment_intent_id')
    # Fields populated by Stripe or signals should ideally be read-only in admin
    readonly_fields = ('payment_date', 'stripe_customer_id', 'stripe_payment_intent_id', 'amount_paid')

    # Optional: Prevent direct creation of UserPayment objects in admin if they are meant to be created by signals/Stripe flow
    # def has_add_permission(self, request):
    #     return False
    # Optional: Prevent deletion if it has implications
    # def has_delete_permission(self, request, obj=None):
    #     return False

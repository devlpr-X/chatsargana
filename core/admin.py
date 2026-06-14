from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteContent, HeroStat, Feature, AboutCard, BenefitTeaser,
    ProductCategory, Product,
    NutrientCard, UsageCard,
    KeyNumber, BenefitDetail,
    MissionValue, ProcessStep,
    Order, OrderItem,
)

admin.site.site_header = 'Чацаргана — Удирдлагын самбар'
admin.site.site_title  = 'Чацаргана Admin'
admin.site.index_title = 'Удирдлагын самбар'


# ─── Site Content ────────────────────────────────────────────
@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display  = ('label', 'key', 'value_preview')
    search_fields = ('key', 'label', 'value')
    list_per_page = 50

    def value_preview(self, obj):
        v = obj.value
        return v[:80] + '…' if len(v) > 80 else v
    value_preview.short_description = 'Утга'


# ─── Hero Stats ──────────────────────────────────────────────
@admin.register(HeroStat)
class HeroStatAdmin(admin.ModelAdmin):
    list_display = ('num', 'label', 'order')
    list_editable = ('order',)


# ─── Features ────────────────────────────────────────────────
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'description', 'order')
    list_editable = ('order',)


# ─── About Cards ─────────────────────────────────────────────
@admin.register(AboutCard)
class AboutCardAdmin(admin.ModelAdmin):
    list_display = ('card_type', 'value', 'label', 'order')
    list_editable = ('order',)


# ─── Benefit Teaser ──────────────────────────────────────────
@admin.register(BenefitTeaser)
class BenefitTeaserAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'order')
    list_editable = ('order',)


# ─── Products ────────────────────────────────────────────────
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('image_preview', 'name', 'category', 'price_display', 'unit', 'badge', 'is_featured', 'is_active', 'order')
    list_editable = ('is_active', 'is_featured', 'order')
    list_filter   = ('category', 'badge', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    list_per_page = 20

    fieldsets = (
        ('Үндсэн мэдээлэл', {
            'fields': ('name', 'category', 'description', 'image')
        }),
        ('Үнэ ба хэмжих нэгж', {
            'fields': ('price', 'unit')
        }),
        ('Дизайн', {
            'fields': ('badge', 'badge_icon', 'nutrients', 'is_featured')
        }),
        ('Харагдах байдал', {
            'fields': ('is_active', 'order')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:6px;object-fit:contain;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Зураг'

    def price_display(self, obj):
        return f'₮{obj.price:,.0f}'
    price_display.short_description = 'Үнэ'


# ─── Nutrient Cards ──────────────────────────────────────────
@admin.register(NutrientCard)
class NutrientCardAdmin(admin.ModelAdmin):
    list_display = ('letter', 'title', 'value_text', 'bar_pct', 'order')
    list_editable = ('bar_pct', 'order')


# ─── Usage Cards ─────────────────────────────────────────────
@admin.register(UsageCard)
class UsageCardAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'icon', 'title', 'order')
    list_editable = ('order',)
    fields = ('image', 'icon', 'title', 'description', 'order')

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px"/>', obj.image.url)
        return '—'
    image_preview.short_description = 'Зураг'


# ─── Key Numbers ─────────────────────────────────────────────
@admin.register(KeyNumber)
class KeyNumberAdmin(admin.ModelAdmin):
    list_display = ('num', 'label', 'order')
    list_editable = ('order',)


# ─── Benefit Detail ──────────────────────────────────────────
@admin.register(BenefitDetail)
class BenefitDetailAdmin(admin.ModelAdmin):
    list_display = ('icon', 'number', 'title', 'is_reverse', 'order')
    list_editable = ('is_reverse', 'order')


# ─── Mission Values ──────────────────────────────────────────
@admin.register(MissionValue)
class MissionValueAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'order')
    list_editable = ('order',)


# ─── Process Steps ───────────────────────────────────────────
@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('number', 'icon', 'title', 'order')
    list_editable = ('order',)


# ─── Orders ──────────────────────────────────────────────────
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'quantity', 'price', 'subtotal_display')
    fields = ('product_name', 'quantity', 'price', 'subtotal_display')

    def subtotal_display(self, obj):
        return f'₮{obj.subtotal:,.0f}'
    subtotal_display.short_description = 'Нийт'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'customer_name', 'customer_phone', 'status_badge', 'total_display', 'created_at')
    list_filter   = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_email', 'address')
    readonly_fields = ('user', 'session_key', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    list_per_page = 30

    fieldsets = (
        ('Захиалагч', {'fields': ('user', 'session_key', 'customer_name', 'customer_phone', 'customer_email')}),
        ('Хүргэлт', {'fields': ('address', 'latitude', 'longitude', 'note')}),
        ('Захиалга', {'fields': ('status', 'total_price', 'created_at', 'updated_at')}),
    )

    def status_badge(self, obj):
        color = obj.status_color()
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:20px;font-size:12px">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Төлөв'

    def total_display(self, obj):
        return f'₮{obj.total_price:,.0f}'
    total_display.short_description = 'Нийт'

from django.contrib import admin
from django.utils.html import format_html
from .models import Menu, Category, Item, TableQRCode

# نمایش آیتم‌ها به صورت Inline داخل هر کتگوری
class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    fields = ('name', 'description', 'image')  # price حذف شد
    readonly_fields = ()

# پنل ادمین برای Category با امکان آپلود عکس شاخص و Inline آیتم‌ها
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_image_preview')  # نمایش پیش‌نمایش عکس
    inlines = [ItemInline]
    search_fields = ['name']

    def category_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "—"
    category_image_preview.short_description = "تصویر کتگوری"

# ثبت منو و آیتم‌ها
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # price حذف شد
    list_filter = ['category']
    search_fields = ['name', 'description']

# پنل ادمین برای TableQRCode
@admin.register(TableQRCode)
class TableQRCodeAdmin(admin.ModelAdmin):
    list_display = ('menu', 'code', 'table_number', 'qr_preview', 'created_at')

    def qr_preview(self, obj):
        if obj.qr_image:
            return format_html('<img src="{}" width="120" height="120" />', obj.qr_image.url)
        return "—"
    qr_preview.short_description = "QR Code"

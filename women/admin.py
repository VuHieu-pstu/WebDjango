from django.contrib import admin,messages
from django.utils.safestring import mark_safe

import women.models
from .models import Women, Category, TagPost, Husband,User


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married','Замужен'),
            ('single','Не замужен')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ('title','slug','photo','post_photo','content','is_published','cat','tags','husband') #de trong trang chinh sua cac ban ghi trang admin chi hien nhung truong duoc chi dinh
    #exclude = ('is_published','tags') #анологично но в этом случае исключить поле, которые ты не хочешь отображать в странице редактирования записей.
    readonly_fields = ('post_photo',)
    filter_horizontal = ['tags']   # de tuy chinh truong chon 'tags' trong trang chinh sua cua admin
    #filter_vertical = ['tags']
    #prepopulated_fields = {"slug":("title",)} # de tao tu dong slug tu title, khi do readonly_fields khong duoc chua thuoc tinh slug
    list_display = ('id','title','post_photo','is_published','time_create','time_update','brief_info')
    list_display_links = ('id','title')
    ordering = ('-time_create','title')
    list_editable = ('is_published',)
    list_per_page = 5
    search_fields = ('id','title')
    #search_fields = ('title__startswith','cat__name')
    list_filter = ('cat__name','is_published',MarriedFilter)
    actions = ['set_published','set_draff']
    save_on_top = True

    @admin.display(description="extra info",ordering='content')
    def brief_info(self, women:Women):
        return f"{len(women.content)} words"

    @admin.display(description="изображение", ordering='content')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "без фото"

    @admin.action(description="publish all choices")
    def set_published(self,request,queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request,f"{count} changed status")

    @admin.action(description="set draff all choices")
    def set_draff(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} set draff", messages.WARNING)

@admin.register(Husband)
class HusbandAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'age')
    list_display_links = ('id', 'name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links = ('id', 'name')

@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('tag',)

@admin.register(User)
class HusbandAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'first_name','last_name','photo','date_birth')
    list_display_links = ('id', 'username')

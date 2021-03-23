from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language, Role


# admin.site.register(BookInstance)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 1


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


class RoleInline(admin.TabularInline):
    model = Role
    extra = 1


class AuthorInline(admin.TabularInline):
    model = Role
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # dodam wyswietlanie ksiazek autora
    list_display = ('surname', 'names', 'birthyear', 'death_year')
    fields = ('surname', 'names', 'birthyear', 'death_year', 'bio')
    inlines = [RoleInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'first_published', 'display_genre', 'display_language')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    list_filter = ('status', 'due_back')

    list_display = ('book', 'id', 'status', 'due_back', 'borrower')

    fieldsets = (
        ("Informacje ogólne", {
            'fields': ('book', 'id')
        }),
        ('Dostępność', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


# Register your models here if @admin.register decorator is not used
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Role)

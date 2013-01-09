from checkin.models import Period
from checkin.models import Shift
from checkin.models import ShiftEmployees
from checkin.models import Employee
from checkin.models import Log
from checkin.models import Block

from django.contrib import admin

class ShiftEmployeesInline(admin.TabularInline):
    model = ShiftEmployees
    extra = 5

class PeriodAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name']}),
        ('Time limits', {'fields': ['start_at', 'end_at']}),
    ]
    inlines = [ShiftEmployeesInline]
    list_display = ('__unicode__', 'start_at', 'end_at')
    date_hierarchy = 'start_at'
    list_filter = ['start_at', 'end_at']
    ordering = ['-start_at']

class BlockAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name']}),
        ('Time limits', {'fields': ['start_at', 'end_at']}),
    ]
    list_display = ['__unicode__', 'start_at', 'end_at']
    ordering = ['start_at']

class LogAdmin(admin.ModelAdmin):
    def name(self, obj):
        return obj.shiftemployees.employee.name
    name.admin_order_field = 'shiftemployees'
    def shift(self, obj):
        return obj.shiftemployees.shift

    fieldsets = [
        (None,      {'fields': ['shiftemployees', 'date', 'absent']}),
        ('Logout',  {'fields': ['logout_at']}),
    ]
    list_display = ('name', 'shift', 'date', 'absent', 'logout_at')
    date_hierarchy = 'date'
    list_filter = ['absent', 'shiftemployees__employee__name', 'shiftemployees__period__start_at']
    search_fields = ['shiftemployees__employee__name']
    ordering = ['-date']

class EmployeeAdmin(admin.ModelAdmin):
    def editLink(self, obj):
        return 'Change'
    editLink.short_description = ''
    search_fields = ['name']
    list_display = ['name', 'editLink']
    list_editable = ['name']
    list_display_links = ['editLink']
    ordering = ['name']

class ShiftAdmin(admin.ModelAdmin):
    def editLink(self, obj):
        return 'Change'
    editLink.short_description = ''
    list_display = ['weekday', 'block', 'editLink']
    list_display_links = ['editLink']
    list_filter = ('weekday', 'block')
    ordering = ['weekday']

admin.site.register(Period, PeriodAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Shift, ShiftAdmin)

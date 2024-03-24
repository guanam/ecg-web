from django.contrib import admin
from django.urls import reverse
from import_export.admin import ImportExportModelAdmin
from .models import PatientManage
from django.utils.html import format_html


@admin.register(PatientManage)
class PatientManage(ImportExportModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('patient_id', 'patient_name', "patient_department")
        }),
        ('选填字段', {
            'classes': ('wide', 'extrapretty',),
            'fields': ('patient_age', 'patient_sex', 'patient_ecg', 'patient_telephone',
                       ),
        }),
    )
    save_as_continue = False  # 修改完成之后跳转到元素列表页面

    def predict_button(self, obj):
        return format_html(
            '<a class="btn btn-sm btn-primary" href="{}">诊断</a>',
            reverse('patient_predict', args=[obj.pk])
        )
    predict_button.short_description = '诊断'
    predict_button.allow_tags = True

    def ecg_plot_button(self, obj):
        return format_html(
            '<a class="btn btn-sm btn-primary" href="{}" target="_blank">查看</a>',
            reverse('generate_ecg_plot', args=[obj.pk])
        )
    ecg_plot_button.short_description = '查看'
    ecg_plot_button.allow_tags = True

    list_display = ('patient_id', 'patient_name', 'patient_age', 'patient_sex',
                    'patient_department', 'patient_telephone',
                    'diagnosis_result', 'create_time', 'update_time', 'predict_button', 'ecg_plot_button')

    # 每页显示条目数 缺省值100
    list_per_page = 100
    # 按日期月份筛选 该属性一般不用
    date_hierarchy = 'create_time'
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('patient_name',)

admin.site.site_header = 'ECG诊断系统'
admin.site.site_title = 'ECG诊断系统'
admin.site.index_title = 'ECG诊断系统'
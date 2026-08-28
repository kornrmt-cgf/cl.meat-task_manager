"""
Forms สำหรับ tasks app
"""

from django import forms
from django.utils import timezone

from .models import Task


class TaskCreateForm(forms.ModelForm):
    """ฟอร์มสร้างงาน"""

    assigned_to = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "employee-checkbox",
        }),
        required=False,
        label="มอบหมายให้",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ดึง active employees
        from accounts.models import EmployeeProfile
        self.fields["assigned_to"].queryset = EmployeeProfile.objects.filter(
            status="active",
        ).select_related("user", "team")
        # ตั้งค่า default task_date เป็นวันนี้
        if not self.initial.get("task_date"):
            self.initial["task_date"] = timezone.now().date()
        # ตั้งค่า default deadline เป็นวันนี้ 23:59
        if not self.initial.get("deadline"):
            today = timezone.now().date()
            default_deadline = timezone.make_aware(
                timezone.datetime.combine(today, timezone.datetime.max.time()).replace(second=0)
            )
            self.initial["deadline"] = default_deadline

    # โหมดงาน
    WORK_MODE_CHOICES = [
        ("assigned", "มอบหมายเฉพาะคน"),
        ("open", "เปิดให้แย่งงาน"),
    ]

    work_mode = forms.ChoiceField(
        choices=WORK_MODE_CHOICES,
        initial="assigned",
        widget=forms.RadioSelect(attrs={"class": "work-mode-radio"}),
        label="โหมดงาน",
    )

    reward = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-input",
            "placeholder": "0.00",
            "min": "0",
            "step": "0.01",
        }),
        label="ค่าตอบแทน (฿)",
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "category",
            "priority",
            "task_date",
            "deadline",
            "start_at",
            "prepare_at",
            "estimated_minutes",
            "location",
            "notes",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "ชื่องาน",
                    "autofocus": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "รายละเอียดงาน (ไม่บังคับ)",
                    "rows": 3,
                }
            ),
            "category": forms.Select(attrs={"class": "form-input"}),
            "priority": forms.Select(attrs={"class": "form-input"}),
            "task_date": forms.DateInput(
                attrs={
                    "class": "form-input",
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "deadline": forms.DateTimeInput(
                attrs={
                    "class": "form-input",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "start_at": forms.DateTimeInput(
                attrs={
                    "class": "form-input",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "prepare_at": forms.DateTimeInput(
                attrs={
                    "class": "form-input",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "estimated_minutes": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "นาที",
                    "min": "1",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "สถานที่ (ไม่บังคับ)",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "หมายเหตุ (ไม่บังคับ)",
                    "rows": 2,
                }
            ),
        }


class TaskUpdateForm(forms.ModelForm):
    """ฟอร์มแก้ไขงาน"""

    # โหมดงาน
    WORK_MODE_CHOICES = [
        ("assigned", "มอบหมายเฉพาะคน"),
        ("open", "เปิดให้แย่งงาน"),
    ]

    work_mode = forms.ChoiceField(
        choices=WORK_MODE_CHOICES,
        initial="assigned",
        widget=forms.RadioSelect(attrs={"class": "work-mode-radio"}),
        label="โหมดงาน",
    )

    reward = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-input",
            "placeholder": "0.00",
            "min": "0",
            "step": "0.01",
        }),
        label="ค่าตอบแทน (฿)",
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "category",
            "priority",
            "task_date",
            "deadline",
            "start_at",
            "prepare_at",
            "estimated_minutes",
            "location",
            "notes",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-input", "rows": 3}),
            "category": forms.Select(attrs={"class": "form-input"}),
            "priority": forms.Select(attrs={"class": "form-input"}),
            "task_date": forms.DateInput(
                attrs={"class": "form-input", "type": "date"},
                format="%Y-%m-%d",
            ),
            "deadline": forms.DateTimeInput(
                attrs={"class": "form-input", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "start_at": forms.DateTimeInput(
                attrs={"class": "form-input", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "prepare_at": forms.DateTimeInput(
                attrs={"class": "form-input", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "estimated_minutes": forms.NumberInput(
                attrs={"class": "form-input", "min": "1"}
            ),
            "location": forms.TextInput(attrs={"class": "form-input"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
        }

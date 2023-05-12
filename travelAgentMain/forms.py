from django.contrib.admin.helpers import ActionForm
from django import forms
from django.utils import timezone
import datetime
class UpdateScoreForm(ActionForm):
    # score = forms.IntegerField()
    # murahal_date = models.DateField(default=timezone.now,verbose_name="تاريخ الترحيل", blank=True, null=True)
    # murahal_date = forms.DateField(default=timezone.now,label='تاريخ الترحيل')
    # date = forms.DateField(initial=datetime.date.today)
    state_date =forms.DateField(label='تاريخ تعديل الحالة', required=False,initial=datetime.date.today)





from django import forms

from documents.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        widgets = {
            'title': forms.Textarea(attrs={'rows': '1', 'class': 'span9'}),
        }


class DocumentFilterForm(forms.Form):
    """A dummy form to check the validity of GET parameters from DataTables."""
    bRegex = forms.BooleanField(required=False)
    bRegex_0 = forms.BooleanField(required=False)
    bRegex_1 = forms.BooleanField(required=False)
    bRegex_2 = forms.BooleanField(required=False)
    bRegex_3 = forms.BooleanField(required=False)
    bRegex_4 = forms.BooleanField(required=False)
    bRegex_5 = forms.BooleanField(required=False)
    bRegex_6 = forms.BooleanField(required=False)
    bRegex_7 = forms.BooleanField(required=False)
    bRegex_8 = forms.BooleanField(required=False)
    bSearchable_0 = forms.BooleanField()
    bSearchable_1 = forms.BooleanField()
    bSearchable_2 = forms.BooleanField()
    bSearchable_3 = forms.BooleanField()
    bSearchable_4 = forms.BooleanField()
    bSearchable_5 = forms.BooleanField()
    bSearchable_6 = forms.BooleanField()
    bSearchable_7 = forms.BooleanField()
    bSearchable_8 = forms.BooleanField()
    bSortable_0 = forms.BooleanField()
    bSortable_1 = forms.BooleanField()
    bSortable_2 = forms.BooleanField()
    bSortable_3 = forms.BooleanField()
    bSortable_4 = forms.BooleanField()
    bSortable_5 = forms.BooleanField()
    bSortable_6 = forms.BooleanField()
    bSortable_7 = forms.BooleanField()
    bSortable_8 = forms.BooleanField()
    iColumns = forms.IntegerField()
    iDisplayLength = forms.IntegerField()
    iDisplayStart = forms.IntegerField()
    iSortCol_0 = forms.IntegerField()
    iSortingCols = forms.IntegerField()
    mDataProp_0 = forms.IntegerField()
    mDataProp_1 = forms.IntegerField()
    mDataProp_2 = forms.IntegerField()
    mDataProp_3 = forms.IntegerField()
    mDataProp_4 = forms.IntegerField()
    mDataProp_5 = forms.IntegerField()
    mDataProp_6 = forms.IntegerField()
    mDataProp_7 = forms.IntegerField()
    mDataProp_8 = forms.IntegerField()
    sColumns = forms.CharField(required=False)
    sEcho = forms.IntegerField()
    sSearch = forms.CharField(required=False)
    sSearch_0 = forms.CharField(required=False)
    sSearch_1 = forms.CharField(required=False)
    sSearch_2 = forms.CharField(required=False)
    sSearch_3 = forms.CharField(required=False)
    sSearch_4 = forms.CharField(required=False)
    sSearch_5 = forms.CharField(required=False)
    sSearch_6 = forms.CharField(required=False)
    sSearch_7 = forms.CharField(required=False)
    sSearch_8 = forms.CharField(required=False)
    sSortDir_0 = forms.ChoiceField(choices=(('asc', 'asc'), ('desc', 'desc')))

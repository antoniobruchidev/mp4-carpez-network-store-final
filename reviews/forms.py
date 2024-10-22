from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('order',)

    line_item = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'line_item':
                self.fields[field_name].widget.attrs['type'] = 'hidden'
            if field_name == 'order':
                self.fields[field_name].widget.attrs['class'] = 'hidden'
from django import forms
from JMapp.models import customer_message

class MessageForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), required=True)
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = customer_message
        fields = ('name', 'email', 'message',)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
from django import forms
from app.models import Train, Station


class TrainForm(forms.ModelForm):  
    class Meta:
        # model = forms.ModelChoiceField(queryset=Train.objects.all(), required=True)
        model = Train
        fields = ('source', 'destination', 'class_type')


    def __init__(self, *args, **kwargs):
        super(TrainForm, self).__init__(*args, **kwargs)
        self.fields['source'].empty_label = "Select"
        self.fields['source'].required = True
        self.fields['destination'].empty_label = "Select"
        self.fields['destination'].required = True
        

# class ClassTypeForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ('name',)
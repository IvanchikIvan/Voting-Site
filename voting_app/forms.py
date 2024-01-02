from django import forms
from .models import Voting, Option

class VotingForm(forms.ModelForm):
    options = forms.CharField(widget=forms.TextInput(attrs={'class': 'option-field'}))
    class Meta:
        model = Voting
        fields = ['title', 'description', 'options']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VotingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        voting = super(VotingForm, self).save(commit=False)
        voting.author = self.request.user
        voting.save()
        print(self.cleaned_data['options'])
        options = self.cleaned_data['options'].split('\n')
        for option_text in options:
            Option.objects.create(voting_id=voting, content=option_text.strip())

        return voting

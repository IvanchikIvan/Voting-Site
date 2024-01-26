from django import forms
from .models import Voting, Option

class VotingForm(forms.ModelForm):
    voting_type = forms.ChoiceField(
        choices=[('single', 'One of Many'), ('multiple', 'Multiple Choices')],
        widget=forms.RadioSelect(),
        initial='single'
    )

    class Meta:
        model = Voting
        fields = ['title', 'description', 'image', 'voting_type']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VotingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        voting = super(VotingForm, self).save(commit=False)
        if self.request:
            voting.author = self.request.user
        voting.save()

        options_input = self.data.getlist('option-field')
        for option_text in options_input:
            Option.objects.create(voting_id=voting, content=option_text.strip())

        return voting

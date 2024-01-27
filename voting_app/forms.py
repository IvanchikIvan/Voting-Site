from django import forms
from .models import Claim, Voting, Option

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


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['body', 'voting']

    def __init__(self, user, *args, **kwargs):
        super(ClaimForm, self).__init__(*args, **kwargs)
        self.fields['voting'].queryset = Voting.objects.filter(author=user)
        self.fields['voting'].widget = forms.HiddenInput()  # Скрыть поле voting, так как значение уже установлено

    def clean_voting(self):
        return self.cleaned_data['voting']

    def save(self, commit=True):
        claim = super(ClaimForm, self).save(commit=False)
        claim.user = self.user
        if commit:
            claim.save()
        return claim

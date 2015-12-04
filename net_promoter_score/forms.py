# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import AnonymousUser

from net_promoter_score.models import PromoterScore


class PromoterScoreForm(forms.ModelForm):

    """Form for capturing NPS score."""

    reason = forms.CharField(max_length=512, required=False)

    def __init__(self, *args, **kwargs):
        assert 'user' in kwargs, u"Score must have a valid user."
        self.user = kwargs.pop('user')
        super(PromoterScoreForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PromoterScore
        fields = ('score', 'reason')
        exclude = ('user', )

    def clean_score(self):
        score = self.cleaned_data['score']
        if score < -1 or score > 10:
            raise forms.ValidationError("Score must be between 0-10")
        return score

    def save(self, commit=True):
        """Set the user attr of the score."""
        score = super(PromoterScoreForm, self).save(commit=False)
        score.user = self.user
        return score.save()

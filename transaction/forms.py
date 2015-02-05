from django import forms

HOUSE_TYPE_CHOICES = (
    ('', 'All'),
    ('h', 'HDB'),
    ('c', 'Condo'),
)

ROOM_CHOICES = [('', 'All')] + [(i, i) for i in range(1, 9)] + [('u', 'Unknown')]


class FilterForm(forms.Form):
    type = forms.ChoiceField(label="Type", choices=HOUSE_TYPE_CHOICES, required=False)
    name = forms.CharField(label="HouseName", widget=forms.TextInput(), required=False)
    postal_code = forms.CharField(label="PostalCode", widget=forms.TextInput(), required=False)
    address = forms.CharField(label="Address", widget=forms.TextInput(), required=False)
    room_count = forms.ChoiceField(label="No.Bedroom", choices=ROOM_CHOICES, required=False)

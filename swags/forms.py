from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Swag
from django.forms.widgets import NumberInput
from django.utils.safestring import mark_safe

class StarRatingWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = f'<div class="star-rating">'
        html += f'<input type="hidden" name="{name}" id="id_{name}" value="{value or 5}">'

        # Create stars with full-star increments only
        for i in range(5, 0, -1):  # 5 to 1 for full-star increments (reversed to match rtl display)
            star_value = i
            checked = 'checked' if value and int(float(value)) >= star_value else ''
            html += f'''
            <input type="radio" id="star-{i}" name="star-{name}" value="{star_value}" {checked}
                onclick="document.getElementById('id_{name}').value = this.value;">
            <label for="star-{i}" title="{star_value} stars"></label>
            '''

        html += '</div>'

        # Add CSS for star rating
        html += '''
        <style>
            .star-rating {
                display: inline-block;
                direction: rtl;  /* Right to left for proper star filling */
            }
            .star-rating input[type="radio"] {
                display: none;
            }
            .star-rating label {
                color: #ddd;
                font-size: 1.5em;
                padding: 0;
                cursor: pointer;
                width: 1em;
                overflow: hidden;
            }
            .star-rating label:before {
                content: '★';
            }
            .star-rating input[type="radio"]:checked ~ label,
            .star-rating input[type="radio"]:hover ~ label {
                color: #ffc107;
            }
        </style>
        '''

        return mark_safe(html)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SwagForm(forms.ModelForm):
    class Meta:
        model = Swag
        fields = ['name', 'photo', 'company', 'conference', 'rating', 'comments']
        widgets = {
            'rating': StarRatingWidget(),
        }

class SwagSearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search swags...'})
    )

from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post, Experience, Education

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
        
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'start_date', 'end_date', 'description']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter position'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter description'}),
        }
        labels = {
            'company': 'Company Name',
            'position': 'Position',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'major', 'start_date', 'end_date']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Name of Institution'}),
            'degree': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Degree'}),
            'major': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Major'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control mb-3', 'type': 'date', 'placeholder': 'Start Date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control mb-3', 'type': 'date', 'placeholder': 'End Date'}),
        }

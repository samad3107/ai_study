# core/forms.py
from django import forms
from .models import UserNote

class PDFUploadForm(forms.ModelForm):
    """Form for uploading a PDF file and providing a title."""
    
    pdf_file = forms.FileField(
        label='Upload PDF Notes',
        help_text='Max file size 50MB. Only PDF files allowed.',
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf'})
    )
    
    class Meta:
        model = UserNote
        fields = ['title', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a title for your notes'}),
        }

class TopicForm(forms.Form):
    """Simple form for users to input a topic."""
    topic_name = forms.CharField(
        label='Enter Topic Name',
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., Quantum Entanglement, The Water Cycle, The French Revolution',
            'class': 'w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 futuristic-text'
        })
    )
from django import forms
from .models import Book

class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'



class SelectBookForm(forms.Form):
    class Meta:
        model = Book
        book = forms.ModelChoiceField(
            queryset=Book.objects.all(),
            to_field_name='pk',  # Use the book's primary key as the field value
            label="Select a Book to Update"
        )






class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book  # Associate the form with the Book model
        fields = ['id']  ##'__all__' You can specify specific fields if needed

        selected_book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        empty_label=None, # example to add label
        widget=forms.Select(attrs={'class': 'form-control'}))  # example to add widgets
    
class ConfirmBookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    published_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})) # this outputs a date widget in the template '{{update_form.published_date}}' if you include it it must be filled in!


"""
NOTE -from customisations
select fields 
    fields = ['title', 'author', 'published_date']

exlude fields
    exclude = ['published_date']  

customise widget 
    widgets = {
    'description': forms.Textarea(attrs={'rows': 4, 'cols': 40})}

custom validation
    def clean_title(self):
    # Custom validation for the 'title' field
    title = self.cleaned_data['title']
    if not title.isalnum():
    raise forms.ValidationError("Title should only contain alphanumeric characters.")
    return title

help text and labels
    labels = {'title': 'Book Title'}
    help_texts = {'author': 'The author of the book.'}

overriding the default form render to custom template
      template_name = 'custom_form_template.html'
"""
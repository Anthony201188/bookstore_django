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
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}))  
    









""" class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
       # fields = '__all__'  # Use '__all__' to include all fields in the form
        fields = ['title']
        def __init__(self, *args, **kwargs):
            book_instance = kwargs.pop('book_instance', None) # calls the inherited method and adds the book instance to the constructor of this class removing the key from the passed kwargs dict.
            super(UpdateBookForm, self).__init__(*args, **kwargs)
            
            # Pre-fill the form with data from the selected book instance
            if book_instance:
                for field in self.fields:
                    self.fields[field].initial = getattr(book_instance, field) #fields.[fields] refers to the fields dict from djangos forms.Form class and the [fields] refers to the fields in the model
    
        def save(self, commit=True): #commit saves changes instantly
            instance = super(UpdateBookForm, self).save(commit=False) # returns an instance of the model with the updated data
    
            # Update the fields with the new data
            if commit:
                instance.save()
            return instance """



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
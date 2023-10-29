from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, FormView 
from django.views.generic.list import ListView 
from django.views.generic import DetailView ,View
from django.contrib.auth.views import LoginView, LogoutView
from .models import Book
from .forms import CreateBookForm, SelectBookForm, UpdateBookForm, ConfirmBookUpdateForm
from django.urls import reverse_lazy
from django.http import  HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

class BookListView(ListView):
    model = Book
    template_name = 'book-list-template.html' 
    context_object_name = 'books' #<- used for the context name in the template. 

class BookDetailView(DetailView):
    model = Book
    template_name = 'book-detail-template.html'
    context_object_name = 'book_details' # variable name in the template

    """ 
    NOTE -
    method 1 for selection of what details to display
        def get_queryset(self):
        # Customize the queryset to select specific fields
        return YourModel.objects.only('field1', 'field2')

    method 2 
        def get_object(self):
        # Override get_object to select specific fields
        obj = super().get_object()
        obj.field3 = obj.field3  # Include field3 if needed
        return obj
    """

class BookCreateView(CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'book-create-template.html'
    success_url = reverse_lazy('book-list') # use revervse lazy to redirect to book view to see updates

class BookUpdateView(FormView):
    model = Book
    template_name = 'book-update-template.html'
    form_class = UpdateBookForm

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        print("form invalid",form) 
        return self.render_to_response(self.get_context_data(form=form))
    
    def form_valid(self, form):
        # Access the selected_book from the POST data
        selected_book_pk = self.request.POST.get('selected_book')

        return redirect('book-update-confirm', pk=selected_book_pk)   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context
    

class BookUpdateConfirmView(View):
    template_name = 'book-update-confirm-template.html'

    def get(self, request, pk):
        selected_book = Book.objects.get(pk=pk)
        update_form = ConfirmBookUpdateForm(instance=selected_book)
        return render(request, self.template_name,
                {'selected_book': selected_book, 'update_form': update_form}
                )

    def post(self, request, pk):
        selected_book = Book.objects.get(pk=pk)
        updated_form = ConfirmBookUpdateForm(request.POST, instance=selected_book)

        if updated_form.is_valid():
            updated_form.save()
            return redirect('book-list')

        return render(request, self.template_name, 
                      {'selected_book': selected_book, 'updated_form': updated_form})
    

class BookDeleteView(FormView):
    model = Book
    context_object_name = 'books'
    template_name = 'book-delete-template.html'
    form_class = SelectBookForm
    success_url = reverse_lazy('book-delete-confirm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()  # Query the Book model and pass the queryset
        return context
    
    def post(self, request):
        #get the primary key from the form post dict named 'book'
        primary_key = request.POST.get('book')

        #pass the primary_key value to the delete views url using HTTPResponseRedirect
        second_view_url = reverse_lazy('book-delete-confirm', kwargs={'pk': primary_key}) 

        return HttpResponseRedirect(second_view_url)



class BookDeleteConfirmView(DeleteView):
    model = Book
    template_name = 'book-delete-confirm-template.html'
    success_url = reverse_lazy('book-list')

    def form_valid(self, form):
        self.object = self.get_object() # get object collects the pk from the url
        self.object.delete()
        return HttpResponseRedirect(self.success_url)
    
class BookLoginView(LoginView):
    template_name = 'login.html'

class BookLogoutView(LogoutView):
    template_name = 'logout.html'

    #method 1 for dynamic user name display doesnt work
    #this is becasue the user is logged out before the re-direct 
    # def get_context_data(self, **kwargs: Any):
    #     context = super().get_context_data(**kwargs)
    #     context['user'] = self.request.user
    #     return context

    # method 2 using messages framework
    def get(self, request, *args, **kwargs):
        
        messages.success(request, 'You have been logged out successfully.') # uses the {%messages%}{{message}} tags, see logout.html for full standard use
        return super().get(request, *args, **kwargs)

class LoggedinBookListView(BookListView):
    """ extends from book list with welcome and log out options """
    template_name = 'logged-in-book-list-template.html'


    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user # get the user data from the http request 
       #context['key'] = value <- this syntax is context(dictname), ['dictval'], =value to add.
       # its the baisc syntax to add values to dicts
        return context
    

class SignUpView(CreateView):
    form_class = UserCreationForm # built in method from the auth model
    success_url = reverse_lazy('login')
    template_name = 'sign-up.html'





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import List

from django.views.generic import FormView, CreateView, DetailView, ListView, UpdateView

User = get_user_model()


class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm


class ViewAndAddToList(DetailView, CreateView):
    model = List
    template_name = 'list.html'
    form_class = ExistingListItemForm

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return self.form_class(for_list=self.object, data=self.request.POST)


class NewListView(CreateView):
    form_class = NewListForm
    template_name = 'home.html'

    def form_valid(self, form):
        list_ = form.save(owner=self.request.user)
        return redirect(list_)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})

class MyListsView(ListView):
    template_name = "my_lists.html"

    def get_queryset(self):
        self.owner = get_object_or_404(User, email=self.kwargs['email'])
        self.shared_list =  List.objects.filter(shared_with=self.owner)
        return self.shared_list

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['owner'] = self.owner
        context['shared_list'] = self.shared_list
        return context


# Here, maybe it is not worth it to change to cbv
def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        email = request.POST['sharee']
        list_.shared_with.add(email)
        return redirect(list_)
        

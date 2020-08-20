from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import List

from django.views.generic import FormView, CreateView, DetailView

User = get_user_model()

class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm

# class ViewAndAddToList(DetailView):
#     model = List

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "list.html", {"list": list_, "form": form})

def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        email = request.POST['sharee']
        list_.shared_with.add(email)
        return redirect(list_)

class NewListView(CreateView):
    form_class = NewListForm
    template_name = 'home.html'

    def form_valid(self, form):
        list_ = form.save(owner=self.request.user)
        return redirect(list_)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})

        
def my_lists(request, email):
    owner = User.objects.get(email=email)
    shared_list = List.objects.filter(shared_with=owner)
    return render(request, 'my_lists.html', {'owner': owner, 'shared_list': shared_list})

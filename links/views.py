from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import Link
from .forms import AddLinkForm
from django.views.generic import DeleteView


# Create your views here.
'''
For our home view e need to pass to the template:
- qs
- number of items
- number of items discounted
- form
-error (if exists)
'''

def home_view(request):
    no_discounted = 0
    error = None

    form = AddLinkForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("links.views.home_view"))
        except AttributeError:
            error = "Opps.. coudn't get the name or the price!!"
        except:
            error = "Ops... something went wrong"

    form = AddLinkForm()

    qs = Link.objects.all()
    items_no = qs.count()

    if items_no > 0:
        discount_list = []
        for item in qs:
            if item.old_price > item.current_price:
                discount_list.append(item)
            no_discounted = len(discount_list)
            # print(no_discounted)
    

    context = {
        'qs':qs,
        'items_no': items_no,
        'no_discounted': no_discounted,
        'form':form,
        'error':error,
    }

    return render(request, 'links/main.html',context)

class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'links/confirmDel.html'
    success_url = reverse_lazy('home-view')

def UpdatePrices(request):
    qs = Link.objects.all()
    for link in qs:
        link.save()
    return redirect('home-view')
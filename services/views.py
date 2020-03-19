from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from pool.models import *
from .forms import ServiceCreationForm, FoodCreationForm,newFoodCreationForm
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# class FoodCreateView(LoginRequiredMixin, FormView):
#     form_class= FoodCreationForm
#     success_url = '/'
#     template_name = 'services/foodcreate.html'
#
#     def form_valid(self, form):
#         form.save(self.request.user)
#         return super().form_valid(form)


class FoodCreateView(LoginRequiredMixin, FormView):
    form_class= newFoodCreationForm
    success_url = '/'
    template_name = 'services/foodcreate.html'

    def form_valid(self, form):
        u = self.request.user
        data = form.save()
        f = FoodService(category=Category.objects.get(name='Food'), initiator=u, vendor=data['vendor'], description=data['description'],
                        start_time=data['start_time'], end_time=data['end_time'], slackness=data['slackness'], stype='Food')
        f.save()
        sm = ServiceMember(service=f, user=u)
        sm.save()
        # form.save(self.request.user)
        return super().form_valid(form)




# @login_required
# class ServiceCreateView(FormView):
#
#     # model = Service
#     form_class = ServiceCreationForm
#     success_url = '/'
#     template_name = 'services/create.html'
#
#
#     def get_success_url(self):
#         return self.success_url
#
#     def post(self, request, *args, **kwargs):
#
#         service_create_form = ServiceCreationForm(data=request.POST)
#
#         if service_create_form.is_valid():
#             service_create_form.save(commit=True)
#             return redirect('pool:home')
#         else:
#             print(service_create_form.errors)
#             return render(request, 'services/create.html', {'form_cat': service_create_form})
#
#
#     # fields=['name','description']
#
#     # # def get_initial(self):
#     # #     initial=super(GroupCreateView,self).get_initial()
#     # #     initial['admin_id']=self.request.user.id
#     # #     return initial
#     # def form_valid(self, form):
#     #     form.instance.admin=User.objects.get(id=self.request.user.id)
#     #     return super(GroupCreateView,self).form_valid(form)
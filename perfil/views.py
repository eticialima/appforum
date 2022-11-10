from django.core.paginator import Paginator
from django.http import HttpResponseRedirect 
from django.shortcuts import redirect
from django.urls import reverse_lazy 
from django.contrib import messages
from django.views.generic.base import View  
from django.views.generic.edit import CreateView 
from accounts.forms import CustomUserCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from base.base_admin_permissions import BaseAdminUsersAd 
from django.views.generic import TemplateView, DetailView, UpdateView, ListView 
from perfil.models import Network, Profile
from accounts.models import CustomUser 
from post.models import Post 

 
class ProfileView(DetailView):
    model = CustomUser
    template_name = "profile/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "perfil"
    object = None   
    
    def get_object(self, queryset=None):
        self.perfil = self.model.objects.select_related('profile').prefetch_related("posts").prefetch_related("network").get(user_name=self.kwargs.get(self.slug_url_kwarg)) 
        return self.perfil

    def get(self, request, *args, **kwargs):
        self.object = self.get_object() 
        context = self.get_context_data(object=self.object) 
        page = self.request.GET.get('page')    
        title = request.GET.get('title') 
        if title: 
            context['page_obj'] = Paginator(Post.objects.all().filter(title__icontains=title, author=self.object, is_activate__exact=True), 6).get_page(page) 
            print("resultado filtro !!!") 
            print(context['page_obj'])
        else: 
            context['page_obj'] = Paginator(Post.objects.all().filter(author=self.object, is_activate__exact=True), 6).get_page(page)
            print("Todos os filtros !!!") 
        return self.render_to_response(context) 



class ProfileEditView(UpdateView):
    model = Profile
    template_name = "config/edit-profile.html"
    context_object_name = "profile"
    object = None
    fields = "__all__"

    def get_object(self, queryset=None):
        return self.request.user.profile 

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['network'] = Network.objects.filter(user=self.request.user)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        print(request.POST.get('first_name'))
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name') 
        user.save()
        profile = user.profile
        profile.about = request.POST.get('about')
        profile.occupation = request.POST.get('occupation')
        profile.description = request.POST.get('description') 
        if request.POST.get('gender') == "Homem":
            profile.gender = "Homem"
        else:
            profile.gender = "Mulher"
        profile.country = request.POST.get('country')
        profile.city = request.POST.get('city')
        profile.phone = request.POST.get('phone')
        profile.save()
        networks = Network.objects.filter(user=self.request.user) 
        urls = request.POST.getlist('url') 
        for network, url in zip(networks, urls):
            network.url = url
            network.save()
        messages.success(self.request, 'Changes saved successfully!!!')
        return redirect(reverse_lazy('profile:edit-profile'))


class EditPhotoProfile(UpdateView):
    model = Profile
    template_name = "profile/profile.html"
    template_name_suffix = '_update_form'  
    fields = ['image'] 
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):  
        messages.success(self.request, 'Profile image successfully updated!!!')
        return reverse_lazy('profile:user-profile', args=[self.request.user.user_name])


class ProfileAddLike(LoginRequiredMixin, View):
    login_url = '/accounts/login/'  
    redirect_field_name = 'redirect_to'
    slug_field = "username"
    slug_url_kwarg = "username"

    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        is_like = False
        for like in profile.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            profile.likes.add(request.user)

        if is_like:
            profile.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        

class ConfigView(TemplateView):
    template_name = "config/_config.html"


class UserListView(BaseAdminUsersAd, ListView):
    model = Profile
    template_name = 'config/usuarios.html'  
    context_object_name = 'profile_list' 
    
    def get_queryset(self):      
        user_name = self.request.GET.get('user_name') 
        is_active = self.request.GET.get('is_active') 
        if user_name:  
            profile_list = Profile.objects.filter(user__user_name__icontains=user_name) 
            return profile_list
        if is_active:
            profile_list = Profile.objects.filter(user__is_active=is_active)        
            return profile_list
        else:
            profile_list = Profile.objects.filter() 
        return profile_list   
    
    
class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreateForm
    template_name = 'config/add-user.html'
    success_url = reverse_lazy('profile:users-profile')
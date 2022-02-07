from django.urls import reverse_lazy
from django.contrib import messages
from base.base_admin_permissions import BaseAdminUsersAd, BaseAdminUsersall
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView 
from post.models import Post  
from post.forms import PostForm 
from accounts.models import CustomUser
from django.shortcuts import render
from django.template.defaultfilters import slugify  


class PostView(BaseAdminUsersall, ListView):
        model = Post
        template_name = 'post/post.html'
        context_object_name = "post_disable"
        
        def get_queryset(self): 
                query = self.request.GET.get('title')
                query2 = self.request.GET.get('is_activate')   
                if query:
                        post_list = self.model.objects.filter(title__icontains=query)
                        return post_list
                if query2:
                        post_list = self.model.objects.filter(is_activate__icontains=query2)
                        return post_list
                else: 
                        post_list = self.model.objects.all()
                return post_list
                

class TodosPostView(BaseAdminUsersAd, ListView):
        model = Post
        template_name = 'post/post.html'
        context_object_name = "post_todos"

        def get_queryset(self):
                query = self.request.GET.get('title')
                query2 = self.request.GET.get('is_activate')
                if query:
                        post_list = self.model.objects.filter(
                                title__icontains=query)
                        return post_list
                if query2:
                        post_list = self.model.objects.filter(is_activate__icontains=query2)
                        return post_list
                else:
                        post_list = self.model.objects.all()
                return post_list
 
 
class PostCreate(BaseAdminUsersall, CreateView):
        model = Post
        form_class = PostForm
        template_name = 'post/post_create.html'

        def get(self, request):
                form = PostForm()
                posts = Post.objects.all() 
                common_tags = Post.tags.most_common()[:4]
                context = {'posts': posts, 'common_tags': common_tags, 'form': form}
                return render(request, 'post/post_create.html', context)

        def post(self, request, *args, **kwargs):
                user_pk = request.user
                user = CustomUser.objects.filter(username=user_pk) 
                form = PostForm(request.POST, request.FILES) 
                if 'btn_adicionar':
                        if form.is_valid():
                                form_model = form.save(commit=False)
                                form_model.slug = slugify(form_model.title)
                                form_model.author = user[0]
                                form_model.save()
                                form.save_m2m()  
                                return self.form_valid(form)
                        else:
                                return self.form_invalid(form)
        
        def get_success_url(self) -> str:
                messages.success(self.request, 'O post foi Cadastrado com sucesso')
                return reverse_lazy('home:home')


class PostUpdate(BaseAdminUsersall, UpdateView):
        model = Post
        form_class = PostForm
        template_name = 'post/post_update.html'    

        def get_success_url(self):  
                messages.success(self.request, 'Post atualizada com sucesso!!!')
                return reverse_lazy('profile:user-profile', args=[self.request.user.user_name])


class PostDelete(BaseAdminUsersall, DeleteView):
        model = Post
        form_class = PostForm
        template_name = 'post/post_delete.html'
        success_url = reverse_lazy('post')
        success_message = 'O post foi deletado com sucesso'
 
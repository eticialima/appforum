from django.urls import path 
from post.views import (PostView, PostCreate, PostUpdate, PostDelete, TodosPostView) 

urlpatterns = [  
	path('post/', PostView.as_view(), name='post'), 
	path('post-create/', PostCreate.as_view(), name='post-create'),   
	path('<int:pk>/post-update/', PostUpdate.as_view(), name='post-update'),  
 	path('<int:pk>/post-delete/', PostDelete.as_view(), name='post-delete'), 
        path('todos/', TodosPostView.as_view(), name='post-todos'), 
]
#coding:utf-8
import markdown
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from comments.forms import CommentForm
from .models import Post,Category
from django.views.generic import ListView,DetailView





# Create your views here.
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
'''
def index(request):
	post_list = Post.objects.all().order_by('-create_time')
	return render(request,'blog/index.html',context={'post_list':post_list})
	'''
'''
	return  render(request,'blog/index.html',context ={
			'title':'我的博客首页',
			'welcome':'欢迎访问我的博客首页'

		})
'''
'''
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    #当有用户访问某篇文章时，阅读量加1
    post.increase_views()
    
    #extra:包含很多扩展
	#codehilite:使得文字语法高亮
	#toc：自动生成目录
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post':post,
    			'form':form,
    			'comment_list':comment_list
    }
    return render(request, 'blog/detail.html', context=context)
'''
class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'

	#重写get（）方法,以实现对阅读量的递增
	def get(self,request,*args,**kwargs):
		response = super(PostDetailView,self).get(request,*args,**kwargs)

		#将阅读量+1
		self.object.increase_views()
		return response

	#重写get_object()以实现对post的body进行渲染
	def get_object(self,queryset = None):
		post = super(PostDetailView,self).get_object(queryset=None)
		post.body = markdown.markdown(post.body,extensions = [
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			'markdown.extensions.toc',
			])
		return post

	def get_context_data(self,**kwargs):
		context = super(PostDetailView,self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
			'form':form,
			'comment_list':comment_list
			})
		return context







'''
def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
 '''
class ArchivesView(ListView):
 	model = Post
 	template_name = 'blog/index.html'
 	context_object_name = 'post_list'

 	def get_queryset(self):
 		year = self.kwargs.get('year')
 		month = self.kwargs.get('month')
 		return super(ArchivesView,self).get_queryset().filter(create_time__year=year,
 															create_time__month=month)


'''
def category(request,pk):
	cate =  get_object_or_404(Category,pk=pk)
	post_list = Post.objects.filter(category=cate).order_by('-create_time')
	return render(request,'blog/index.html',context = {'post_list':post_list})
'''
class CategoryView(IndexView):
	def get_queryset(self):
		cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
		return super(CategoryView,self).get_queryset().filter(category = cate)

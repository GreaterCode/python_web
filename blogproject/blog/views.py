#coding:utf-8
import markdown
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from comments.forms import CommentForm
from .models import Post,Category
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator




# Create your views here.
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	#开启分页功能
	paginate_by = 2

	def get_context_data(self,**kwargs):
		#获取父类生成的传递给模版的字典
		context = super().get_context_data(**kwargs)	
		
		#从父类的字典中获取paginator、page_obj、is_paginated
		#paginator：Paginator的一个实例
		#page_obj:Page的实例
		#is_paginated:指示是否已经分页
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

		#调用自己实现的pagination_data获取显示分页的内容
		pagination_data = self.pagination_data(paginator,page,is_paginated)

		#将分页导航条的模板变量更新到context中
		context.update(pagination_data)

		#返回更新后的context
		return context

	def pagination_data(self,paginator,page,is_paginated):
		if not is_paginated:
			#若无分页，则无需显示分页导航条
			return {}

		#当前页左边连续的页码号，初值为空
		left = []

		#当前页右边连续的页码号，初值为空
		right = []

		#标识第一页页码后面是否需要省略号
		left_has_more = False

		#标识最后一页前是否需要省略号
		right_has_more = False
    	
    	#标识是否需要显示第一页
		first = False

		#标识是否需要显示最后一页
		last = False

		#获得用户当前请求的页码号
		page_number = page.number

		#获得分页后的总页数
		total_pages = paginator.num_pages

		#获得整个分页页码列表，如[1,2,3,4,5]
		page_range = paginator.page_range

		if page_number == 1:
			#获取当前页右边的连续页码号
			right = page_range[page_number:page_number+1]
			#如果最右边的页码比倒数第二页小，则需显示省略号
			if right[-1] < total_pages -1:
				right_has_more = True
			
			#若最右边页码比最后一页还小，则显示最后一页页码
			if right[-1] < total_pages:
				last = True
		elif page_number == total_pages:
			#如果用户请求最后一页,
			if (page_number - 3) > 0:
				left = page_range[page_number - 3:page_number -1]
			else:
				left = 0

			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True
		else:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_number[page_number:page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			if left[0] > 2:
				left_has_more = True

			if left[0] > 1:
				first = True
		data = {
		'left':left,
		'right':right,
		'left_has_more':left_has_more,
		'right_has_more':right_has_more,
		'first':first,
		'last':last,

		}

		return data






					








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

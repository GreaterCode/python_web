from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags
import markdown

# Create your models here.

# python_2_unicode_compatible 用于python2
@python_2_unicode_compatible
class Category(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length = 100)

		
@python_2_unicode_compatible
class Tag(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length = 100)


@python_2_unicode_compatible
class Post(models.Model):
	#文章标题
	title = models.CharField(max_length = 70)

	#文章内容
	body = models.TextField()

	#文章创建时间
	create_time = models.DateTimeField()

	#文章修改时间
	modified_time = models.DateTimeField()

	#文章摘要
	excerpt = models.CharField(max_length = 200,blank = True)

	#阅读量
	views = models.PositiveIntegerField(default = 0)

	#分类
	category = models.ForeignKey(Category)
	
	#标签
	tags = models.ManyToManyField(Tag,blank = True)

	#user
	author = models.ForeignKey(User)

	def __str__(self):
		return self.title

	# 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})

	def increase_views(self):
		self.views += 1
		self.save(update_fields = ['views'])

	class Meta:
		ordering = ['-create_time']
  
    #文章自动生成摘要信息
    #方法一：复写save方法
	def save(self,*args,**kwargs):
    	#如果没有填写摘要
		if not self.excerpt:
    		#实例化一个markdown实例，去渲染文章文本
			md = markdown.Markdown(extensions = [
    			'markdown.extensions.extra',
    			'markdown.extensions.codehilite',
    			])
    		#首先将markdown文本渲染成html文本，然后去掉html文本中的
			#html标签，然后取前54个字符为文章摘要
			self.excerpt = strip_tags(md.convert(self.body))[:54]

		#调用父类save方法，将数据保存至数据库中
		super(Post,self).save(*args,**kwargs)    
	#方法二：使用truncatechars模本过滤器
	#详见index.html中post.body | truncatechars:54




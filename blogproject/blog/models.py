from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

# Create your models here.

# python_2_unicode_compatible 用于金融港python2
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
	def __str__(self):
		return self.title
	# 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})
	def increase_views(self):
		self.views += 1
		self.save(update_field = ['views'])

	title = models.CharField(max_length = 70)
	body = models.TextField()
	create_time = models.DateTimeField()
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
	class Meta:
		ordering = ['-create_time']



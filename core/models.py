from django.db import models
import markdown

md = markdown.Markdown()

def parse_markdown(markdown_source):
    html = md.convert(markdown_source)
    return html


class Project(models.Model):
	title = models.CharField(max_length=300)
	description = models.TextField()
	files = models.ManyToManyField("ProjectFile", blank=True)
	completed = models.BooleanField(default=False)
	published = models.BooleanField(default=False)

	@property
	def image(self):
		img = None
		for file in self.files.all():
			if file.file_type == 'image':
				img = file
				break
		return img.file

	@property
	def images(self):
		return self.files.all().filter(file_type='image')

	@property
	def videos(self):
		return self.files.all().filter(file_type='video')


	def parse_markdown_to_html(self):
		if not self.id:
			raise Exception("Cannot perform parsing on unsaved instance")
		html_content = parse_markdown(self.description)
		return html_content

	@property
	def html(self):
		return self.parse_markdown_to_html()
	

	def __str__(self):
		return self.title


class ProjectFile(models.Model):
	project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
	file_type = models.CharField(max_length=10, choices=(('image', 'Image'), ('video', 'Video')), default='image')
	file = models.FileField(upload_to='projects/')

	def __str__(self):
		return self.project_id.title + ' - ' + self.file_type + str(self.position)

	@property
	def position(self):
		count = 1
		for image in self.project_id.images:
			if not image == self:
				count += 1
			break
		return count


class FileObject(models.Model):
	file = models.FileField(upload_to='files/')

	def file_type(self):
		return self.file.name.split('.')[-1]


class Solution(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	files = models.ManyToManyField(FileObject, blank=True)

	def __str__(self):
		return self.name

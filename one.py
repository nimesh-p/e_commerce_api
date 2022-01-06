from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from app.constants import StatusConstants, FileTypeConstants, RatingConstants, NonEmployeeConstants


def validate_name(value):
    if TechnologyStack.objects.filter(name__iexact=value).exists():
        raise ValidationError("Technology already exists")
    return value

class Department(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Designation(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class TechnologyStack(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[validate_name])

    def __str__(self):
        return str(self.name)

class Topic(models.Model):
    topic_name = models.CharField(max_length=100, null=True, blank=True)
    technology_stack = models.ForeignKey(TechnologyStack, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.topic_name


class User(AbstractUser):
    """Custom user model that supports email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=255, null=True, blank=True)

    past_experience = models.FloatField(default=0, null=True, blank=True)

    files = GenericRelation("FileStorage", content_type_field='content_type', object_id_field='object_id')

    # objects = UserManager()
    # u.technology_stack.all().values("employeetechnologyrating__rating")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.email)

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joining_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    technology_stack = models.ManyToManyField(TechnologyStack, through="EmployeeTechnologyRating", related_name="employee_technology")

    is_current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    @classmethod
    def get(cls, id):
        return UserDetails.objects.get(id=id)

    def get_designation(self):
        return self.designation.name

    @property
    def is_employee(self):
        designation = self.get_designation()
        return not designation in NonEmployeeConstants.get_values()

class EmployeeTechnologyRating(models.Model):
    technology_stack = models.ForeignKey(TechnologyStack, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    rating = models.CharField(max_length=255, choices=RatingConstants.get_choices(), default=RatingConstants.AVERAGE.value)

    def __str__(self):
        return str(self.technology_stack) +  "/" + str(self.user) + "/" + str(self.rating)


class Project(models.Model):
    title = models.CharField(max_length=80)
    user = models.ManyToManyField(User, through="UserProject")
    status = models.CharField(max_length=7, choices=StatusConstants.get_choices(), default=StatusConstants.CREATED.value)
    project_start_date = models.DateField(null=True, blank=True)
    project_end_date = models.DateField(null=True, blank=True)
    technology_stack = models.ManyToManyField(TechnologyStack, related_name="project_technology")
    description = models.TextField(null=True, blank=True)

    files = GenericRelation("FileStorage", content_type_field='content_type', object_id_field='object_id')


    class Meta:
        ordering = ['title']

    def __str__(self):
        return (self.title)

class ProjectRole(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return (self.name)

class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    user_active_date = models.DateField(null=True, blank=True)
    user_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return (self.role)

class ReferenceLinks(models.Model):
    links = models.URLField(null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return (self.links)

class FileType(models.Model):
    name = models.CharField(max_length=20, choices=FileTypeConstants.get_choices(), default=FileTypeConstants.DOCUMENT.value)

    @classmethod
    def get_file_by_name(cls, name):
        return FileType.objects.get(name= 'Document')

class FileStorage(models.Model):

    file = models.FileField(upload_to="files/%Y/%m/%d")
    file_type = models.ForeignKey(FileType, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.file)



# class Sprint(models.Model):
#     name = models.CharField(max_length=50, blank=True, null=True)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     status = models.CharField(max_length=30, choices=STATUS, blank=True, null=True)

#     def __str__(self):
#         return (self.name)
from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    github = models.URLField()
    linkedin = models.URLField()
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='profile/')

    def __str__(self):
        return self.name



class Project(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    tech_stack = models.CharField(
        max_length=200,
        help_text="Example: Python, Django, AI"
    )

    key_features = models.TextField(
        blank=True,
        help_text="Comma-separated features (e.g. Smart Integration, Cloud Setup)"
    )

    image = models.ImageField(upload_to='projects/')

    project_url = models.URLField(blank=True)

    github_url = models.URLField(blank=True)

    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: AI, Web Development, Cybersecurity"
    )

    featured = models.BooleanField(
        default=False,
        help_text="Show this project in featured section"
    )

    order = models.IntegerField(
        default=0,
        help_text="Display order of projects"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
class About(models.Model):

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()

    profile_image = models.ImageField(upload_to="about/")

    skills_tags = models.TextField(blank=True, help_text="Comma-separated tags (e.g. AI, Python, C++)")
    focus_areas = models.TextField(blank=True, help_text="Comma-separated focus areas (e.g. AI System Development, Financial AI)")

    email = models.EmailField()
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    location = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Skill(models.Model):

    name = models.CharField(max_length=100)
    level = models.IntegerField(help_text="Skill level in percentage")

    def __str__(self):
        return self.name
    
class Experience(models.Model):

    company = models.CharField(max_length=200)

    role = models.CharField(max_length=200)

    description = models.TextField()

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    company_logo = models.ImageField(upload_to="experience/", blank=True)

    def __str__(self):
        return f"{self.role} at {self.company}"
    
class Education(models.Model):

    institution = models.CharField(max_length=200)

    degree = models.CharField(max_length=200)

    field_of_study = models.CharField(max_length=200)

    start_year = models.IntegerField()
    end_year = models.IntegerField()

    grade = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
class Certificate(models.Model):

    title = models.CharField(max_length=200)

    organization = models.CharField(max_length=200)

    certificate_image = models.ImageField(upload_to="certificates/")

    certificate_url = models.URLField(blank=True)

    issue_date = models.DateField()

    def __str__(self):
        return self.title
    
class Resume(models.Model):

    title = models.CharField(max_length=200)

    resume_file = models.FileField(upload_to="resume/")

    downloads = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True, default="Anonymous")
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating: {self.rating}/5 from {self.name}"
from django.db import models
from django.contrib.auth.models import *
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
class UserModel(AbstractUser):
     USER_TYPE_CHOICES = [
        ('Recruiter', 'Recruiter'),
        ('Student', 'Student'),
    ]
     interest_choice = [
       ('Web Development', 'Web Development'),
       ('Data Science', 'Data Science'),
       ('Data Engineering', 'Data Engineering'),
       ('Frontend Development', 'Frontend Development'),
       ('Backend Development', 'Backend Development'),
       ('Artificial Intelligence', 'Artificial Intelligence'),  # fixed typo
       ('Cloud Computing', 'Cloud Computing'),
       ('DevOps', 'DevOps'),
       ('Machine Learning', 'Machine Learning'),
       ('Cybersecurity', 'Cybersecurity'),
       ('Mobile Development', 'Mobile Development'),
       ('UI/UX Design', 'UI/UX Design'),
       ('Game Development', 'Game Development'),
       ('Blockchain Development', 'Blockchain Development'),
       ('Internet of Things (IoT)', 'Internet of Things (IoT)')
]
     work_experience =models.ForeignKey('WorkExperince',on_delete=models.CASCADE,null=True,blank=True)
     education =models.ForeignKey('Education',on_delete=models.CASCADE,null=True,blank=True)
     projects=models.ForeignKey('Projects',on_delete=models.CASCADE,null=True,blank=True)
     achievements=models.ForeignKey('Achievement',on_delete=models.CASCADE,null=True,blank=True)
     certifications=models.ForeignKey('Certification',on_delete=models.CASCADE,null=True,blank=True)
        
     
     image = CloudinaryField('image', blank=True, null=True)
     mobile_number =models.CharField(max_length=200,null=True, blank=True)
     type =models.CharField(choices=USER_TYPE_CHOICES ,max_length=50 ,null=True, blank=True)
     dob=models.DateField(null=True)
     skills=models.CharField(max_length=200, null=True,blank =True)
     interests=models.CharField(choices=interest_choice, null=True, blank =True, max_length=200)
     groups = models.ManyToManyField(Group, blank=True)
     def __str__(self):
         return self.first_name
    
class Education(models.Model):
    degree_choice =degree_choices = [
    ('Bachelor of Arts (B.A.)', 'Bachelor of Arts (B.A.)'),
    ('Bachelor of Science (B.Sc.)', 'Bachelor of Science (B.Sc.)'),
    ('Bachelor of Commerce (B.Com.)', 'Bachelor of Commerce (B.Com.)'),
    ('Bachelor of Technology (B.Tech.)', 'Bachelor of Technology (B.Tech.)'),
    ('Bachelor of Engineering (B.E.)', 'Bachelor of Engineering (B.E.)'),
    ('Bachelor of Medicine, Bachelor of Surgery (MBBS)', 'Bachelor of Medicine, Bachelor of Surgery (MBBS)'),
    ('Bachelor of Dental Surgery (BDS)', 'Bachelor of Dental Surgery (BDS)'),
    ('Bachelor of Business Administration (BBA)', 'Bachelor of Business Administration (BBA)'),
    ('Bachelor of Computer Applications (BCA)', 'Bachelor of Computer Applications (BCA)'),
    ('Bachelor of Pharmacy (B.Pharm)', 'Bachelor of Pharmacy (B.Pharm)'),
    ('Bachelor of Education (B.Ed.)', 'Bachelor of Education (B.Ed.)'),
    ('Bachelor of Law (LLB)', 'Bachelor of Law (LLB)'),
    ('Master of Arts (M.A.)', 'Master of Arts (M.A.)'),
    ('Master of Science (M.Sc.)', 'Master of Science (M.Sc.)'),
    ('Master of Commerce (M.Com.)', 'Master of Commerce (M.Com.)'),
    ('Master of Technology (M.Tech.)', 'Master of Technology (M.Tech.)'),
    ('Master of Engineering (M.E.)', 'Master of Engineering (M.E.)'),
    ('Master of Business Administration (MBA)', 'Master of Business Administration (MBA)'),
    ('Master of Computer Applications (MCA)', 'Master of Computer Applications (MCA)'),
    ('Doctor of Medicine (MD)', 'Doctor of Medicine (MD)'),
    ('Doctor of Philosophy (Ph.D.)', 'Doctor of Philosophy (Ph.D.)'),
    ('Diploma in Engineering', 'Diploma in Engineering'),
    ('Diploma in Pharmacy', 'Diploma in Pharmacy'),
    ('Post Graduate Diploma', 'Post Graduate Diploma')
]

    start_year=models.DateField()
    end_year =models.DateField()
    degree =models.CharField(max_length=200,choices=degree_choice)
    college_name=models.CharField(max_length=200)
    grade=models.CharField(max_length=200)
    
class Company(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE,null=True, blank=True)
    company_name= models.CharField(max_length=200,null=True,blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company_address=models.TextField(null=True,blank=True)
    slug =models.SlugField(max_length=400,null=True,blank=True)
    def save(self, *args,**kwrgs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        return super(Company,self).save(*args,**kwrgs)
    def __str__(self):
        return self.company_name
class Job(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name="user_job")
    company=models.ForeignKey(Company, on_delete=models.CASCADE,related_name="job_company")
    postition=models.CharField(max_length=200,null=True, blank=True)
    job_title=models.CharField(max_length=200,null=True, blank=True)
    job_type=models.CharField(choices=[('Part Time','Part Time') ,('Full Time','Full Time')])
    location =models.CharField(max_length=200,null=True,blank=True)
    salary=models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug =models.SlugField(max_length=400, null=True,blank=True)
    job_description=models.TextField(null=True,blank=True)
    job_requirement=models.TextField(null=True,blank=True)
    job_experience=models.TextField(null=True,blank=True)
    
    def save(self, *args,**kwrgs):
        if not self.slug:
            self.slug = slugify(self.job_title)
        if not self.job_description:
            self.job_description="Job decription will be updated soon please contact the recruiter"
        if not self.job_requirement:
            self.job_requirement="Job Requirements will be updated soon please contace the recruiter"
        return super(Job,self).save(*args,**kwrgs)
    def __str__(self):
        return self.job_title
class Projects(models.Model):
    skill=soft_skills_choices = [
    ('Communication', 'Communication'),
    ('Teamwork', 'Teamwork'),
    ('Leadership', 'Leadership'),
    ('Problem Solving', 'Problem Solving'),
    ('Time Management', 'Time Management'),
    ('Critical Thinking', 'Critical Thinking'),
    ('Adaptability', 'Adaptability'),
    ('Creativity', 'Creativity'),
    ('Emotional Intelligence', 'Emotional Intelligence'),
    ('Conflict Resolution', 'Conflict Resolution'),
    ('Decision Making', 'Decision Making'),
    ('Collaboration', 'Collaboration'),
    ('Negotiation', 'Negotiation'),
    ('Stress Management', 'Stress Management'),
    ('Attention to Detail', 'Attention to Detail'),
    ('Active Listening', 'Active Listening'),
    ('Public Speaking', 'Public Speaking'),
    ('Interpersonal Skills', 'Interpersonal Skills'),
    ('Organizational Skills', 'Organizational Skills'),
    ('Work Ethic', 'Work Ethic'),
    ('Self-Motivation', 'Self-Motivation'),
    ('Empathy', 'Empathy'),
    ('Flexibility', 'Flexibility'),
    ('Coaching & Mentoring', 'Coaching & Mentoring')
]

    project_title=models.CharField(max_length=200)
    project_description=models.TextField()
    repo_link=models.URLField(null=True ,blank=True)
    website_link=models.URLField(null=True ,blank=True)
    skills_used=models.CharField(choices=skill,max_length=200)
class Achievement(models.Model):
    title=models.CharField(null=True ,blank=True)
    description =models.CharField(null=True ,blank=True)
class Certification(models.Model):
    title =models.CharField(max_length=200)
    description =models.CharField(max_length=200)
    start_month=models.DateField()
    end_month=models.DateField()
    link =models.URLField(max_length=200)
    skills_used = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class WorkExperince(models.Model):
    tech_cities_choices = [
    ('Bengaluru', 'Bengaluru'),
    ('Hyderabad', 'Hyderabad'),
    ('Pune', 'Pune'),
    ('Chennai', 'Chennai'),
    ('Mumbai', 'Mumbai'),
    ('Delhi', 'Delhi'),
    ('Gurugram', 'Gurugram'),
    ('Noida', 'Noida'),
    ('Kolkata', 'Kolkata'),
    ('Ahmedabad', 'Ahmedabad'),
    ('Coimbatore', 'Coimbatore'),
    ('Trivandrum', 'Trivandrum'),
    ('Kochi', 'Kochi'),
    ('Indore', 'Indore'),
    ('Jaipur', 'Jaipur'),
    ('Nagpur', 'Nagpur'),
    ('Mysuru', 'Mysuru'),
    ('Lucknow', 'Lucknow'),
    ('Surat', 'Surat'),
    ('Bhubaneswar', 'Bhubaneswar'),
    ('Visakhapatnam', 'Visakhapatnam'),
    ('Vadodara', 'Vadodara'),
    ('Patna', 'Patna'),
    ('Chandigarh', 'Chandigarh'),
    ('Bhopal', 'Bhopal'),
    ('Raipur', 'Raipur'),
    ('Vijayawada', 'Vijayawada'),
    ('Ranchi', 'Ranchi'),
    ('Jamshedpur', 'Jamshedpur'),
    ('Kanpur', 'Kanpur'),
    ('Agra', 'Agra'),
    ('Nashik', 'Nashik'),
    ('Gwalior', 'Gwalior'),
    ('Madurai', 'Madurai'),
    ('Rajkot', 'Rajkot'),
    ('Udaipur', 'Udaipur'),
    ('Aurangabad', 'Aurangabad'),
    ('Pondicherry', 'Pondicherry'),
    ('Gandhinagar', 'Gandhinagar'),
    ('Dehradun', 'Dehradun'),
    ('Shimla', 'Shimla'),
    ('Mangalore', 'Mangalore'),
    ('Tiruchirappalli', 'Tiruchirappalli'),
    ('Kozhikode', 'Kozhikode'),
    ('Vellore', 'Vellore'),
    ('Amritsar', 'Amritsar'),
    ('Faridabad', 'Faridabad'),
    ('Ghaziabad', 'Ghaziabad'),
    ('Meerut', 'Meerut'),
    ('Durgapur', 'Durgapur'),
    ('Siliguri', 'Siliguri'),
    ('Jodhpur', 'Jodhpur'),
    ('Aligarh', 'Aligarh'),
    ('Allahabad (Prayagraj)', 'Allahabad (Prayagraj)'),
    ('Varanasi', 'Varanasi'),
    ('Panaji', 'Panaji'),
    ('Guntur', 'Guntur'),
    ('Hubli', 'Hubli'),
    ('Belgaum', 'Belgaum'),
    ('Salem', 'Salem'),
    ('Thane', 'Thane'),
    ('Rourkela', 'Rourkela'),
    ('Jabalpur', 'Jabalpur'),
    ('Srinagar', 'Srinagar'),
    ('Ujjain', 'Ujjain'),
    ('Thiruvananthapuram', 'Thiruvananthapuram'),
    ('Vapi', 'Vapi'),
    ('Anand', 'Anand'),
    ('Haldwani', 'Haldwani'),
    ('Moradabad', 'Moradabad'),
    ('Saharanpur', 'Saharanpur'),
    ('Jalgaon', 'Jalgaon'),
    ('Satara', 'Satara'),
    ('Tumkur', 'Tumkur'),
    ('Karimnagar', 'Karimnagar'),
    ('Bellary', 'Bellary'),
    ('Palakkad', 'Palakkad'),
    ('Erode', 'Erode'),
    ('Thanjavur', 'Thanjavur'),
    ('Tirunelveli', 'Tirunelveli')
]

    companyName=models.CharField(max_length=200)
    work_type=models.CharField(choices=[('Internship','Internship')      
                                        ,('Part-Time','Part-Time'),
                                        ('Full-Time','Full-Time')])
    company_website =models.CharField(max_length=200)
    location =models.CharField(max_length=200,choices=tech_cities_choices)
    start_date=models.DateField()
    end_date =models.DateField(null=True,blank=True)
    working=models.CharField(choices=[(
        'Working Currently','Working Currently'
    ), 
    (
    'No','No')])
    def __str__(self):
        return self.companyName
    
class Application(models.Model):
    name=models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    age=models.CharField(max_length=200)

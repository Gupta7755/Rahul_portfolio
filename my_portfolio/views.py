from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def admin_login(request):

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("admins")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("admins")

    return render(request, "admin_login.html")

def admin_logout(request):
    logout(request)
    return redirect("admin_login")

def download_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    resume.downloads += 1
    resume.save()
    return redirect(resume.resume_file.url)

def request_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            return JsonResponse({"success": False, "error": "Email is required"})
            
        otp = str(random.randint(100000, 999999))
        request.session['contact_otp'] = otp
        request.session['contact_email'] = email
        
        try:
            send_mail(
                subject="Your Portfolio Contact Verification Code",
                message=f"Your verification code is: {otp}\n\nPlease enter this code to securely send your message.",
                from_email=getattr(settings, 'EMAIL_HOST_USER', 'noreply@example.com'),
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})

def verify_contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        user_otp = request.POST.get("otp")
        
        saved_otp = request.session.get('contact_otp')
        saved_email = request.session.get('contact_email')
        
        if not saved_otp or user_otp != saved_otp or email != saved_email:
            return JsonResponse({"success": False, "error": "Invalid or expired OTP"})
            
        try:
            send_mail(
                subject=f"New Verified Portfolio Message from {name}",
                message=f"VERIFIED MESSAGE\n\nFrom Name: {name}\nVisitor Email: {email}\n\nMessage:\n{message}",
                from_email=getattr(settings, 'EMAIL_HOST_USER', 'noreply@example.com'),
                recipient_list=[getattr(settings, 'EMAIL_HOST_USER')],
                fail_silently=False,
            )
            del request.session['contact_otp']
            del request.session['contact_email']
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Failed to deliver message: {str(e)}"})
    return JsonResponse({"success": False, "error": "Invalid request"})

def viewers(request):
    try:
        profile = Profile.objects.first()
        about = About.objects.first()
    except Exception as e:
        # Tables don't exist yet (migrations needed)
        return render(request, 'viewers.html', {'error_msg': "Database tables not found. Please run migrations."})
    
    if request.method == "POST":
        if "contact_submit" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            message = request.POST.get("message")
            
            try:
                send_mail(
                    subject=f"New Portfolio Message from {name}",
                    message=f"You have received a new message from your portfolio contact form.\n\nFrom Name: {name}\nVisitor Email: {email}\n\nMessage:\n{message}",
                    from_email=getattr(settings, 'EMAIL_HOST_USER', 'noreply@example.com'),
                    recipient_list=[getattr(settings, 'EMAIL_HOST_USER')],
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully! I'll get back to you soon.")
            except Exception as e:
                messages.error(request, f"Failed to send email. Please check SMTP settings. Error: {e}")
                
            return redirect('/#contact')

        elif "feedback_submit" in request.POST:
            f_name = request.POST.get("feedback_name", "Anonymous")
            if not f_name.strip(): f_name = "Anonymous"
            f_message = request.POST.get("feedback_message")
            f_rating = request.POST.get("rating", 5)
            
            Feedback.objects.create(name=f_name, rating=f_rating, comment=f_message)
            messages.success(request, "Thank you! Your feedback will help improve this portfolio.")
            return redirect('/#contact')
    if about:
        about.skills_list = [s.strip() for s in about.skills_tags.split(',')] if about.skills_tags else []
        about.focus_list = [f.strip() for f in about.focus_areas.split(',')] if about.focus_areas else []
        
    projects = Project.objects.all().order_by('order')
    for project in projects:
        project.display_title = project.title.replace('_', ' ')
        project.features_list = [f.strip() for f in project.key_features.split(',')] if project.key_features else []
        project.tech_list = [t.strip() for t in project.tech_stack.split(',')] if project.tech_stack else []
    
    experiences = Experience.objects.all().order_by('-start_date')
    educations = Education.objects.all().order_by('-start_year')
    certificates = Certificate.objects.all().order_by('-issue_date')
    skills = Skill.objects.all()
    resume = Resume.objects.order_by('-updated_at').first()

    context = {
        'profile': profile,
        'about': about,
        'projects': projects,
        'experiences': experiences,
        'educations': educations,
        'certificates': certificates,
        'skills': skills,
        'resume': resume,
    }

    return render(request, 'viewers.html', context)


@login_required(login_url="admin_login")
def admins(request):

    profile = Profile.objects.first()
    
    feedbacks = Feedback.objects.all().order_by('-created_at')
    for fb in feedbacks:
        fb.stars_range = range(fb.rating)
        fb.empty_stars_range = range(5 - fb.rating)

    context = {
        'profile': profile,
        'projects_count': Project.objects.count(),
        'experiences_count': Experience.objects.count(),
        'educations_count': Education.objects.count(),
        'certificates_count': Certificate.objects.count(),
        'skills_count': Skill.objects.count(),
        'has_resume': Resume.objects.exists(),
        'resume': Resume.objects.first(),
        'has_about': About.objects.exists(),
        'feedbacks': feedbacks,
    }

    return render(request, "admins.html", context)
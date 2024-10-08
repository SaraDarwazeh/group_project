from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def profile(request):
  return render(request,'profile.html')
# Create your views here.
def index(request):

  return render(request,'index.html')

def assessment(request):
  context = {
    'questions':all_questions(),
    'choices':all_choices(),
  }
  return render(request,'assessment.html',context)

def login(request):
  return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        errors = User.objects.register(request.POST)

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/login')
        try:
            patient = create_patient(request.POST)
            if patient and patient.email and patient.first_name:
                # Send the welcome email
                send_registration_email(patient.email, patient.first_name)
                return redirect('/login')
            else:
                return redirect('/login')
        except Exception as e:
            # Handle any unexpected errors during patient creation
            messages.error(request, f'Registration failed due to an error: {str(e)}')
            return redirect('/login')
    else:

        return render(request, 'email/register.html')

def sign_up(request):
  if request.method == 'POST':
    errors = User.objects.login(request.POST)

    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/login')
    else:
        user = user_email(request.POST)
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password .encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/team')
        else:
            messages.error(request, "Invalid password.")
            return redirect('/login')
        return redirect('/')

    


def about(request):
  return render(request,'about.html')

def team(request):
  context={
    'therapists':all_therapist()
  }
  return render(request,'team.html',context)

def contact(request):
  return render(request,'contact.html')

def services(request):
  return render(request,'services.html')
# def index(request):
#     if request.method == "POST":
#         errors = User.objects.basic_validator(request.POST)
#         if errors:
#             for key, value in errors.items():
#                 messages.error(request, value)
#             return redirect('/')

#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         date_of_birth = request.POST.get('dateofbirth')
#         phone_number = request.POST.get('phone_number')
#         email = request.POST.get('email')
#         photo = request.FILES.get('photo')
#         password = generate_random_password()
#         # password = request.POST.get('password')
#         # confirm_password = request.POST.get('confirm_password')


#         # # Check if passwords match
#         # if password != confirm_password:
#         #     messages.error(request, "Passwords do not match.")
#         #     return redirect('/')

#         # pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

#         # Create User
#         user = User.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             dateofbirth=date_of_birth,
#             phone_number=phone_number,
#             email=email,
#             password=password,
#             photo = photo,
#         )
#         request.session['first_name'] = first_name

#         # Handle role
#         role_title = request.POST.get('role')
#         custom_role = request.POST.get('custom_role')
#         custom_description = request.POST.get('custom_description')

#         if role_title == 'custom' and custom_role:
#             role = Role.objects.create(
#                 title=custom_role,
#                 description=custom_description,
#                 user=user
                
#             )
#         elif role_title == 'member':
#             role = Role.objects.create(
#                 title=role_title,
#                 description='this is a member',
#                 user=user
#             )
#         elif role_title == 'trainer':
#             role = Role.objects.create(
#                 title=role_title,
#                 description='this is a trainer',
#                 user=user
#             )
#         return redirect('/users')

#     content = {
#         'roles': Role.objects.all(),
#         'users': User.objects.all()
#     }
#     return render(request, 'index.html', content)

      
def send_registration_email(user_email, user_first_name):
    subject = 'Thank You for Registering!'
    message = render_to_string('email/thank_you_email.html', {
        'user': {
            'first_name': user_first_name
        }
    })
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email]
    )
    email.content_subtype = 'html'  # Set content type to HTML
    email.send()
    
def therapist_info(request, first_name, last_name):
    # Use get_object_or_404 to ensure that if no therapist is found, a 404 error is raised.
    therapist = get_object_or_404(Therapist, first_name=first_name, last_name=last_name)
    language_names = ', '.join([language.name for language in therapist.languages.all()])
    # Render the therapist_info template with the therapist data.
    return render(request, 'therapist_info.html', {'therapist': therapist, 'language_names': language_names})

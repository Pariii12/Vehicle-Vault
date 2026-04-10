from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserSignupForm, UserLoginForm
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def generate_otp():
    return str(random. randint(100000,999999))

def userSignupView(request):
    if request.method =="POST":
        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.status = 'inactive'
            user.otp = generate_otp()
            user.save()

            #email send
            email = form.cleaned_data['email']

            request.session['pending_user_id'] = user.id

            send_mail(subject="welcome to vehicle vault",message=f"your OTP is {user.otp}",from_email=settings.EMAIL_HOST_USER,recipient_list=[email])
            return redirect('verify_otp') #redirect to OTP page 
        else:
            return render(request,'core/signup.html',{'form':form})
    else:
        form = UserSignupForm()
        return render(request,'core/signup.html',{'form':form})


def verifyOtpView(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('login') #fallback if session lost
    
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        # 🔹 Handle resend button
        if "resend" in request.POST:
            user.otp = generate_otp()
            user.save()
            send_mail(
                subject="Resend OTP - Vehicle Vault",
                message=f"Your new OTP is {user.otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return render(request, "core/verify_otp.html", {"message": "New OTP sent to your email."})
        
        # 🔹 Handle OTP verification
        entered_otp = request.POST.get('otp')
        if user.otp == entered_otp:
            user.status = 'active'
            user.otp = None
            user.save()
            del request.session['pending_user_id'] #clear session 
            return redirect('login')
        else:
            return render(request, 'core/verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'core/verify_otp.html')


def userLoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                # OTP check: block inactive users
                if user.status == "inactive":
                    return redirect("verify_otp")                    
                login(request, user)
       
                # Role-based redirect
                if user.role == "admin":
                    return redirect("admin_dashboard")
                elif user.role == "seller":
                    return redirect("seller_dashboard")
                elif user.role == "buyer":
                    return redirect("buyer_dashboard")
                else:
                    # Unexpected role
                    return render(request, "core/login.html", {
                        "form": form,
                        "error": "Your account role is not recognized. Contact support."
                    })

            # Invalid credentials
            return render(request, "core/login.html", {
                "form": form,
                "error": "Invalid email or password."
            })

        # Form invalid
        return render(request, "core/login.html", {
            "form": form,
            "error": "Please correct the errors below."
        })

    # GET request
    form = UserLoginForm()
    return render(request, "core/login.html", {"form": form})



def logout_view(request):
    logout(request)  # clears the session
    return redirect('login') # send user back to login page




 
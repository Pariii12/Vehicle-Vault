from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserSignupForm, UserLoginForm

# Create your views here.
def userSignupView(request):
    if request.method =="POST":
        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            #email send
            email = form.cleaned_data['email']
            send_mail(subject="welcome to vehicle vault",message="Thank you for registering with Vehicle Vault.",from_email=settings.EMAIL_HOST_USER,recipient_list=[email])
            form.save()
            return redirect('login') 
        else:
            return render(request,'core/signup.html',{'form':form})
    else:
        form = UserSignupForm()
        return render(request,'core/signup.html',{'form':form})
         

def userLoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
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




 
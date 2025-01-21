from django.shortcuts import render
from .models import Account
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import auth
from .forms import RegistrationForm,update_profile
from django.contrib.auth.decorators import login_required


# Create your views here.
class register(CreateView):
    model = Account
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username=form.cleaned_data['email'].split('@')[0]
        form.instance.username = username
        if Account.objects.filter(email=form.cleaned_data['email']).exists():
            messages.warning(self.request,'Email already exists')
            return redirect('registration')
        if form.cleaned_data['password']!=form.cleaned_data['confirm_password']:
            messages.warning(self.request,'Password does not match')
            return redirect('registration')
        # pore email verification add kore account active korbo
        
        form.save()
        auth.login(self.request,form.instance)
        messages.success(self.request,'Registration Successful')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request,'Registration Failed,Plesase try again')
        return redirect('registration')
    
  
def login(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = Account.objects.filter(email=email).first()
        if user:
            if user.check_password(password):
                if user.is_active==False:
                    messages.warning(request,'Account is not activated')
                    return redirect('login')
                messages.success(request,'Login Successful')
                auth.login(request,user)
                return redirect('home')
            else:
              
                messages.warning(request,'Invalid Password')
                return redirect('login')
        else:
            messages.warning(request,'Invalid Email')
            return redirect('login')
        
   
    return render(request,'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html')

@login_required(login_url='login')
def edit_profile(request):
    if request.method=="POST":
        form=update_profile(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"profile Updated successful")
            return redirect('profile')
        else:
            messages.error(request,"Something went wrong try again")
            return redirect('edit_profile')
    form=update_profile(instance=request.user)   
    return render(request,'edit_profile.html',{'form':form}) 
    

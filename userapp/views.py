from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.views import View
from .models.user import User



# Create your views here.
def base(request):
    return render(request,'base.html')
class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')
    def post(self,request):
        postData = request.POST
        username = postData.get('username')
        email = postData.get('email')
        address = postData.get('address')
        password = postData.get('password')
        value = {
            'username': username,
            'email': email,
            'address': address,
            'password': password,

        }
        error_message = None
        user = User(username=username, email=email, address=address,  password=password)
        error_message = self.validatecustomer(user)

        # saving
        if not error_message:
            user.password = make_password(user.password)
            user.register()

            return redirect('login')

        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validatecustomer(self, user):
        # Validations
        error_message = None

        if not user.username:
            error_message = "Username is Required"
        elif len(user.username) > 50:
            error_message = "Username should be less than 50 characters"
        elif not user.email:
            error_message = "Email Required"
        elif len(user.email) > 50:
            error_message = "Email should be less than 50 characters"
        elif not user.address:
            error_message = "Address is Required"
        elif len(user.address) > 400:
            error_message = "Address should not exceed 200 characters"
        elif not user.password:
            error_message = "Password Required"
        elif len(user.password) < 8:
            error_message = "Password should have minimum 8 characters"
        elif user.isExists():
            error_message = "Email Address already registered"

        return error_message

class Login(View):
    return_url = None
    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    def post(self,request):
        postData = request.POST
        email = postData.get('email')
        password = postData.get('password')
        user = User.get_user_by_email(email)

        error_message = None
        if user:
            flag = check_password(password, user.password)
            if flag:

                request.session['user'] = user.id
                print(user.id)

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)

                else:
                    Login.return_url = None
                    return redirect('details')
            else:
                error_message = 'Invalid email or password!!'
        else:
            error_message = 'Invalid email or password!!'
        return render(request, 'login.html', {'error': error_message})

class Details(View):
    def get(self,request):
        user = request.session.get('user')
        details = User.get_user_info(user)
        return render(request,'details.html',{'details':details})
    def post(self,request):
        postData = request.POST
        user = request.session.get('user')
        User.objects.filter(pk=user).update(username = postData.get('username'))
        User.objects.filter(pk=user).update(address=postData.get('address'))
        details = User.get_user_info(user)
        details.username = postData.get('username')
        details.address = postData.get('address')
        print(details)
        details.register()
        return render(request,'details.html',{'details':details})

def clear(request):
    user = request.session.get('user')
    User.objects.get(pk = user).delete()
    return redirect('login')

def logout(request):
    request.session.clear()
    return redirect('login')
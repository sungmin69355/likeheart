from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
# Create your views here.


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not username:
            messages.info(request, '아이디를 입력해 주세요')
            return render(request, 'signup.html')

        if not password1:
            messages.info(request, '비번을 입력해 주세요')
            return render(request, 'signup.html')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, '아이디가 중복됩니다.')
                return render(request, 'signup.html')
            else:
                user = User.objects.create_user(username, password=password1)
                auth.login(request, user)
                return redirect('home')
        else:
            messages.info(request, '비밀번호가 다릅니다.')
            return render(request, 'signup.html')
        


    return render(request, 'signup.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    
    return render(request, 'signup.html')
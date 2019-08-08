from django.shortcuts import render, redirect
from .models import *
from .forms import RegisterForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from custom_user.forms import MyUserChangeForm, MyUserCreationForm

User = get_user_model()


def common(request):
    context = {}
    context["menu"] = Menu.objects.all()
    context["mainicon"] = MainIcon.objects.last()
    context["main"] = Main.objects.all()
    context["footer"] = Footer.objects.last()
    context["footerfields"] = Footerfields.objects.all()
    context["footermenu"] = Footermenu.objects.all()
    context["footername"] = Footername.objects.last()
    context["footericon"] = Footericon.objects.all()
    context["aboutsite"] = AboutSite.objects.last()
    return context


def home(request):
    context = {}
    context["menu"] = Menu.objects.all()
    context["mainicon"] = MainIcon.objects.last()
    context["main"] = Main.objects.all()
    context["portfolio"] = Portfolio.objects.last()
    context["portfoliophoto"] = Portfoliophoto.objects.all()
    context["features"] = Features.objects.last()
    context["featuresmain"] = FeaturesMain.objects.all()
    context["footer"] = Footer.objects.last()
    context["footerfields"] = Footerfields.objects.all()
    context["footermenu"] = Footermenu.objects.all()
    context["footername"] = Footername.objects.last()
    context["footericon"] = Footericon.objects.all()
    context["aboutsite"] = AboutSite.objects.last()
    context["form"] = RegisterForm()
    context["loginform"] = LoginForm()

    return render(request, "index.html", context)


def register_view(request):
    context = {}
    context["register"] = Register.objects.all()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get("password1"))
            # user.first_name = request.POST.get("fullname").split()[0]
            # user.last_name = request.POST.get("fullname").split()[1]
            user.is_active=False
            user.save()
            messages.success(
                request, "Emailinizi tesdiqleyin"
            )
        else:
            context["form"] = form

    return redirect("home")

def verify_view(request, token, user_id):
    verify = Verification.objects.filter(token=token, user_id=user_id, expire=False).last()
    if verify:
        verify.expire = True
        verify.save()
        verify.user.is_active = True
        verify.user.save()
        messages.info(
            request, "Success"
        )
        return redirect('settings_view')
    else:
        return redirect('home')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect("explore")
                else:
                    messages.error(
                        request, "Username or Password inValid"
                    )
            return redirect("home")
        return render(request,"index.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def settings_view(request):
    context = common(request)
    # context["profile"] = Profile.objects.filter(user=request.user)
    context["profileview"] = MyUserChangeForm(instance=request.user, initial={
        "fullname": request.user.get_full_name(),
        "username": request.user.get_username(),
        "email": request.user.email
    })
    if request.method == "POST":
        form = MyUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # user.first_name = request.POST.get("fullname").split()[0]
            # user.last_name = request.POST.get("fullname").split()[1]
            # user.username=request.POST.get("username")
            # user.email = request.POST.get("email")
            # user.save()
            return redirect('home')
        else:
            context["profileview"] = form

    return render(request, "setting-profile.html", context)


def profile_view(request, id):
    context = common(request)
    context["user"] = User.objects.filter(id=id).last()
    context["dashboard"] = Post.objects.filter(user_id=id)

    return render(request, "user-profile.html", context)


def explore(request):
    context = common(request)
    context["post"] = Post.objects.all()
    return render(request, "explore-style1.html", context)


def dashboard(request):
    context = common(request)
    context["dashboard"] = Post.objects.filter(user=request.user)

    return render()


def addpost_view(request):
    context = common(request)
    context["form"] = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect("explore")
        else:
            context["form"] = PostForm()

    return render(request, "shot-add.html", context)


def ShotDetail(request,id):
    context={}
    id = request.GET.get('id')
    current_post = Post.objects.filter(id=id).last()
    context["currentpost"]=current_post
    print(id)

    return render(request, 'shot-detail.html', context)

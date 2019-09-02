from threading import Thread

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from  django.db.models import Q
from django.views.generic import UpdateView

import json

from sqlparse.sql import Token

from todo_app.tasks import send_forget_password, send_verification_email
from .models import *
from .forms import RegisterForm, LoginForm, PostForm, CommentForm, SocialForm, ForgetPass, PasswordChangeForm, Contact
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from custom_user.forms import MyUserChangeForm, MyUserCreationForm
from django.http import JsonResponse, request
from django.core.paginator import Paginator

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

    if request.user.is_authenticated:
        return redirect('explore')
    else:
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
            user.is_active = False
            user.save()
            messages.success(
                request, "Emailinizi tesdiqleyin"
            )
            return redirect("home")
        else:
            messages.error(request,"Password is not match")
            context["form"] = form

    return redirect('home')


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
        login(request, verify.user)
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
                    return redirect("settings_view")
                else:
                    messages.error(
                        request, "Username or Password inValid"
                    )
            return redirect("home")
        return render(request, "index.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def social_settings(request):
    context = common(request)
    context["socialmodel"] = Socialsetting.objects.filter(user=request.user).last()
    context["socialform"] = SocialForm()
    if request.method == "POST":
        form = SocialForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            messages.success(
                request, "Succes"
            )
            return redirect('socialsetting')

    return render(request, "setting-socials.html", context)


@login_required
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
            return redirect('home')
        else:
            context["profileview"] = form

    return render(request, "setting-profile.html", context)


def profile_view(request, id):
    context = common(request)
    user = User.objects.filter(id=id).last()
    context["socialmodel"] = Socialsetting.objects.filter(user=request.user).last()
    context["count"] = Post.objects.filter(user_id=id).all().count()
    pagination = Paginator(Post.objects.filter(user_id=id), 6)
    context["dashboard"] = pagination.get_page(request.GET.get('page', 1))
    context["page_range"] = pagination.page_range
    context["user"] = User.objects.filter(id=id).last()
    context["followers"] = [follow.from_user for follow in user.followers.all()]
    context["following"] = [follow.to_user for follow in user.following.all()]
    context["follower_count"] = user.followers.all().count()
    context["following_count"] = user.following.all().count()

    return render(request, "user-profile.html", context)


class PostUpdate(generic.UpdateView):
    extra_context = common(request)
    model = Post
    form_class = PostForm
    template_name = "shot-add.html"
    success_url = "/"


def explore(request):
    context = common(request)
    pagination = Paginator(Post.objects.all(), 6)
    context["post"] = pagination.get_page(request.GET.get('page', 1))
    context["page_range"] = pagination.page_range
    if request.method == "POST" and request.is_ajax():
        post_id = request.POST.get("post_id")
        post = Post.objects.filter(id=post_id).last()
        if post:
            like = Like.objects.filter(post=post, user=request.user).last()
            if like:
                post.like_count -= 1
                post.save()
                like.delete()
                return JsonResponse({
                    "like_count": post.like_count,
                    "status": False
                })
            else:
                post.like_count += 1
                post.save()
                Like.objects.create(
                    user=request.user,
                    post=post
                )

                return JsonResponse({
                    "like_count": post.like_count,
                    "status": True
                })
    if 'q' in request.GET:
        query = request.GET.get('q')
        explore = Post.objects.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query)
        )
        pagination = Paginator(explore, 8)
        context['post'] = pagination.get_page(request.GET.get('page', 1))

    return render(request, "explore-style1.html", context)


def like_view(request):
    if request.method == "POST" and request.is_ajax():
        post_id = request.POST.get("post_id")
        post = Post.objects.filter(id=post_id).last()
        if post:
            like = Like.objects.filter(post=post, user=request.user).last()
            if like:
                post.like_count -= 1
                post.save()
                like.delete()
                return JsonResponse({
                    "like_count": post.like_count,
                    "status": False
                })
            else:
                post.like_count += 1
                post.save()
                Like.objects.create(
                    user=request.user,
                    post=post
                )

                return JsonResponse({
                    "like_count": post.like_count,
                    "status": True
                })
        else:
            return redirect("explore")
    else:
        return redirect("explore")


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


def ShotDetail(request, id):
    context = {}

    id = request.GET.get('id')
    if id:

        pass
    else:
        id = request.POST.get("post_id_cm")
    current_post = Post.objects.filter(id=id).last()
    if request.user not in current_post.view.all():
        current_post.view.add(request.user)
    context["currentpost"] = current_post
    context["follower_count"] = current_post.user.followers.all().count()
    context["following_count"] = current_post.user.following.all().count()
    me = Post.objects.all().filter(user=current_post.user).count()
    current_post_comment = current_post.commentpost_set.all()
    context["current_post_comment"] = current_post_comment
    context["form"] = CommentForm()
    if request.method == "POST" and request.is_ajax():
        post_id_cm = request.POST.get("post_id_cm")
        if post_id_cm:
            text_coment = request.POST.get('text_comment')
            CommentPost.objects.create(
                user=request.user,
                comment=text_coment,
                post=Post.objects.filter(id=post_id_cm).last(),
            )
            return JsonResponse({
                'append': True,
                'image': request.user.profilephoto.url,
                'user': request.user.username,
                'text_comment': text_coment,
                'comment_count': current_post_comment.count()
            })

    context["count"] = me
    print(id)

    return render(request, 'shot-detail.html', context)


class Delete(generic.DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = "/"

    def get_queryset(self):
        qs = super(Delete, self).get_queryset()
        return qs.filter(user=self.request.user)


class FollowView(generic.View):

    def post(self, request):
        user_id = request.POST.get("user_id")
        follow = Follow.objects.filter(
            from_user=request.user,
            to_user_id=user_id
        ).last()
        if not follow:  # follow
            Follow.objects.create(
                from_user=request.user,
                to_user_id=user_id
            )
            return JsonResponse({
                "status": True
            })
        else:
            follow.delete()
            return JsonResponse({
                "status": False
            })


# senin followerlerin
def Follower_friend(request, id):
    context = common(request)
    user = User.objects.filter(id=id).last()
    pagination = Paginator([follow.from_user for follow in user.followers.all()], 6)
    context["page_range"] = pagination.page_range
    context["followers"] = pagination.get_page(request.GET.get('page', 1))
    context["user_followers"] = [follow.from_user for follow in user.followers.all()]
    context["following"] = [follow.to_user for follow in user.following.all()]
    context["user_list"] = User.objects.all()
    context["following_count"] = user.following.all().count()
    context["follower_count"] = user.followers.all().count()
    context["user"] = user

    return render(request, 'user-followers.html', context)


# kimleri follow etdiyin
def Following_friend(request, id):
    context = common(request)
    user = User.objects.filter(id=id).last()
    pagination = Paginator([follow.to_user for follow in user.following.all()], 6)
    context["page_range"] = pagination.page_range
    context["following"] = pagination.get_page(request.GET.get('page', 1))
    context["followers"] = [follow.from_user for follow in user.followers.all()]
    Follow.objects.filter(to_user=user)
    context["follower_count"] = user.followers.all().count()
    context["following_count"] = user.following.all().count()
    context["user"] = user

    return render(request, 'user-following.html', context)


# postu beyenen userlerin siyahisi
def likers_user(request, id):
    context = common(request)
    user = Post.objects.filter(id=id).last()
    context["likers"] = user

    return render(request, "likers_user.html", context)


# email imputunu acmag ucun
class ForgetPassword(generic.FormView):
    template_name = "forgetpassword.html"
    success_url = "/"
    form_class = ForgetPass

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        user = User.objects.filter(email=email).last()
        if user:
            verify = Verification.objects.create(user=user)
            background_job = Thread(target=send_forget_password, args=(email, verify.forget_url()))
            background_job.start()
            messages.success(self.request, "Succes")
            return super(ForgetPassword, self).form_valid(form)
        else:
            messages.success(self.request, "Succes")
            return super(ForgetPassword, self).form_valid(form)


# parolu deyishmek ucun
class Forget_Password(generic.View):
    def get(self, request, user_id, token):
        verify = Verification.objects.filter(
            user_id=user_id,
            token=token,
            expire=False
        ).last()
        if verify:
            context = {}
            context["form"] = PasswordChangeForm()
            return render(request, "forgetpassword.html", context)
        else:
            return redirect("/")

    def post(self, request, user_id, token):
        verify = Verification.objects.filter(
            user_id=user_id,
            token=token,
            expire=False
        ).last()
        if verify:
            if not verify.expire:
                verify.expire = True
                verify.save()
                form = PasswordChangeForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data.get("new_password")
                    verify.user.set_password(password)
                    verify.user.save()
                    return redirect("/")
                else:
                    return redirect("/")
        else:
            return redirect("/")


def about(request):
    context = common(request)
    context["about"] = About.objects.last()

    return render(request, "page-about.html", context)


def contact_view(request):
    context = common(request)
    context["contact"] = Contactus.objects.all()
    context["contactmenu"]=Contactmenu.objects.last()
    context["form"] = Contact()
    if request.method=="POST":
        form=Contact(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            return redirect('contact')
        else:
            context["form"]=Contact()

    return render(request, "page-contact.html", context)

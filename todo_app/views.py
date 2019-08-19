from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
import json
from .models import *
from .forms import RegisterForm, LoginForm, PostForm, CommentForm, SocialForm
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
    context["user"] = User.objects.filter(id=id).last()
    context["count"] = Post.objects.filter(user_id=id).all().count()
    pagination = Paginator(Post.objects.filter(user_id=id), 6)
    context["dashboard"] = pagination.get_page(request.GET.get('page', 1))
    context["page_range"] = pagination.page_range
    context["followers"] = [follow.from_user for follow in user.followers.all()]
    context["follower_count"] = user.followers.all().count()
    context["following_count"] = user.following.all().count()
    context["followers"] = [follow.from_user for follow in user.followers.all()]

    return render(request, "user-profile.html", context)


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

    # def get_context_data(self, **kwargs):
    #     context = {}
    #     context["following"] = [follow.to_user for follow in self.request.user.following.all()]
    #     context["user_list"] = User.objects.all().exclude(id__in=[self.request.user.id])
    #     return context


def Follower_friend(request, id):
    context = {}
    user = User.objects.filter(id=id).last()
    context["followers"] = [follow.from_user for follow in user.followers.all()]
    context["user_list"] = User.objects.all()
    context["following_count"] = request.user.following.all().count()
    context["follower_count"] = user.followers.all().count()
    context["user"] = user

    return render(request, 'user-followers.html', context)


def Following_friend(request, id):
    context = {}
    user = User.objects.filter(id=id).last()
    context["following"] = [follow.to_user for follow in user.following.all()]
    context["follower_count"] = user.followers.all().count()
    context["following_count"] = user.following.all().count()
    context["user"] = user


    return render(request, 'user-following.html', context)





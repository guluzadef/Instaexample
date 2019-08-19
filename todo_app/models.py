from django.db import models
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()


def generate_token(size=120, chars=string.ascii_letters + string.digits):
    return "".join([random.choice(chars) for _ in range(size)])


class MainIcon(models.Model):
    image = models.ImageField(upload_to="mainicon")


class Menu(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"


class Main(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    image = models.ImageField(upload_to="mainphoto")

    def __str__(self):
        return f"{self.title}"


class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"


class Portfoliophoto(models.Model):
    image = models.ImageField(upload_to="portfoliophoto")

    def __str__(self):
        return f"{self.image}"


class Features(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"


class FeaturesMain(models.Model):
    icon = models.CharField(max_length=255)
    icontitle = models.CharField(max_length=255)
    icondescription = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.icon}"


class Footer(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"


class Footerfields(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"


class Footermenu(models.Model):
    footer = models.ForeignKey(Footerfields, on_delete=models.CASCADE)
    fields = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.footer}"


class Footername(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"


class Footericon(models.Model):
    icon = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.icon}"


class AboutSite(models.Model):
    image = models.ImageField(upload_to="aboutsitephoto")


class Register(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.fullname}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="postphoto")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    view=models.ManyToManyField(User,related_name="views")
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title}"

    def get_likers(self):
        return [like.user for like in self.like_set.all()]

class CommentPost(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment=models.CharField(max_length=130)

    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post}"

    class Meta:
        ordering = ["-id"]

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.IntegerField(choices=(
        (0, "Like"),
        (1, "Unlike")
    ),
        default=0
    )
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"


class Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120, default=generate_token)
    expire = models.BooleanField(default=False)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.token}"


class Socialsetting(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    website=models.CharField(max_length=123,null=True,blank=True)
    facebook = models.CharField(max_length=123,null=True,blank=True)
    twitter= models.CharField(max_length=123,null=True,blank=True)


class Profileicon(models.Model):
    icon = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.icon}"



class Follow(models.Model):
    from_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name="following")
    to_user = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="followers")
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.from_user} => {self.to_user}"
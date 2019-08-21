from django.urls import path
from .views import home,PostUpdate,Following_friend,Follower_friend,FollowView,register_view,social_settings,verify_view,like_view,login_view,settings_view,logout_view,profile_view,addpost_view,explore,ShotDetail

urlpatterns = [
    path('', home, name="home"),
    path('verify/<str:token>/<int:user_id>', verify_view, name="verify_view"),
    path('register/', register_view, name="register_view"),
    path('login/', login_view, name="login_view"),
    path('settings/', settings_view, name="settings_view"),
    path('social/', social_settings, name="socialsetting"),
    path('logout/', logout_view, name="logout_view"),
    path('profile/<int:id>', profile_view, name="profile_view"),
    path('addpost/', addpost_view, name="addpost_view"),
    path('explore/', explore, name="explore"),
    path('like/', like_view, name="like-view"),
    path('detail/<int:id>/', ShotDetail, name="detail"),
    path('follow/', FollowView.as_view(), name="follower"),
    path('<int:id>/follower/',Follower_friend,name="friend_follow"),
    path('<int:id>/following/', Following_friend, name="friend_following"),
    path('update/<int:pk>/',PostUpdate.as_view(),name="update")
]

from django.shortcuts import render, redirect
from coverweb.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
import string
import os

id_filter = string.ascii_letters + string.digits + "_"
password_filter = string.ascii_letters + string.digits + "!@#$%^&*\\"

gr = ["케이팝", "팝", "락", "메탈", "EDM", "힙합", "R&B", "가요", "발라드", "제이팝", "재즈", "기타"]

# Create your views here.

def main(request):
    videos = []
    for i in gr:
        for j in Video.objects.all():
            if j.genre == i:
                user = User.objects.filter(username=j.username)[0]
                videos.append([j,user])
                break

    context = {
        "videos" : videos,
        "genre" : gr,
        "search" : ["", ""]
    }

    if request.method == "POST":
        genre = request.POST.get("genre")
        keyw = request.POST.get("keyw")
        context["videos"] = []
        context["search"] = [genre, keyw]
        for i in Video.objects.all():
            if keyw == "":
                if genre == i.genre:
                    user = User.objects.filter(username=i.username)
                    context["videos"].append([i, user])
            else:
                if genre == i.genre and (keyw in i.sub or keyw in i.info):
                    user = User.objects.filter(username=i.username)
                    context["videos"].append([i, user])
        return render(request, "main.html", context)

    return render(request, "main.html", context)

def signup(request):
    if request.method == "POST":
        nick = request.POST.get("nick")
        username = request.POST.get("username")
        password = request.POST.get("password")
        info = request.POST.get("info")
        re = request.POST.get("re-enter")
        if nick == "":
            messages.info(request, "닉네임은 빈칸일 수 없습니다.")
            return render(request, "signup.html", {"nick" : nick, "id" : id, "password" : password, "re" : re, "info" : info})
        if User.objects.filter(username=username).exists():
            messages.info(request, "아이디가 중복됩니다.")
            return render(request, "signup.html", {"nick" : nick, "id" : id, "password" : password, "re" : re, "info" : info})
        if username == "":
            messages.info(request, "아이디는 빈칸일 수 없습니다.")
            return render(request, "signup.html", {"nick" : nick, "id" : id, "password" : password, "re" : re, "info" : info})
        for i in username:
            if not i in id_filter:
                messages.info(request, "아이디는 영어, 숫자, _만 사용 가능합니다.")
                return render(request, "signup.html", {"nick" : nick, "id" : id, "password" : password, "re" : re, "info" : info})
        if password == "":
            messages.info(request, "비밀번호는 빈칸일 수 없습니다.")
            return render(request, "signup.html", {"nick" : nick, "id" : id, "password" : password, "re" : re, "info" : info})
        for i in password:
            if not i in password_filter:
                messages.info(request, "비밀번호는 영어, 숫자, 특수문자만 사용 가능합니다.")
                return render(request, "signup.html", {"nick" : nick, "id" : id, "password" : password, "re" : re, "info" : info})
        if password == re:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(nick=nick, username=username, password=password, info=info).save()
            return redirect("signin")
        else:
            messages.info(request, "비밀번호가 같지 않습니다.")
            return render(request, "signup.html", {"nick" : nick, "id" : username, "password" : password, "re" : re, "info" : info})
    return render(request, "signup.html", {"nick" : "", "id" : "", "password" : "", "re" : "", "info" : ""})

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        u = authenticate(username=username, password=password)
        if u:
            login(request, u)
            return redirect("main")
        else:
            messages.info(request, "아이디 또는 비밀번호가 일치하지 않습니다.")
            return render(request, "signin.html", {"username" : username, "password" : password})
    return render(request, "signin.html", {"username" : "", "password" : ""})

def signout(request):
    logout(request)
    return redirect("main")

def info(request, username):
    user = User.objects.filter(username=username)[0]
    context = {
        "sub" : len(user.sub.split(" ")) - 1,
        "user" : user
    }
    if not request.user.username in user.sub.split(" "):
        context["subscribe"] = "🤍"
    else:
        context["subscribe"] = "❤️"
    return render(request, "info.html", context)

def chinfo(request):
    if request.method == "POST":
        nick = request.POST.get("nick")
        username = request.POST.get("username")
        info = request.POST.get("info")
        if nick == "":
            messages.info(request, "닉네임은 빈칸일 수 없습니다.")
            return render(request, "chinfo.html", {"nick" : nick, "username" : username, "info" : info})
        if User.objects.filter(username=username).exists() and username != request.user.username:
            messages.info(request, "아이디가 중복됩니다.")
            return render(request, "chinfo.html", {"nick" : nick, "username" : username, "info" : info})
        if username == "":
            messages.info(request, "아이디는 빈칸일 수 없습니다.")
            return render(request, "chinfo.html", {"nick" : nick, "username" : username, "info" : info})
        for i in username:
            if not i in id_filter:
                messages.info(request, "아이디는 영어, 숫자, _만 사용 가능합니다.")
                return render(request, "chinfo.html", {"nick" : nick, "username" : username, "info" : info})
        for i in Video.objects.filter(username=request.user.username):
            i.username = username
            i.save()
        request.user.nick = nick
        request.user.username = username
        request.user.info = info
        request.user.save()
        return redirect(f"/info/{username}")
    return render(request, "chinfo.html", {"nick" : request.user.nick, "username" : request.user.username, "info" : request.user.info})

def chpass(request):
    opassword = ""
    npassword = ""
    if request.method == "POST":
        opassword = request.POST.get("opass")
        npassword = request.POST.get("npass")
        if check_password(opassword, request.user.password):
            request.user.set_password(npassword)
            request.user.save()
            return redirect("signin")
    return render(request, "chpass.html")

def deluser(request):
    request.user.delete()
    return redirect("main")

def subscribe(request, username, idx):
    user = User.objects.filter(username=username)[0]
    if request.user.username != username:
        if not request.user.username in user.sub.split(" "):
            user.sub += f"{request.user.username} "
        else:
            user.sub = user.sub.replace(f"{request.user.username} ", "")
        user.save()
    if idx == "0":
        return redirect(f"/info/{username}")
    else:
        return redirect(f"/watch/{idx}")

def upload(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            username = request.user.username
            sub = request.POST.get("sub")
            info = request.POST.get("info")
            thumbnail = request.FILES.get("thumbnail")
            video = request.FILES.get("video")
            genre = request.POST.get("genre")
            if not genre in gr:
                messages.info(request, "Don't crack")
                return render(request, "upload.html", {"sub" : sub, "info" : info, "thumbnail" : thumbnail, "video" : video, "genre" : gr})
            Video(username=username, sub=sub, info=info, thumbnail=thumbnail, video=video, genre=genre).save()
            request.user.video += f"{sub}!)#*"
            request.user.save()
            return redirect("main")
        else:
            messages.info(request, "로그인 후 이용해주세요")
            return redirect("signin")
    return render(request, "upload.html", {"sub" : "", "info" : "", "thumbnail" : "", "video" : "", "genre" : gr})

def chvideo(request, idx):
    video = Video.objects.filter(idx=idx)[0]
    context = {
        "video" : video,
        "genre" : gr
    }
    if request.method == "POST":
        if request.user.username == video.username:
            sub = request.POST.get("sub")
            info = request.POST.get("info")
            thumbnail = request.FILES.get("thumbnail")
            videofile = request.FILES.get("video")
            genre = request.POST.get("genre")
            if not genre in gr:
                messages.info(request, "Don't crack")
                return render(request, "upload.html", {"sub" : sub, "info" : info, "thumbnail" : thumbnail, "video" : videofile, "genre" : gr})
            request.user.video = request.user.video.replace(f"{video.sub} ", f"{sub} ")
            video.sub = sub
            video.info = info
            if thumbnail != None:
                video.thumbnail = thumbnail
            if videofile != None:
                video.video = video
            video.genre = genre
            request.user.save()
            video.save()
            return redirect(f"/watch/{idx}")
        else:
            messages.info(request, "로그인 후 이용해주세요")
            return redirect("signin")
    return render(request, "chvideo.html", context)

def delvideo(request, idx):
    video = Video.objects.filter(idx=idx)[0]
    VideoBackUp(username=video.username, sub=video.sub, info=video.info, thumbnail=video.thumbnail, video=video.video, genre=video.genre).save()
    os.system(f"rm media/{video.thumbnail}")
    os.system(f"rm media/{video.video}")
    video.delete()
    return redirect("main")

def watch(request, idx):

    if idx == "":
        return render(request, "404.html")
    if not Video.objects.filter(idx=idx).exists():
        return render(request, "404.html")
    video = Video.objects.filter(idx=idx)[0]
    user = User.objects.filter(username=video.username)[0]
    sub = len(user.sub.split(" ")) - 1
    like = len(video.like.split(" ")) - 1

    context = {
        "video" : video,
        "user" : user,
        "sub" : sub,
        "like" : like
    }

    if not request.user.username in user.sub.split(" "):
        context["subscribe"] = "🤍"
    else:
        context["subscribe"] = "❤️"
    if not request.user.username in video.like.split(" "):
        context["liking"] = "✊🏻"
    else:
        context["liking"] = "👍🏻"

    return render(request, "watch.html", context)

def like(request, idx):
    video = Video.objects.filter(idx=idx)[0]
    if not request.user.username in video.like.split(" "):
        video.like += f"{request.user.username} "
    else:
        video.like = video.like.replace(f"{request.user.username} ", "")
    video.save()
    return redirect(f"/watch/{idx}")
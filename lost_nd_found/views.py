from datetime import datetime
from django.shortcuts import render, redirect
from .models import UserTable, ItemTable, Complaints, Found


def userlogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = UserTable.objects.filter(username=username, password=password).first()
        if user:
            request.session["user_id"] = user.id
            if user.is_admin:
                return redirect("adminhome")
            else:
                return redirect("userhome")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")


def adminhome(request):
    if not is_admin_user(request):
        return redirect("login")
    return render(request, 'adminhome.html')


def userhome(request):
    if not is_logged_in(request):
        return redirect("login")
    return render(request, 'user_home.html')


def viewuser(request):
    if not is_admin_user(request):
        return redirect("login")
    data = UserTable.objects.all()
    return render(request, 'view_user.html', {"data": data})


def viewitems(request):
    if not is_logged_in(request):
        return redirect("login")
    data = ItemTable.objects.all()
    return render(request, 'view_items.html', {"data": data})


def viewfound(request):
    if not is_logged_in(request):
        return redirect("login")
    return render(request, 'view_found.html')


def viewcomplaint(request):
    if not is_admin_user(request):
        return redirect("login")
    data = Complaints.objects.all()
    return render(request, 'view_complaint.html', {"data": data})


def reply(request, id):
    if not is_admin_user(request):
        return redirect("login")
    ob = Complaints.objects.get(id=id)
    if request.method == "POST":
        ob.reply = request.POST["reply"]
        ob.save()
        return redirect("viewcomplaint")
    return render(request, 'reply.html', {"ob": ob})


def viewprofile(request):
    if not is_logged_in(request):
        return redirect("login")
    id = request.session.get("user_id")
    ob = UserTable.objects.get(id=id)
    if request.method == "POST":
        ob.name = request.POST["name"]
        ob.place = request.POST["place"]
        ob.pin = request.POST["pin"]
        ob.phone = request.POST["phone"]
        ob.email = request.POST["email"]
        if "image" in request.FILES:
            ob.image = request.FILES["image"]
        ob.save()
        return redirect("userhome")
    return render(request, 'viewprof.html', {"ob": ob})


def changepass(request):
    if not is_logged_in(request):
        return redirect("login")
    id = request.session.get("user_id")
    ob = UserTable.objects.get(id=id)
    if request.method == "POST":
        current = request.POST["current_password"]
        new = request.POST["new_password"]
        confirm = request.POST["confirm_password"]
        if ob.password == current:
            if new == confirm:
                ob.password = new
                ob.save()
                return redirect("userhome")
            else:
                return render(request, "change_pass.html", {"error": "New passwords do not match"})
        else:
            return render(request, "change_pass.html", {"error": "Current password is wrong"})
    return render(request, 'change_pass.html')


def managelost(request):
    if not is_logged_in(request):
        return redirect("login")
    id = request.session.get("user_id")
    data = ItemTable.objects.filter(userid=id)
    return render(request, 'manage_lost.html', {"data": data})


def addlost(request):
    if not is_logged_in(request):
        return redirect("login")
    if request.method == "POST":
        id = request.session.get("user_id")
        user = UserTable.objects.get(id=id)
        item = request.POST["item"]
        image = request.FILES["image"]
        details = request.POST["details"]
        date = request.POST["date"]
        ItemTable.objects.create(userid=user, item=item, image=image, details=details, date=date, status="pending")
        return redirect("managelost")
    return render(request, 'add_lost.html')


def viewlost(request):
    if not is_logged_in(request):
        return redirect("login")
    data = ItemTable.objects.filter(status='pending').exclude(userid_id=request.session.get("user_id"))
    return render(request, 'view_lost.html', {"data": data})


def updatelost(request, id):
    if not is_logged_in(request):
        return redirect("login")
    dd = ItemTable.objects.get(id=id)
    if request.method == "POST":
        ob = Found()
        ob.userid_id = request.session.get("user_id")
        ob.item_id = id
        ob.image = request.FILES['image']
        ob.details = request.POST['details']
        ob.date = datetime.today()
        ob.status = 'found'
        ob.save()
        return redirect('viewlost')
    return render(request, 'update_lost.html', {'ob': dd})


def view_my_found(request):
    if not is_logged_in(request):
        return redirect("login")
    ob = Found.objects.filter(item__userid_id=request.session.get("user_id"))
    return render(request, 'view_my_found.html', {'ob': ob})


def confirm_found(request, id):
    if not is_logged_in(request):
        return redirect("login")
    ob = Found.objects.get(id=id)
    ob.status = 'confirmed'
    ob.save()
    dd = ItemTable.objects.get(id=ob.item_id)
    dd.status = 'found'
    dd.save()
    return redirect('view_my_found')


def viewreply(request):
    if not is_logged_in(request):
        return redirect("login")
    id = request.session.get("user_id")
    data = Complaints.objects.filter(userid=id)
    return render(request, 'view_reply.html', {'data': data})


def sendcomplaint(request):
    if not is_logged_in(request):
        return redirect("login")
    if request.method == "POST":
        id = request.session.get("user_id")
        user = UserTable.objects.get(id=id)
        complaint = request.POST["complaint"]
        date = request.POST["date"]
        Complaints.objects.create(userid=user, complaint=complaint, date=date)
        return redirect("viewreply")
    return render(request, 'send_complain.html')


def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        place = request.POST["place"]
        pin = request.POST["pin"]
        image = request.FILES["image"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        UserTable.objects.create(name=name, place=place, pin=pin, image=image, phone=phone, email=email, username=username, password=password)
        return redirect("login")
    return render(request, "register.html")


def editlost(request, id):
    if not is_logged_in(request):
        return redirect("login")
    ob = ItemTable.objects.get(id=id)
    if request.method == "POST":
        ob.item = request.POST["item"]
        ob.details = request.POST["details"]
        ob.date = request.POST["date"]
        if "image" in request.FILES:
            ob.image = request.FILES["image"]
        ob.save()
        return redirect("managelost")
    return render(request, "add_lost.html", {"ob": ob})


def deletelost(request, id):
    if not is_logged_in(request):
        return redirect("login")
    ob = ItemTable.objects.get(id=id)
    ob.delete()
    return redirect("managelost")


def userlogout(request):
    request.session.flush()
    return redirect("login")


def is_logged_in(request):
    return request.session.get("user_id") is not None


def is_admin_user(request):
    id = request.session.get("user_id")
    if id:
        user = UserTable.objects.filter(id=id).first()
        return user and user.is_admin
    return False

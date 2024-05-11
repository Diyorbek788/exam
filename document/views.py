from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Note

@login_required(login_url='/login/')
def editor(request):
    docid = request.GET.get('docid', None)
    note = None
    if docid and docid != '0':  
        note = get_object_or_404(Note, pk=docid, user=request.user)
    if request.method == 'POST':
        docid = request.POST.get('docid')
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        if docid:  
            note = get_object_or_404(Note, pk=docid, user=request.user)
            note.title = title
            note.content = content
            note.save()
        else:  
            note = Note.objects.create(title=title, content=content, user=request.user)
        return redirect('/editor/?docid=%s' % note.id)
    
    notes = Note.objects.filter(user=request.user)
    return render(request, 'editor.html', {'note': note, 'notes': notes})

@login_required(login_url='/login/')
def delete_note(request, docid):
    note = get_object_or_404(Note, pk=docid, user=request.user)
    note.delete()
    return redirect('/editor/')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/editor/')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/editor/')
        else:
            messages.error(request, "Username or password is incorrect")
    return render(request, "login.html")

def register_page(request):
    if request.user.is_authenticated:
        return redirect('/editor/')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Registration successful.")
            return redirect('/login/')
    return render(request, "register.html")

def custom_logout(request):
    logout(request)
    return redirect('/login/')


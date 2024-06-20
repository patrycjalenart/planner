from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Planner

# Create planner page
from django.shortcuts import render, redirect
from .models import Planner
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required(login_url='/login/')
def planner(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        name = request.POST.get('name')
        description = request.POST.get('description')

        if day and name and description:
            planner = Planner.objects.create(day=day, name=name, description=description)
            if planner:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': False})

    queryset = Planner.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(day__icontains=request.GET.get('search'))

    context = {'planners': queryset}  # Fix the context variable name to match 'planners'
    return render(request, 'planner.html', context)

# Update planner data
@login_required(login_url='/login/')
def update_planner(request, id):
    queryset = Planner.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        day = data.get('day')
        name = data.get('name')
        description = data.get('description')

        queryset.day = day
        queryset.name = name
        queryset.description = description
        queryset.save()
        return redirect('planner')

    context = {'planner': queryset}
    return render(request, 'update_planner.html', context)

# Delete planner data
@login_required(login_url='/login/')
def delete_planner(request, id):
    planner = get_object_or_404(Planner, id=id)
    if request.method == 'POST':
        planner.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Login page for user
def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                messages.error(request, "Username not found")
                return redirect('login')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('planner')
            else:
                messages.error(request, "Wrong Password")
                return redirect('login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('register')
    return render(request, "login.html")

# Register page for user
def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first()
            if user_obj:
                messages.error(request, "Username is taken")
                return redirect('register')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('register')
    return render(request, "register.html")

# Logout function
@login_required(login_url='/login/')
def custom_logout(request):
    logout(request)
    return redirect('login')

# Generate PDF (not used in the provided views)
def pdf(request):
    queryset = Planner.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(
            day__icontains=request.GET.get('search'))

    context = {'planner': queryset}
    return render(request, 'pdf.html', context)

# Show URLs for debugging
def show_urls(request):
    from django.urls import get_resolver
    url_patterns = get_resolver().url_patterns
    output = ""
    for pattern in url_patterns:
        output += f"{pattern.pattern}\n"
    return HttpResponse(f"<pre>{output}</pre>")


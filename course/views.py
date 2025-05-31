from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from openpyxl import load_workbook # For course planner
import os # For course planner path & material serving
from django.conf import settings # For course planner path & media settings
from .models import CourseMaterial # Import the CourseMaterial model
from django.http import HttpResponseForbidden, FileResponse # For serving files

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                students_group = Group.objects.get(name='Students')
                user.groups.add(students_group)
            except Group.DoesNotExist:
                print("Warning: 'Students' group not found. User not added to group.")
            login(request, user)
            return redirect('course:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'course/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', reverse_lazy('course:dashboard'))
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'course/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('course:login')

@login_required
def dashboard_view(request):
    is_instructor = request.user.groups.filter(name='Instructors').exists()
    return render(request, 'course/dashboard.html', {'is_instructor': is_instructor})

@login_required
def course_planner_view(request):
    planner_data = []
    headers = []
    file_path = os.path.join(settings.BASE_DIR, 'course', 'data', 'planner.xlsx')
    try:
        workbook = load_workbook(filename=file_path, read_only=True)
        sheet = workbook.active
        header_cells = sheet[1]
        headers = [cell.value for cell in header_cells]
        for row_idx, row_cells in enumerate(sheet.iter_rows(min_row=2)):
            if not any(cell.value for cell in row_cells):
                break
            row_data = {headers[col_idx]: cell.value for col_idx, cell in enumerate(row_cells) if col_idx < len(headers)}
            planner_data.append(row_data)
    except FileNotFoundError:
        print(f"Planner file not found at {file_path}")
    except Exception as e:
        print(f"Error reading planner file: {e}")
    return render(request, 'course/course_planner.html', {'planner_data': planner_data, 'headers': headers})

@login_required
def course_materials_list_view(request):
    materials = CourseMaterial.objects.all().order_by('material_type', 'uploaded_at')
    return render(request, 'course/course_materials_list.html', {'materials': materials})

@login_required
def serve_protected_material(request, material_id):
    try:
        material = CourseMaterial.objects.get(pk=material_id)
    except CourseMaterial.DoesNotExist:
        return HttpResponseForbidden("Material not found.")

    # TODO: Implement actual payment check here.
    file_path = os.path.join(settings.MEDIA_ROOT, str(material.file))
    if not os.path.exists(file_path):
        print(f"ERROR: File not found for material ID {material_id} at path {file_path}")
        return HttpResponseForbidden("File not found on server. Please contact an administrator.")
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(material.file.name))

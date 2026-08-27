from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProjectForm,TaskForm,TeamMemberForm,CommentForm
from .models import Project, Task, TeamMember,Comment,Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import date
@login_required
def home(request):
    # Project statistics - current user only
    total_projects = Project.objects.filter(
        user=request.user
    ).count()

    planning = Project.objects.filter(
        user=request.user,
        status="Planning"
    ).count()

    in_progress = Project.objects.filter(
        user=request.user,
        status="In Progress"
    ).count()

    completed = Project.objects.filter(
        user=request.user,
        status="Completed"
    ).count()

    # Task statistics - current user only
    total_tasks = Task.objects.filter(
        user=request.user
    ).count()

    pending_tasks = Task.objects.filter(
        user=request.user,
        status="Pending"
    ).count()

    in_progress_tasks = Task.objects.filter(
        user=request.user,
        status="In Progress"
    ).count()

    completed_tasks = Task.objects.filter(
        user=request.user,
        status="Completed"
    ).count()

    # Recent tasks - current user only
    recent_tasks = Task.objects.filter(
        user=request.user
    ).order_by('-id')[:5]

    # Recent projects - current user only
    recent_projects = Project.objects.filter(
        user=request.user
    ).order_by('-id')[:5]

    # Notifications
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')
    return render(request, 'home.html', {
        'total_projects': total_projects,
        'planning': planning,
        'in_progress': in_progress,
        'completed': completed,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'recent_tasks': recent_tasks,
        'recent_projects': recent_projects,
        'notifications': notifications,
    })
@login_required
def profile(request):
    return render(request, 'profile.html')
@login_required
def settings(request):
    return render(request, 'settings.html')
@login_required
def projects(request):
    status = request.GET.get('status')

    if status:
        projects = Project.objects.filter(
            user=request.user,
            status=status
        )
    else:
        projects = Project.objects.filter(
            user=request.user
        )

    return render(request, 'projects.html', {'projects': projects})
@login_required
def project_detail(request, id):
    project = get_object_or_404(
        Project,
        id=id,
        user=request.user
    )

    return render(request, 'project_detail.html', {
        'project': project
    })
@login_required
def edit_project(request, id):
    project = get_object_or_404(
        Project,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect('projects')

    else:
        form = ProjectForm(instance=project)

    return render(request, 'edit_project.html', {
        'form': form
    })
@login_required
def delete_project(request, id):
    project = get_object_or_404(
        Project,
        id=id,
        user=request.user
    )

    project.delete()
    return redirect('projects')
@login_required
def edit_task(request, id):
    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()

            Notification.objects.create(
                user=request.user,
                message=f"Task updated: {task.task_name}"
            )

            return redirect('tasks')

    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form})
@login_required
def delete_task(request, id):
    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )

    task_name = task.task_name
    task.delete()

    Notification.objects.create(
        user=request.user,
        message=f"Task deleted: {task_name}"
    )

    return redirect('tasks')
@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('projects')
    else:
        form = ProjectForm()

    return render(request, 'add_project.html', {'form': form})
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)

    today = date.today()

    for task in tasks:
        if task.due_date:
            if task.due_date == today:
                Notification.objects.get_or_create(
                    user=request.user,
                    message=f"Task due today: {task.task_name}"
                )
            elif task.due_date < today:
                Notification.objects.get_or_create(
                    user=request.user,
                    message=f"Task overdue: {task.task_name}"
                )

    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')
    return render(request, 'tasks.html', {
        'tasks': tasks,
        'projects': projects,
        'notifications': notifications,
    })
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(
    Task,
    id=task_id,
    user=request.user
)
    comments = task.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.save()
            Notification.objects.create(
                user=request.user,
                message=f"New comment added to task: {task.task_name}"
            )
            return redirect('task_detail', task_id=task.id)
    else:
        form = CommentForm()

    return render(request, 'task_detail.html', {
        'task': task,
        'comments': comments,
        'form': form,
    })

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            Notification.objects.create(
                user=request.user,
                message=f"New task added: {task.task_name}"
            )

            return redirect('tasks')

    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})
@login_required
def team(request):
    members = TeamMember.objects.filter(
        user=request.user
    )
    return render(request, 'team.html', {'members': members})
@login_required
def add_team_member(request):
    if request.method == "POST":
        form = TeamMemberForm(request.POST)

        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            return redirect('team')

    else:
        form = TeamMemberForm()

    return render(request, 'add_team_member.html', {'form': form})
@login_required
def delete_team_member(request, id):
    member = get_object_or_404(
        TeamMember,
        id=id,
        user=request.user
    )

    member.delete()
    return redirect('team')
@login_required
def edit_team_member(request, id):
    member = get_object_or_404(
        TeamMember,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = TeamMemberForm(request.POST, instance=member)

        if form.is_valid():
            form.save()
            return redirect('team')

    else:
        form = TeamMemberForm(instance=member)

    return render(request, 'edit_team_member.html', {'form': form})
def user_logout(request):
    logout(request)
    return render(request, 'logout.html')
# Create your views here.

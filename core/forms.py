from django import forms
from .models import Project, Task,Comment,TeamMember

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['project_name', 'description', 'status', 'start_date', 'due_date']

        widgets = {
            'project_name': forms.TextInput(attrs={
                'placeholder': 'Enter Project Name'
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter Project Description',
                'rows': 4
            }),

            'start_date': forms.TextInput(attrs={
                'placeholder': 'YYYY-MM-DD'
            }),

            'due_date': forms.TextInput(attrs={
                'placeholder': 'YYYY-MM-DD'
            }),
        }
class TaskForm(forms.ModelForm):

    assigned_to = forms.ModelChoiceField(
        queryset=TeamMember.objects.all(),
        required=False,
        empty_label="Select Team Member"
    )

    status = forms.ChoiceField(
        choices=[
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
        ]
    )

    class Meta:
        model = Task
        fields = [
            'project',
            'task_name',
            'description',
            'status',
            'priority',
            'due_date',
            'assigned_to'
        ]

        widgets = {
            'project': forms.Select(),

            'task_name': forms.TextInput(attrs={
                'placeholder': 'Enter Task Name'
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter Task Description',
                'rows': 4
            }),

            'status': forms.Select(),

            'priority': forms.Select(
                choices=[
                    ('Low', 'Low'),
                    ('Medium', 'Medium'),
                    ('High', 'High'),
                ]
            ),

            'due_date': forms.TextInput(attrs={
                'placeholder': 'YYYY-MM-DD'
            }),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
class TeamMemberForm(forms.ModelForm):

    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'email']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter Name'
            }),

            'role': forms.TextInput(attrs={
                'placeholder': 'Enter Role'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter Email'
            }),
        }
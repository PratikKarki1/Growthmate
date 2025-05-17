from django import forms
from .models import Course, CourseThumbnail

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class CourseForm(forms.ModelForm):
    thumbnails = MultipleFileField(
        required=False,
        help_text="You can select multiple images"
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'duration', 'level', 
                 'prerequisites', 'objectives', 'target_audience', 'is_active', 
                 'is_featured', 'certificate_available', 'max_students']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'prerequisites': forms.Textarea(attrs={'rows': 3}),
            'objectives': forms.Textarea(attrs={'rows': 3}),
            'target_audience': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        course = super().save(commit=False)
        if commit:
            course.save()
            # Handle multiple thumbnails
            thumbnails = self.files.getlist('thumbnails')
            for i, thumbnail in enumerate(thumbnails):
                CourseThumbnail.objects.create(
                    course=course,
                    image=thumbnail,
                    is_primary=(i == 0),  # First image is primary
                    order=i
                )
        return course 
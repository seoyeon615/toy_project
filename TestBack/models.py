from django.db import models
from django.conf import settings

class Course(models.Model):
    course_number = models.CharField(max_length=20, unique=True, help_text="과목 번호 (학수번호)")
    subject = models.CharField(max_length=100, help_text="과목명")
    professor = models.CharField(max_length=50, help_text="담당 교수")

    def __str__(self):
        return f"[{self.course_number}] {self.subject} - {self.professor} 교수님"


class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='tests', help_text="대상 과목 선택")
    
    exam_type = models.CharField(max_length=20, help_text="시험 종류 (중간/기말 등)")
    test_format = models.CharField(max_length=50, help_text="시험 유형 (객관식/주관식 등)")
    rating = models.PositiveIntegerField(default=3, help_text="난이도 별점 (1~5)")
    
    title = models.CharField(max_length=200, help_text="후기 제목")
    content = models.TextField(help_text="총평 및 내용")
    views = models.PositiveIntegerField(default=0, help_text="조회수")
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tests', help_text="작성자")
    created_at = models.DateTimeField(auto_now_add=True, help_text="작성일시")

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_tests', blank=True, help_text="좋아요 누른 유저들")
    scraps = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='scrapped_tests', blank=True, help_text="스크랩한 유저들")

    def __str__(self):
        return f"[{self.course.subject}] {self.title}"

class Comment(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_anonymous_number(self):
        users = Comment.objects.filter(
            test=self.test,
            is_anonymous=True
        ).order_by('created_at').values_list('user_id', flat=True)
        ordered = list(dict.fromkeys(users))
        return ordered.index(self.user_id) + 1

    def __str__(self):
        return f"[{self.test.title}] {self.content[:20]}"
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Test, Course

@login_required
def test_create(request):
    if request.method == 'POST':
        subject_name = request.POST.get('subject')
        professor_name = request.POST.get('professor')
        exam_type = request.POST.get('exam_type')
        test_format = request.POST.get('test_format')
        rating = request.POST.get('rating', 3)
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        course, created = Course.objects.get_or_create(
            subject=subject_name,
            professor=professor_name,
            defaults={'course_number': f"TEMP_{subject_name}"}
        )
        
        test = Test.objects.create(
            course=course,
            exam_type=exam_type,
            test_format=test_format,
            rating=int(rating),
            title=title,
            content=content,
            user=request.user
        )
        return redirect('TestBack:test_detail', pk=test.pk)
        
    return render(request, 'TestBack/test_form.html')

def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    test.views += 1
    test.save()
    
    author_other_tests = Test.objects.filter(user=test.user).exclude(pk=pk).order_by('-created_at')[:3]
    
    return render(request, 'TestBack/test_detail.html', {
        'test': test,
        'author_other_tests': author_other_tests
    })

@login_required
def test_update(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if test.user != request.user:
        return redirect('TestBack:test_detail', pk=pk)
    
    if request.method == 'POST':
        subject_name = request.POST.get('subject')
        professor_name = request.POST.get('professor')
        
        course, created = Course.objects.get_or_create(
            subject=subject_name,
            professor=professor_name,
            defaults={'course_number': f"TEMP_{subject_name}"}
        )
        
        test.course = course
        test.exam_type = request.POST.get('exam_type')
        test.test_format = request.POST.get('test_format')
        test.rating = int(request.POST.get('rating', 3))
        test.title = request.POST.get('title')
        test.content = request.POST.get('content')
        test.save()
        return redirect('TestBack:test_detail', pk=pk)
        
    return render(request, 'TestBack/test_form.html', {'test': test})

@login_required
def test_delete(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if test.user == request.user:
        test.delete()
    return redirect('TestBack:test_list')

def test_list(request):
    sort = request.GET.get('sort', 'latest')
    search_keyword = request.GET.get('search', '')
    
    tests = Test.objects.all()
    
    if search_keyword:
        tests = tests.filter(
            Q(title__icontains=search_keyword) | 
            Q(course__subject__icontains=search_keyword) | 
            Q(content__icontains=search_keyword)
        )
        
    if sort == 'likes':
        tests = tests.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    else:
        tests = tests.annotate(like_count=Count('likes')).order_by('-created_at')
        
    paginator = Paginator(tests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'TestBack/test_list.html', {
        'page_obj': page_obj, 
        'sort': sort,
        'search_keyword': search_keyword
    })

@login_required
def test_like(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if test.likes.filter(id=request.user.id).exists():
        test.likes.remove(request.user)
    else:
        test.likes.add(request.user)
    return redirect('TestBack:test_detail', pk=pk)

@login_required
def test_scrap(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if test.scraps.filter(id=request.user.id).exists():
        test.scraps.remove(request.user)
    else:
        test.scraps.add(request.user)
    return redirect('TestBack:test_detail', pk=pk)
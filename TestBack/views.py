from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Test, Course, Comment

from django.db import IntegrityError
from django.http import HttpResponse

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
        try:
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
            
        except IntegrityError:
            response_html = "<script>alert('⚠️ 이미 등록된 시험 정보이거나 중복된 데이터가 존재합니다.');history.back();</script>"
            return HttpResponse(response_html)
        
    return render(request, 'TestBack/test_form.html')

def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    
    skip_view = request.session.pop('skip_view_count', False)
    
    if not skip_view:
        if request.user.is_authenticated and test.user != request.user:
            test.views += 1
            test.save()
        elif not request.user.is_authenticated:
            test.views += 1
            test.save()
    
    author_other_tests = Test.objects.filter(user=test.user).exclude(pk=pk).order_by('-created_at')[:3]

    # 수정할 댓글 불러오기
    edit_comment = None
    edit_comment_id = request.GET.get('edit_comment')
    if edit_comment_id:
        edit_comment = get_object_or_404(Comment, id=edit_comment_id, user=request.user)
    
    return render(request, 'TestBack/test_detail.html', {
        'test': test,
        'author_other_tests': author_other_tests,
        'edit_comment': edit_comment,
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
    elif sort == 'views':
        tests = tests.annotate(like_count=Count('likes')).order_by('-views', '-created_at')
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
    
    if test.user == request.user:
        response_html = "<script>alert('❌ 본인 글에는 좋아요를 누를 수 없습니다.');history.back();</script>"
        return HttpResponse(response_html)
        
    if test.likes.filter(id=request.user.id).exists():
        test.likes.remove(request.user)
    else:
        test.likes.add(request.user)
        
    request.session['skip_view_count'] = True
    return redirect('TestBack:test_detail', pk=pk)

@login_required
def test_scrap(request, pk):
    test = get_object_or_404(Test, pk=pk)
    
    if test.user == request.user:
        response_html = "<script>alert('❌ 본인 글은 스크랩할 수 없습니다.');history.back();</script>"
        return HttpResponse(response_html)
        
    if test.scraps.filter(id=request.user.id).exists():
        test.scraps.remove(request.user)
    else:
        test.scraps.add(request.user)
        
    request.session['skip_view_count'] = True
    return redirect('TestBack:test_detail', pk=pk)

@login_required
def comment_create(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        parent_id = request.POST.get('parent_id') 

        Comment.objects.create(
            test=test,
            user=request.user,
            content=content,
            is_anonymous=is_anonymous,
            parent_id=parent_id if parent_id else None
        )
    request.session['skip_view_count'] = True
    return redirect('TestBack:test_detail', pk=pk)

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
    request.session['skip_view_count'] = True
    return redirect('TestBack:test_detail', pk=comment.test.pk)

@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('TestBack:test_detail', pk=comment.test.pk)

    if request.method == 'POST':
        comment.content = request.POST.get('content')
        comment.save()
    request.session['skip_view_count'] = True
    return redirect('TestBack:test_detail', pk=comment.test.pk)

@login_required
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    # 🌟 댓글 좋아요 시 조회수 스킵
    request.session['skip_view_count'] = True
    return redirect('TestBack:test_detail', pk=comment.test.pk)
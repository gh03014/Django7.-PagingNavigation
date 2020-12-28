from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from pip._vendor.requests import Response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from board.models import Board

def home(request):
    return render(request, 'home.html')

def board(request):
    # 가장 번호가 큰 게시물 순서로 정렬
    total_list = Board.objects.all().order_by('-b_no')

    page_row = 10 # 한 페이지 당 게시글 갯수
    page_window = 10 # 한 페이지에 표시할 페이징 번호 범위
    page = request.GET.get('page', 1)# 페이지
    paginator = Paginator(total_list, page_row)
    totalPageCount = paginator.num_pages  # 전체 페이지 갯수
    rsBoard = paginator.page(page)

    # page값이 정수형이 아닐 경우 1 페이지, 빈값이면 마지막 페이지로 설정한다
    #try:
    #    rsBoard = paginator.page(page)
    #except PageNotAnInteger:
    #    rsBoard = paginator.page(1)
    #    page = 1
    #except EmptyPage:
    #    rsBoard = paginator.page(paginator.num_pages)
    #    page = paginator.num_pages

    page = int(page)
    startPageNum = int((page - 1) / page_window) * page_window + 1 # 가장 왼쪽 페이징 번호
    endPageNum = startPageNum + page_window - 1 #가장 오른쪽 페이징 번호
    # 가장 오른쪽에 위치한 페이징 번호는 마지막 페이지 보다 크면 안된다
    if totalPageCount < endPageNum:
        endPageNum = totalPageCount
    bottomPages = range(int(startPageNum), int(endPageNum + 1))

    before_window = startPageNum - 1
    next_window = endPageNum + 1

    return render(request, "board_list.html", {
        'rsBoard': rsBoard,
        'page': page,
        'page_window': page_window,
        'bottomPages': bottomPages,
        'totalPageCount': totalPageCount,
        'startPageNum': startPageNum,
        'endPageNum': endPageNum,
        'before_window': before_window,
        'next_window': next_window
    })

def board_write(request):
    return render(request, "board_write.html", )

def board_insert(request):
    btitle = request.GET['b_title']
    bnote = request.GET['b_note']
    bwriter = request.GET['b_writer']

    if btitle != "":
        rows = Board.objects.create(b_title=btitle, b_note=bnote, b_writer=bwriter)
        return redirect('/board')
    else:
        return redirect('/board_write')

def board_view(request):
    bno = request.GET['b_no']
    rsDetail = Board.objects.filter(b_no=bno)

    return render(request, "board_view.html", {
        'rsDetail': rsDetail
    })

def board_edit(request):
    bno = request.GET['b_no']
    rsDetail = Board.objects.filter(b_no=bno)

    return render(request, "board_edit.html", {
        'rsDetail': rsDetail
    })

def board_update(request):
    bno = request.GET['b_no']
    btitle = request.GET['b_title']
    bnote = request.GET['b_note']
    bwriter = request.GET['b_writer']

    try:
        board = Board.objects.get(b_no=bno)
        if btitle != "":
            board.b_title = btitle
        if bnote != "":
            board.b_note = bnote
        if bwriter != "":
            board.b_writer = bwriter

        try:
            board.save()
            return redirect('/board')
        except ValueError:
            return Response({"success": False, "msg": "에러입니다."})

    except ObjectDoesNotExist:
        return Response({"success": False, "msg": "게시글 없음"})

def board_delete(request):
    bno = request.GET['b_no']
    rows = Board.objects.get(b_no=bno).delete()

    return redirect('/board')
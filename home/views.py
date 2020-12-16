import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactMessage
from product.models import Product, Comment, Chapter, ChapterImage


def index(request):
    products_slider = Product.objects.all().order_by('id')[:4]  # First 4 product
    slider = Product.objects.all()  # First 4 product
    products_latest = Product.objects.all().order_by('-id')[:3]  # Last 4 product
    products_picked = Product.objects.all().order_by('?')[:12]  # random select 4 product
    page = "home"
    context = {
        'page': page,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
        'slider': slider}
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'about.html', context)


def contactus(request):
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {'setting': setting, 'form': form}
    return render(request, 'contactus.html', context)


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # create relation with model
            catid = form.cleaned_data['catid']  # get form input data
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            context = {'query': query, 'products': products}
            return render(request, 'shopcart_products.html', context)
    return HttpResponseRedirect('/')


def search_auto(request):  # Jqueary Auto Search engine
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_detail(request, id, slug):
    product = Product.objects.get(pk=id)
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite = True
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'product': product,
               'comments': comments,
               'is_favourite': is_favourite}
    return render(request, 'product_detail.html', context)


def Chapters(request, bid, cnum):
    chapters = Chapter.objects.get(books__id=int(bid), chapter_number=int(cnum))
    images = ChapterImage.objects.filter(chapter_obj__id=chapters.id)
    all_chapter = Chapter.objects.filter(books=chapters.books)
    chapters.views= chapters.views + 1
    chapters.save()
    context = {
        'chapters': chapters,
        'images': images,
        'all_chapter': all_chapter,
    }
    return render(request, 'chapter.html', context)


def post_delete(request, id):
    return HttpResponse('Hello Delete')


def favourite_post(request, id):
    post = get_object_or_404(Product, id=id)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect('/')


def post_favourite_list(request):
    user = request.user
    favourite_posts = user.favourite.all()
    context = {
        'favourite_posts': favourite_posts,
    }
    return render(request, 'post_favourite_list.html', context)

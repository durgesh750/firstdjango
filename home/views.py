from django.shortcuts import render,redirect
from .forms import BookForms,SearchForm
from .models import Book
from django.utils import timezone
from django.contrib import messages

# Create your views here.

def form_view(request):
    msg=""
    if request.method=='POST':
        form=BookForms(request.POST)
        if form.is_valid():
           # book=Book(
           #     name=form.cleaned_data.get('name'),
           #     purchase_date=form.cleaned_data.get('pur_data'),
           #     genre=form.cleaned_data.get('genre'),
           #     author=form.cleaned_data.get('author')
           # )
            book=Book.objects.create(
                name=form.cleaned_data.get('name'),
                purchase_date=form.cleaned_data.get('pur_data'),
                # genre=form.cleaned_data.get('genre'),
                book_author=form.cleaned_data.get('author')
            )
            book.save()
            msg='Book Added Sucessfully!!'
        else:
            msg=form.error
    else:
        form=BookForms()
    return render(request,'forms.html',{'msg':msg,'forms':form})



def booksearch(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            q=form.cleaned_data.get('q')
            #book=Book.objects.filter(name__contains=q,purchase_date__lte=timezone.now)
            book=Book.objects.filter(name__contains=q)
            #form=None
            return render(request,'showtables.html',{'book':book,'form':SearchForm()})

    else:
        form=SearchForm()
        book=Book.objects.all()
    return render(request,'showtables.html',{'book':book,'form':form})

def deletebook(request,id):
    book=Book.objects.get(id=id)
    book.delete()
    messages.success(request,'Deleted #'+str(id)+' Sucessfully!!!')

    return redirect('/')

def editbook(request,id):
    book=Book.objects.get(id=id)
    if request.method=='POST':
        form=ModuleBookForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Book Updated Sucessfully!!!')
            return render('/')
    else:
        form=ModelBookForms(instance=book)
        return render(request,'editbookhtml',{'form':form})
    

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from OTS.models import Question, User,Result
import random as ran
# Create your views here.
# admin user
def createAdmin():
    user=User()
    user.username='Admin'
    user.password='admin'
    user.fullname='Super User'
    user.role="ADMIN"
    user.save()
def ots(request):
    
    res=render(request,'OTS/ots.html')
    return res

def signup(request):
    errormsg=''
    try:
        if request.GET['error']=='1':
            errormsg='username has already taken'
    except:
        errormsg=''

    res=render(request,'OTS/signup.html',{'errormsg':errormsg})
    return res

def checkUser(request):
    user=User.objects.filter(username=request.GET['username'])
    
    if not user:
        return HttpResponse("true")
    return HttpResponse("false")

def saveUser(request):
    user=User()
    u=User.objects.filter(username=request.POST['username'])
    if not u:
        user.username=request.POST['username']
        user.fullname=request.POST['fullname']
        user.password=request.POST['password']
        user.role='LEARNER'
        user.save()
        url='/login'
    else:
        url='/signup?error=1'
    return HttpResponseRedirect(url)


def login(request):
    user=User.objects.filter(username="Admin")
    errormsg=''
    if not user:
        createAdmin()
    try:
        if request.GET['username']=='invalid': 
            errormsg='invalid Username'
    except:
        errormsg=''
    try:
        if request.GET['password']=='invalid':
            errormsg='invalid Password'
    except:
        pass
    res=render(request,'OTS/login.html',{'errormsg':errormsg})
    return res

def loginValidation(request):
    url=''
    try:
        user=User.objects.get(username=request.POST['username'])
        if user.username==request.POST['username'] and user.password==request.POST['password']:
            request.session['username']=user.username
            request.session['fullname']=user.fullname
            request.session['role']=user.role
            url='/'
        else:
            url='/login?password=invalid'
    except:
        url='/login?username=invalid'
                


    return HttpResponseRedirect(url)

def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/login')

def newQuestion(request):
    try:
     request.session['role']=='ADMIN'
    except KeyError:
     return HttpResponseRedirect('/login')
    res=render(request,'OTS/new_question.html',)
    return res 

# user test functions

def startTest(request):
    try:
        request.session['username']
    except KeyError:
     return HttpResponseRedirect('/login')
    questions=list()
    questions_pool=list(Question.objects.all())
    ran.shuffle(questions_pool)
    questions=questions_pool[:5]   
     
    res=render(request,'OTS/start_test.html',{'questions':questions})
    return res


def submitTest(request):
    
    qid=list()
    answer=list()
   
    total_right=0
    total_attempt=0
    total_wrong=0
    k=0
    for i in range(5):
        qid.append(request.POST['qid'+str(i+1)])
        answer.append(request.POST['answer'+str(i+1)])
    for i in qid:
        question=Question.objects.get(quno=i)
        if question.answer==answer[k]:
            total_right+=1
            total_attempt+=1
        elif answer[k]=='default':
            pass
        else:
            total_attempt+=1            
            total_wrong+=1            
        k+=1
    result=Result()
    suser=User.objects.get(username=request.session['username'])
    result.total_attempt=total_attempt   
    result.total_wrong=total_wrong
    result.total_right=total_right
    result.user=suser
    result.save()
    d1={'total_right':total_right,'total_wrong':total_wrong,'total_attempt':total_attempt}
    res=render(request,'OTS/submit_test.html',d1)
    return res

def userResults(request):
    result=Result.objects.filter(user=request.session['username'])
    res=render(request,'OTS/results.html',{'result':result})
    return res

def saveQuestion(request):
    question=Question()
    question.que=request.POST['question']
    question.optiona=request.POST['optiona']
    question.optionb=request.POST['optionb']
    question.optionc=request.POST['optionc']
    question.optiond=request.POST['optiond']
    question.answer=request.POST['answer']
    question.save()
    return HttpResponseRedirect('/view-questions')

    
def editQuestion(request):
    try:
     request.session['role']=='ADMIN' 
    except KeyError:
     return HttpResponseRedirect('/login')
    q=request.GET['qun']
    question=Question.objects.get(quno=q)
    res=render(request,'OTS/edit_question.html',{'question':question})
    return res

def editSaveQuestion(request):
    question=Question()
    question.quno=request.POST['quno']
    question.que=request.POST['question']
    question.optiona=request.POST['optiona']
    question.optionb=request.POST['optionb']
    question.optionc=request.POST['optionc']
    question.optiond=request.POST['optiond']
    question.answer=request.POST['answer']
    question.save()
    return HttpResponseRedirect('/view-questions')


def viewQuestions(request):
    try:
     request.session['role']=='ADMIN'
    except KeyError:
     return HttpResponseRedirect('/login')
    questions=Question.objects.all()
    res=render(request,'OTS/view_questions.html',{'questions':questions})
    return res 


def deleteQuestion(request):
    q=request.GET['qun']    
    question=Question.objects.filter(quno=q)
    question.delete()
    return HttpResponseRedirect('/view-questions')
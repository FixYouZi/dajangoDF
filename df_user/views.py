from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from hashlib import sha1
from .models import UserInfo


# Create your views here.
def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码的输入
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd3 = s1.hexdigest()
    # 创建模型类对象
    user = UserInfo()
    user.user_name = uname
    user.pwd = upwd3
    user.uemail = uemail
    user.save()
    # 转到登录页面
    return render(request,'df_user/login.html')

def register_exist (request):
    uname = request.GET.get('uname')
    #返回统计个数
    count = UserInfo.objects.filter(user_name=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context ={'title':'用户登陆','error_name':0,'uname':'name'}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)  # 设置默认值0
    # 根据用户名查询数据
    users = UserInfo.objects.filter(user_name=uname)  # list[]
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        if s1.hexdigest() == users[0].pwd:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')
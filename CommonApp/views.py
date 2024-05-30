from django.contrib import  auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import   WhyChooseUs, Feedback, ReviewUser, Catalog, BasketUser, OrderUser, User, OrderStatus
# Create your views here.
from django.urls import reverse
from .forms import UserLoginForm, FeedBackForm, ReviewForm, OrderStatusForm, UserRegistrationForm
from django.contrib.auth.models import Group
def index(request):
    # Получаем все группы, к которым принадлежит пользователь
    work_status_now = request.user.groups.filter(name="Workers").exists()

    # Получаем название группы пользователя
    context  = {
        'cards_context_why_choose_us':       WhyChooseUs.objects.all(),
        'is_worker_now': work_status_now,
    }
    return render(request,"CommonApp/index.html", context)
def login(request):
    error_post_form = False
    if request.method == "POST":
        user_form_author = UserLoginForm(data = request.POST)
        if user_form_author.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            cur_user =  auth.authenticate(username =username,password = password)
            if cur_user:
                auth.login(request,cur_user)
                return HttpResponseRedirect(reverse('CommonApp:index'))
        error_post_form = True
    else:
        user_form_author =   UserLoginForm()
    context = {
        'login_form' : user_form_author,
        'error_post_form' : error_post_form,
    }
    return render(request,'CommonApp/login_user.html',context)


def about_us(request):
    work_status_now = request.user.groups.filter(name="Workers").exists() # внутрення проверка на принадлежность пользователя
                                                                          # к сотруднику компании
    is_send_feedback = False # установка значения удачной отправки запроса в FALSE по умолчанию
    is_not_send_feedback = False # установка значения неудачной отправки запроса в FALSE по умолчанию
    if request.method == "POST": # проверка на вид запроса(в данном случае запроса с данными)
        feed_back_full_form = FeedBackForm(data=request.POST) # передача данных из запроса для валидации
        if feed_back_full_form.is_valid(): # проверка на валидность данных
            email = request.POST['email'] #получаем почту пользователя из запроса
            request_user = request.POST['user_request_data'] # польчаем сам вопрос пользователя
            new_fead_back = Feedback(email =email, user_request = request_user) # создаем объект нового обращения
            new_fead_back.save() # добавляем новое обращение в базу данных
            is_send_feedback = True # мы устанавливаем бинарное значение флажка успешной отправки запроса в значение «Истина»
        else:
            is_not_send_feedback = True # мы устанавливаем бинарное значение флашка неудачной отправки запроса в
                                        # значение «Истина»
    context= { # создание объекта данных для страницы в формате JSON
        "feed_back_form" : FeedBackForm(), # создаем пустой объект формы для заполнения данных пользователем
        'is_send_feedback': is_send_feedback, # передаем значение переменной успешной отправки запроса
        "is_not_send_feedback":is_not_send_feedback,  # передаем значение переменной неуспешной отправки запроса
        'is_worker_now': work_status_now,# передаем значение внутренней проверки на принадлежность сотрудника к компании

    }
    return  render(request,'CommonApp/about_us.html',context) # открываем нашу страницу по нужному адрес
                                                                           # с данными
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def reviews(request):
    work_status_now = request.user.groups.filter(name="Workers").exists()
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = ReviewUser(user_id = request.user, description = request.POST['description'])
            new_review.save()
            return redirect(request.META.get('HTTP_REFERER'))
    context = {
        "reviews" :  reversed(ReviewUser.objects.all()),
        'review_form': ReviewForm(),
        'is_worker_now': work_status_now,

    }
    return render(request,"CommonApp/reviews.html",  context)

def catalog(request, successful_doing = False):  # создаем функцию(views
    print("оформление заказа статус - ", successful_doing)
    context = { #создаем контекст данные в формате словаря (ключ:значение)
        'cards_products' : Catalog.objects.all(), #обращаемся к базе данных и получаем все доступные товары из каталога
        'successful_doing': successful_doing, #бинарная переменная для проверки на выполнение действий в корзине
    }
    return render(request,"CommonApp/catalog.html",  context) # загружаем страницу catalog.html
                                                                           # и передаем туда ранее созданный context(данные)
@login_required
def add_item_in_catalog(request,id_card):
    check_product_in_basket = BasketUser.objects.filter(user=request.user,product = Catalog.objects.get(id=id_card)).first()
    if check_product_in_basket:
        print("такой товар уже есть")
        check_product_in_basket.count+=1
        check_product_in_basket.save()
    else:
        print("новый товар")
        new_Backet  = BasketUser(user=request.user,product = Catalog.objects.get(id=id_card))
        new_Backet.save()
    return catalog(request,True)
@login_required
def basket(request,succes_result = False):
    work_status_now = request.user.groups.filter(name="Workers").exists() # проверка статуса на принадлежность к работнике
    user_basket = BasketUser.objects.filter(user=request.user) # получение всех товаров корзины пользователя
    res_sum = 0
    for product in user_basket: # цикл для подсчет итоговой стоимости
        res_sum+=product.product.price*product.count
    context = { # создание контекста страницы корзины
        'basket_products' : BasketUser.objects.filter(user=request.user),
        'res_sum' : res_sum,
        'successful_purchase' : succes_result,
        'is_worker_now': work_status_now,

    }
    return render(request,"CommonApp/basket.html",  context)
@login_required
def del_product_in_basket(request,id_product):
    product_in_basket  = BasketUser.objects.filter(user=request.user, product_id=id_product)
    product_in_basket.delete()
    return redirect(request.META.get('HTTP_REFERER'))
@login_required
def minus_count_product_in_basket(request,id_product):
    cur_product = BasketUser.objects.filter(user=request.user,product = Catalog.objects.get(id=id_product)).first()

    cur_product.count-=1
    if cur_product.count==0:
        cur_product.delete()
    else:
        cur_product.save()
    return redirect(request.META.get('HTTP_REFERER'))
@login_required
def plus_count_product_in_basket(request,id_product):
    cur_product = BasketUser.objects.filter(user=request.user,product = Catalog.objects.get(id=id_product)).first()

    cur_product.count+=1
    cur_product.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def go_purchase(request):
    cur_basket_objects = BasketUser.objects.filter(user=request.user)
    sum_order_in_basket = 0
    for product in cur_basket_objects:
        sum_order_in_basket += product.product.price * product.count
    OrderUser(user=request.user,number_order=request.user.number_order, summa_order=sum_order_in_basket,status_order= OrderStatus.objects.get(id=4)).save()
    cur_user = User.objects.get(id=request.user.id)
    cur_user.number_order += 1
    cur_user.save()
    cur_basket_objects.delete()
    return basket(request, True)
@login_required
def personal_profile(request):
    work_status_now = request.user.groups.filter(name="Workers").exists()
    user_orders = OrderUser.objects.filter(user= request.user)

    context = {
        'orders': user_orders,
        'is_worker_now': work_status_now,
    }
    return render(request,'CommonApp/personal_profile.html', context)

@login_required
def working(request):
    if request.method == 'POST': # проверяем, данные пришли к нам или нет
        order_status_form = OrderStatusForm()
    else:
        order_status_form =         OrderStatusForm()
    context = { # создание контеста для страница
        "user_orders": OrderUser.objects.exclude(status_order__name_status__in=['Отменен','Выполнен']),
        'form_status_order': order_status_form,
    }
    return (render(request,'CommonApp/worker.html', context) )

@login_required
def update_status_order_in_worker(request,id_order):
    print(request.POST['name_status'])
    cur_order =         OrderUser.objects.get(id=id_order)
    cur_order.status_order = OrderStatus.objects.get(id=request.POST['name_status'])
    cur_order.save()
    return working(request)
def register(request):
    print("я был тут")
    error_post_form = False
    if request.method == "POST":
        print("я отправил")
        user_form_reg = UserRegistrationForm(data=request.POST)
        print(request.POST)
        if user_form_reg.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            email = request.POST['email']
            new_user = User(username=username, password=password,first_name = firstname,last_name=lastname,email=email)
            new_user.save()
            auth.login(request,new_user)
            return HttpResponseRedirect(reverse('CommonApp:index'))

        print('обвалил на валидации')
        error_post_form = True
    else:
        user_form_reg = UserRegistrationForm()
    context = {
        'reg_form': user_form_reg,
        'error_post_form': error_post_form,
    }
    return render(request,'CommonApp/register.html',context)




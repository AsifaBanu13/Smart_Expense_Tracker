from django.db import models
from django.contrib.auth.models import User

#Create mode for Expense
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default='something')
    price = models.IntegerField(default=0)

    # Import necessary libraries
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User  # Import User model
from .models import Expense

# Create Expense page
@login_required(login_url='/login/')
def expenses(request):
    salary = 0 
    if request.method == 'POST':
        data = request.POST
        salary = int(data.get('salary', 0))
        name = data.get('name')
        price = int(data.get('price', 0))

        Expense.objects.create(
            salary=salary,
            name=name,
            price=price,
        )
        return redirect('/')

    queryset = Expense.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(
            name__icontains=request.GET.get('search'))

    # Calculate the total sum
    total_sum = sum(expense.price for expense in queryset)
    
    context = {'expenses': queryset, 'total_sum': total_sum}
    return render(request, 'expenses.html', context)

# Update the Expenses data
@login_required(login_url='/login/')
def update_expense(request, id):
    queryset = Expense.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        price = int(data.get('price', 0))

        queryset.name = name
        queryset.price = price
        queryset.save()
        return redirect('/')

    context = {'expense': queryset}
    return render(request, 'update_expense.html', context)

# Delete the Expenses data
@login_required(login_url='/login/')
def delete_expense(request, id):
    queryset = Expense.objects.get(id=id)
    queryset.delete()
    return redirect('/')

# Login page for user
def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                messages.error(request, "Username not found")
                return redirect('/login/')
            user_auth = authenticate(username=username, password=password)
            if user_auth:
                login(request, user_auth)
                return redirect('expenses')
            messages.error(request, "Wrong Password")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
    return render(request, "login.html")

# Register page for user
def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    return render(request, "register.html")

# Logout function
def custom_logout(request):
    logout(request)
    return redirect('login')

# Generate the Bill
@login_required(login_url='/login/')
def pdf(request):
    if request.method == 'POST':
        data = request.POST
        salary = int(data.get('salary'))
        name = data.get('name')
        price = int(data.get('price', 0))

        Expense.objects.create(
            salary=salary,
            name=name,
            price=price,
        )
        return redirect('pdf')from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('logout/', views.custom_logout, name="logout"),
    path('pdf/', views.pdf , name='pdf'),
    path('admin/', admin.site.urls),
    path('login/' , views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('', views.expenses, name='expenses'),
    path('update_expense/<id>', views.update_expense, name='update_expense'),
    path('delete_expense/<id>', views.delete_expense, name='delete_expense'),
]

    queryset = Expense.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(
            name__icontains=request.GET.get('search'))

    # Calculate the total sum
    total_sum = sum(expense.price for expense in queryset)
    # Get the username
    username = request.user.username

    context = {'expenses': queryset, 'total_sum': total_sum, 'username':username}
    return render(request, 'pdf.html', context)

from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('logout/', views.custom_logout, name="logout"),
    path('pdf/', views.pdf , name='pdf'),
    path('admin/', admin.site.urls),
    path('login/' , views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('', views.expenses, name='expenses'),
    path('update_expense/<id>', views.update_expense, name='update_expense'),
    path('delete_expense/<id>', views.delete_expense, name='delete_expense'),
]

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{page}}</title>

    <style>
        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
        }

        th,
        td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ccc;
        }

        th {
            background-color: #f2f2f2;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        tr:hover {
            background-color: #ddd;
        }
    </style>
</head>

<body>

    {% block start %}
    {% endblock %}

    <script>
        console.log('Hey Django')
    </script>
</body>

</html>

{% extends "base.html" %}
{% block start %}

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
<style>
  .text {
    color: green;
    font-weight: bold;
    font-family: 'Times New Roman', Times, serif;
  }
  .ok {
    color: white;
    text-decoration: none;
  }
  .ok:hover {
    color: white;
    text-decoration: none;
  }
</style>

<div class="container mt-5 col-6">
 
    <form class="col-6 mx-auto card p-3 shadow-lg" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <br>
        <h4 style="font-family: 'Times New Roman', Times, serif;"> Enter Your Expenses</h4>
        <hr>
      
        <div class="form-group">
          <label for="exampleInputEmail1">Expenses Reason </label>
          <input type="text" name="name" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="exampleInputEmail1">Amount</label>
          <input name="price" type="number" class="form-control" required>
         </div>
        <button type="submit" class="btn btn-success">Add Data</button>
    </form>

    <div class="class mt-5">
        <form action="">
          <button class="btn btn-primary"> <a class="ok" href="{% url 'pdf' %}">Total Expenses  </a></button>
          <button class="btn btn-danger"> <a class="ok" href="{% url 'logout' %}">Logout </a></button>
        </form>

        <table class="table mt-6">
            <thead>
                <tr>
                    <th scope="col">S.No. </th>
                    <th scope="col">Expenses Reason</th>
                    <th scope="col">Amount </th>
                    <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for expense in expenses %}
                <tr>
                    <th scope="row">{{forloop.counter}}</th>
                    <td>{{expense.name}}</td>
                    <td> &#x20B9;{{expense.price}}</td>

                    <td>
                        <a href="/delete_expense/{{expense.id }}" class="btn btn-danger m-2">Delete </a>
                        <a href="/update_expense/{{expense.id }}" class="btn btn-success">Update </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endblock %}

<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <title>Job Portal</title>
</head>
<style>
</style>
<body><br><br><br><br>
   
   <br><br>    
    <div class="container  mt-4 bg-white col-md-3 card shadow p-3 " id="log">
        <div class="login-form">
            {% if messages %}
            {% for message in messages %}
            <div class="alert alert-success {{ message.tags }} mt-4" role="alert">
                {{ message }}
            </div>
            {% endfor %}
            {% endif %}
            <form action="" method="post">
                {% csrf_token %}
                <h4 class="text-center" style="font-family: 'Times New Roman', Times, serif;">  Login </h4>
                <div class="form-group">
                    <input type="text" class="form-control" name="username" placeholder="Username" required
                        style="background-color: #fff; border: 1px solid #ddd; border-radius: 5px; padding: 10px;">
                </div>
                <div class="form-group mt-2">
                    <input type="password" class="form-control" name="password" placeholder="Password" required
                        style="background-color: #fff; border: 1px solid #ddd; border-radius: 5px; padding: 10px;">
                </div>
                <div class="form-group mt-2">
                    <button class="btn btn-success btn-block" style="margin-left: 138px;">Login</button>
                </div>
                <br>
            </form>
            <p class="text-center" style="color: #555;"><a href="{% url 'register' %}" style="color: #007bff;">Create an
                    Account</a></p>
        </div>
    </div>
</body>
</html>

<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <title>Job Portal</title>
</head>

<body>

    <body>
        <br> <br><br><br><br><br>

        <div class="container mt-4   bg-white mx-auto col-md-3 card shadow p-3">
            <div class="login-form">
                {% if messages %}
                {% for message in messages %}
                <div class="alert alert-success {{ message.tags }}" role="alert">
                    {{ message }}
                </div>
                {% endfor %}
                {% endif %}
                <form action="" method="post">
                    {% csrf_token %}
                    <h4 class="text-center" style="font-family: 'Times New Roman', Times, serif;"> Register </h4>
                    <div class="form-group">
                        <input type="text" class="form-control" name="username" placeholder="Username" required>
                    </div>
                    <div class="form-group mt-2">
                        <input type="password" class="form-control" name="password" placeholder="Password" required>
                    </div>
                    <div class="form-group mt-2">
                        <button class="btn btn-success btn-block" style="margin-left: 117px;">Register</button>
                    </div>
                    <br>
                </form>
                <p class="text-center"><a href="{% url 'login' %}">Log In</a></p>
            </div>
        </div>

    </body>

</html>
{% extends "base.html" %}
{% block start %}

<link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
<style>
  .text {
    color: green;
    font-weight: bold;
    font-family: 'Times New Roman', Times, serif;
  }
</style>

<div class="container mt-5 col-5">
  <form class="col-6 mx-auto card p-3 shadow-lg" method="post" enctype="multipart/form-data">
    {% csrf_token %}

    <h4 style="font-family: 'Times New Roman', Times, serif; font-size:20px;">Update Data</h4>
    <hr>
    <div class="form-group">
      <label for="exampleInputEmail1">Expenses Reason</label>
      <input type="text" name="name" value="{{expense.name}}" class="form-control" required>
    </div>
    <div class="form-group">
      <label for="exampleInputEmail1">Amount</label>
      <input name="price" type="number" value="{{expense.price}}" class="form-control" required>
    </div>
    <button type="submit" class="btn btn-danger">Update </button>
  </form>
</div>

{% endblock %}
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Expense</title>

    <!-- Add Bootstrap CSS Link -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Times New Roman', Times, serif;
        }

        .container {
            max-width: 700px;
            margin: 30px auto;
        }

        .expense-container {
            padding: 20px;
            border: 1px solid #000;
            border-radius: 5px;
            background-color: #fff;
            margin-top: 30px;
        }

        .expense-header {
            text-align: center;
        }

        .expense-title {
            font-size: 24px;
            color: #333;
            margin-top: 20px;
        }

        .expense-table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }

        .expense-table th,
        .expense-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }

        .expense-total {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-top: 20px;
        }

        .expense-footer {
            margin-top: 20px;
            font-size: 16px;
            color: #555;
        }

        .btn-print {
            margin-left: 48%;
            margin-top: 2%;
        }

        img {
            width: 140px;
            height: 150px;
        }

        #date {
            margin-left: 120px;
        }
    </style>
</head>

<body>

    <div class="container expense-container">
        <div class="expense-header">
            <img src="https://i.ibb.co/7QJjfxV/images-1.jpg" alt="">
            <div class="expense-title">
                <h4>{{ username }}, Your Finance Record</h4>
            </div>
        </div>
        <br>

        <table class="expense-table">
            <thead>
                <tr>
                    <th>Expenses Reason</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
                {% for expense in expenses %}
                <tr>
                    <td>{{ expense.name }}</td>
                    <td> &#x20B9;{{ expense.price }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <p class="expense-total">Total Expenses: &#x20B9;{{ total_sum }}</p>
        <div class="expense-footer">
            <p>Dear {{ username }}, You Expenses is &#x20B9;{{total_sum}}.</p>
        </div>
    </div>    
    <!-- Add Bootstrap JS and jQuery -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.min.js"></script>
   
</body>

</html>
error clear in codeing
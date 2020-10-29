<<<<<<< HEAD
=======
import json
import re
import bcrypt
import jwt

>>>>>>> main
from django.http import JsonResponse
from django.views import View
from user.models import User
from my_settings import SECRET_KEY,ALGORITHM
<<<<<<< HEAD
from user.utils import login_decorator
from movie.models import *
from collections import Counter
=======
>>>>>>> main


class SignUpView(View):

    def post(self,request):
        data = json.loads(request.body)

        email_test      ='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        password_test   ='^[A-Za-z0-9]{6,}$'

        try :
            if re.match(email_test, data['email']) == None :
                return JsonResponse({'MESSAGE' : 'EMAIL_ERORR'}, status = 401)

            elif re.match(password_test, data['password']) == None : 
                return JsonResponse({'MESSAGE' : 'PASSWORD_ERROR'}, status = 401)

            elif User.objects.filter(email = data['email']).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL_OVERLAP'}, status = 404)

            else :
                    User.objects.create(
                        name        = data['name'], 
                        email       = data['email'],
                        password    = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode())

                    return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 401)


class LoginView(View):

    def post(self,request):
        data = json.loads(request.body)

        try :
            if User.objects.filter(email=data['email']).exists():

                db_email= User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'),db_email.password.encode('utf-8')) == True:
                    return JsonResponse({'MESSAGE' : 'SUCCESS', 'AUTHORIZATION' : jwt.encode({'id' : db_email.id}, SECRET_KEY, ALGORITHM).decode()}, status=200)
                else : 
                    return JsonResponse({'MESSAGE' : 'EMAIL_OR_PASSWORD_ERROR'}, status=400)
            else :
                return JsonResponse({'MESSAGE' : 'EMAIL_DOES_NOT_EXIST'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)


class StatusSelectorView(View):

    @login_decorator

    def post(self, request):
        try: 
            data    = json.loads(request.body)
            user_id = request.user.id
            movie_id= data['movie_id']
            status  = data['status']


            if not UserStatus.objects.filter(user = user_id, movie = movie_id).exists():
                UserStatus.objects.create(user = user_id, movie = movie_id, status = status)

                return JsonResponse ({'Success': 'Status created'}, status = 200)

            if UserStatus.objects.filter(user = user_id, movie = movie_id, status = status_id).exists():
                UserStatus.objects.delete(user = user_id, movie = movie_id, status = status_id)

                return JsonResponse ({'Success': 'Status deleted'}, status = 200)

            if UserStatus.objects.filter(user = user_id, status = status).exists():
                new_status = UserStatus.objects.get(user = user_id, status = status).status
                new_status.status = status
                new_status.save()

                return JsonResponse ({'Success': 'Status created'}, status = 200)

        except KeyError:

            return JsonResponse ({'Failure': 'Check auth'}, status = 400)

class PreferenceView(View):

    @login_decorator

    def get(self, request):
        print('1')
        user_id         = request.user.id
        allreviewcount  = Review.objects.filter(user = user_id).count
        userfiltered    = Review.objects.filter(user = user_id)

        {dic.get(star_rating.movie.country, 1)+=1 for star_rating in StarRating.objects.filter(user_id=user_id) 
         }

        country_count = dict(Counter([star_rating.movie.country for star_rating in StarRating.objects.filter(user_id = user_id)]))

        dic = {}

        for star_rating in StarRating.objects.filter(user_id =  user_id):
            if not star_rating.movie.country in dic: 
                dic[star_rating.movie.country] = 1 
            else:
                dic[star_rating.movie.country] += 1

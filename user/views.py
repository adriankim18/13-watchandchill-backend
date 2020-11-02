import json
import re
import bcrypt
import jwt
import itertools

from django.http import JsonResponse
from django.views import View
from user.models import User
from my_settings import SECRET_KEY,ALGORITHM

from user.utils import login_decorator
from movie.models import Movies, MoviePhotos, MovieVideos, Cast, People, Genres, MovieGenres, Tags, MovieTags, Services, MovieServices
from collections import Counter
from review.models import StarRating, Comment, CommentLike




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
        user_id         = request.user.id
        name            = User.objects.get(id= user_id).name
        allreviewcount  = StarRating.objects.filter(user = user_id).count()

        country_count = dict(Counter([star_rating.movie.country for star_rating in StarRating.objects.filter(user_id = user_id)]))
        sorted_country = sorted(country_count.items(), key=lambda x: x[1], reverse=True)

        genre = [genreobject.movie.genre.values_list('name', flat= True) for genreobject in StarRating.objects.filter(user_id = user_id)]
        genre_count = dict(Counter(list(itertools.chain.from_iterable(genre))))
        sorted_genre = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)

        return JsonResponse ({'name': name , 'all_review_count': allreviewcount, 'country_rank': sorted_country, 'genre_rank': sorted_genre}, status=200)


class ProfileView(View):
    @login_decorator
    def get(self,request):

        user_id = request.user.id

        user_name = User.objects.get(pk = user_id).name
        user_rating = StarRating.objects.filter(user_id = user_id).count()

        return JsonResponse({'NAME' : user_name, 'COUNT' : user_rating}, status = 200)         



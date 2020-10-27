from django.urls import path
from movie.views import MovieView, ActorView, FrontView

urlpatterns = [
	#path('/movies', MoviesView.as_view()),
	path('/movie/<int:movie_id>', MovieView.as_view()),
	path('/actor/<int:person_id>', ActorView.as_view()),
	path('/front', FrontView.as_view())
]

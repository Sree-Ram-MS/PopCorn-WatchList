from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView    
from django.urls import reverse_lazy
from django. contrib import messages
from imdb import IMDb
from tmdbv3api import TMDb
from tmdbv3api import Movie
from .models import MyFav,UserProfile,Watchlist
from .forms import UserProfileForm


# Create your views here.

class HomeContent(View):
    def get(self, request):
            tmdb = TMDb()
            tmdb.api_key = 'dee4eee45142faa55cf89a2f052e57e6'
            mv=Movie()
            pplr = mv.popular()
            path = "https://www.themoviedb.org/t/p/original"
            mv_list = []

            for i in pplr:
                mv_dict = {
                    "title": i.title,
                    "bgimg": path + i.backdrop_path,
                    "poster": path + i.poster_path,
                    "rate": i.vote_average
                }
                mv_list.append(mv_dict)
            context = {
                    'movie': mv_list
                    }
            return render(request, 'Home.html', context)
    
class Homepage(LoginRequiredMixin,TemplateView):
    template_name = "SideBar.html"


class MovieSearch(View):
    def get(self, request):
        return render(request, 'Search.html')

    def post(self, request):

        tmdb = TMDb()
        tmdb.api_key = 'dee4eee45142faa55cf89a2f052e57e6'

        query = request.POST.get('query')
        ia = IMDb()
        movies = ia.search_movie(query)
        
        film = None
        if movies:
            movie = movies[0]
            ia.update(movie,['main','plot'])

            poster_url = movie.get('full-size cover url') or movie.get('cover url')

            search = Movie().search(query)
            id=search[0].id
            movie_details = Movie().details(id)

            vd=movie_details.trailers.youtube
            link= None
            for i in vd:
                if (i['type'] == "Trailer") and ("official" or "Trailer" in i['name']):
                    link = i['source']
                    trailer = f"https://www.youtube.com/watch?v={i['source']}"
                    break
            if link is None:
                trailer ="https://www.youtube.com/watch?v=aDm5WZ3QiIE&ab"


            film = {
                'movie_id' : movie.get('imdbID'),   
                'title': movie.get('title'),
                'year': movie.get('year'),
                'genres': movie.get('genres', []),
                'cast': movie.get('cast', []),
                'plot': movie.get('plot', ),
                'poster_url': poster_url,
                'runtimes' : movie.get('runtimes'),
                'languages': movie.get('languages'),
                'airdate': movie.get('original air date'),
                'rating': movie.get('rating'),
                'kind': movie.get('kind'),
                'trailer' : trailer
            }
        
        context = {
            'query': query,
            'film': film,
        }
        return render(request, 'Search.html', context)


class Profile(CreateView):
    form_class=UserProfileForm
    template_name="Profile.html"
    model=UserProfile
    success_url=reverse_lazy("Profile")
    def form_valid(self,form):
        form.instance.user=self.request.user
        self.object = form.save()
        print("saved")
        messages.success(self.request,"Profile Updated")
        return super().form_valid(form)


class ChangePassword(PasswordChangeView):
    template_name = 'ChangePSW.html'
    success_url = reverse_lazy('Profile')    


def Favlist(request,movie_id):
    user = request.user.id
    film = IMDb().get_movie(movie_id)
    if MyFav.objects.filter(movie_id=movie_id,user_id=user):
        messages.warning(request, "Already added to favorites")
    else:
        MyFav.objects.create(movie_id=movie_id,user_id=user)

        messages.success(request, "Added to favorites")

    return redirect('First')

def delfav(request,fid):
    user=request.user
    MyFav.objects.filter(id=fid).delete()
    messages.error(request,"Item Removed form Fav")
    return redirect('MyFav')

def movie_details(imdb_id):
    ia = IMDb()
    movie = ia.get_movie(imdb_id)
    return movie


class MyFavlist(TemplateView):
    template_name='MyFav.html'
    def get(self,request):
        movie_ids = MyFav.objects.filter(user=request.user).values_list('movie_id', flat=True)
        favlist = []

        for ids in movie_ids:
            movie = movie_details(ids)
            poster_url = movie.get('full-size cover url') or movie.get('cover url')

            film = {
                'movie_id' : movie.get('imdbID'),   
                'title': movie.get('title'),
                'year': movie.get('year'),
                'genres': movie.get('genres', []),
                'cast': movie.get('cast', []),
                'plot': movie.get('plot', ),
                'poster_url': poster_url,
                'runtimes' : movie.get('runtimes'),
                'languages': movie.get('languages'),
                'airdate': movie.get('original air date'),
                'rating': movie.get('rating'),
                'kind': movie.get('kind')
            }
            favlist.append(film)
        fid = MyFav.objects.filter(user=request.user)
        combined_list = zip(favlist,fid)
        context = {'combined_list': combined_list}
        # context = {'films':favlist,
        #            'filmid': fid }
        return render (request,'MyFav.html',context)
    

def AddWatchlist(request,movie_id):
    user = request.user.id
    film = IMDb().get_movie(movie_id)
    if Watchlist.objects.filter(movie_id=movie_id,user_id=user):
        messages.warning(request, "Already in Watchlist")
    else:
        Watchlist.objects.create(movie_id=movie_id,user_id=user)

        messages.success(request, "Added to Your Watchlist")

    return redirect('First')

class MyWatchList(TemplateView):
    template_name='Watchlist.html'
    def get(self,request):
        movie_ids = Watchlist.objects.filter(user=request.user).values_list('movie_id', flat=True)
        favlist = []

        for ids in movie_ids:
            movie = movie_details(ids)
            poster_url = movie.get('full-size cover url') or movie.get('cover url')

            film = {
                'movie_id' : movie.get('imdbID'),   
                'title': movie.get('title'),
                'year': movie.get('year'),
                'genres': movie.get('genres', []),
                'cast': movie.get('cast', []),
                'plot': movie.get('plot', ),
                'poster_url': poster_url,
                'runtimes' : movie.get('runtimes'),
                'languages': movie.get('languages'),
                'airdate': movie.get('original air date'),
                'rating': movie.get('rating'),
                'kind': movie.get('kind')
            }
            favlist.append(film)

        fid = Watchlist.objects.filter(user=request.user)
        combined_list = zip(favlist,fid)
        context = {'combined_list': combined_list}
        # context = {'films':favlist,
        #            'filmid': fid }
        return render (request,'Watchlist.html',context)
    
def watched(request,fid):
    user=request.user
    Watchlist.objects.filter(id=fid).delete()
    messages.error(request,"Item Removed form Watchlist")
    return redirect('MyWatchlist')
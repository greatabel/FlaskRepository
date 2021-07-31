from flask import Flask, request
from flask import Blueprint, render_template


# from movie.adapters.memory_repository import load_movies
import movie.adapters.repository as repo
# from movie.domain.model import Director, User, Review, Movie
from movie.domain.model import Director, Review, Movie


# home_blueprint = Blueprint(
#     'home_bp', __name__)


# class PageResult:
    
#     def __init__(self, data, page=1, number=2):
#         self.__dict__ = dict(zip(['data', 'page', 'number'], [data, page, number]))
#         self.full_listing = [self.data[i:i+number] for i in range(0, len(self.data), number)]
#         self.totalpage = len(data)// number
#         print('totalpage=', self.totalpage)


#     def __iter__(self):
#         if self.page - 1 < len(self.full_listing):
#             for i in self.full_listing[self.page-1]:
#                 yield i
#         else:
#             return None

#     def __repr__(self): #used for page linking
#         return "/home/{}".format(self.page+1) #view the next page



# @home_blueprint.route('/home/<int:pagenum>', methods=['GET'])
# @home_blueprint.route('/home', methods=['GET', 'POST'])
# def home(pagenum=1):
#     movie_list = []
#     movie_list = repo.repo_instance.load_movies()
#     # print(movie_list[0], movie_list[0].actors)
#     # movie_list = load_movies()
#     # # 1, and 2
#     # director1 = Director("Joss Whedon")

#     # # 3, 4
#     # director2 = Director("Anthony Russo")

#     # directors = [director1, director2]


#     if request.method == "POST":
#         search_list = []
#         keyword = request.form['keyword']
#         print('keyword=', keyword, '-'*10)
#         if keyword is not None:
#             for movie in movie_list:
#                 if movie.director.director_full_name == keyword:
#                     search_list.append(movie)

#                 for actor in movie.actors:
#                     if actor.actor_full_name == keyword:
#                         search_list.append(movie)
#                         break

#                 for gene in movie.genres:
#                     if gene.genre_name == keyword:
#                         search_list.append(movie)
#                         break
#         print('search_list=' ,search_list, '#'*5)
#         return render_template(
#             'home.html',
#             listing=PageResult(search_list, pagenum, 100),
            
#         )

#     return render_template(
#         'home.html',
#         listing=PageResult(movie_list, pagenum),

        
#     )

# rc_reviews = []
# @home_blueprint.route("/recommend", methods=["GET", "POST"])
# def recommend():
#     import movie.home.recommandation as recommandation
#     choosed = recommandation.main()

#     if request.method == "POST":
        
#         movie_name = request.form['movie_name']
#         movie_id = request.form['movie_id']
#         rtext = request.form['rtext']
#         rating = request.form['rating']

#         movie = Movie(movie_name, 1990, int(movie_id))
#         review = Review(movie, rtext, int(rating))
#         rc_reviews.append(review)


#     return render_template(
#         'recommend.html',
#         choosed=choosed
        
#     )
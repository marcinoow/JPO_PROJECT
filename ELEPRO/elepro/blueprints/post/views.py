from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
    abort)

from elepro.blueprints.post.models import Problem, Comment
from elepro.extensions import db
from elepro.blueprints.post.forms import ProblemForm, CommentForm
from flask_login import login_required, current_user


post = Blueprint('post', __name__, template_folder='templates')


# Funkcja widoku strony glownej aplikacji.
@post.route('/')
@post.route('/home')
def home():
    return render_template('post/home.html')


# Funkcja widoku strony z problemami.
@post.route('/problems')
def problems():
    # Utworzenie obiektu podstrony.
    page = request.args.get('page', 1, type=int)
    # Rodzielenie wszystkich problemow na podstrony.
    problems = Problem.query.order_by(Problem.date_posted.desc()).paginate(page=page,
                    per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    return render_template('post/problems.html', problems=problems)


# Funkcja widoku strony opisujacej dzialanie aplikacji.
@post.route('/about')
def about():
    return render_template('post/about.html')


# Funkcja widoku nowego problemu.
@post.route('/problem/new', methods=['GET', 'POST'])
@login_required
def new_problem():
    # Formularz nowego problemu.
    form = ProblemForm()
    # Jesli formularz jest wypelniony to tworzymy problem.
    if form.validate_on_submit():
        # Obiekt problemu.
        problem = Problem(title=form.title.data, category=form.category.data, content=form.content.data, author=current_user)
        # Zapisanie problemu w bazie danych.
        db.session.add(problem)
        db.session.commit()
        flash(f'Twój problem został opublikowany.', 'success')
        return redirect(url_for('post.home'))
    return render_template("post/create_problem.html", form=form, legend='Mój Problem')


# Funkcja widoku 1 problemu.
@post.route('/problem/<int:problem_id>', methods=['GET', 'POST'])
def problem(problem_id):
    # Formularz komentarza.
    form = CommentForm()
    # Wyszukanie danego problemu.
    problem = Problem.query.get_or_404(problem_id)
    # Jesli formularz jest wypelniony to zapisz komentarz.
    if form.validate_on_submit():
        # Utworzenie obiektu komentarza.
        comment = Comment(body=form.body.data, problem=problem,
                                    author=current_user._get_current_object())
        # Zapis komentarza.
        db.session.add(comment)
        db.session.commit()
        flash('Skomentowałeś problem.', 'success')
        # Przekierowanie na ta sama strone.
        url = request.referrer
        return redirect(url)
    # Podzial komentarzy na kilka podstron.
    page = request.args.get('page', 1, type=int)
    comments = problem.comments.order_by(Comment.timestamp.asc()).paginate(page=page,
                        per_page=4, error_out=False)
    return render_template("post/problem.html", problem=problem, form=form, comments=comments)


# Funkcja widoku usuwania problemu.
@post.route('/problem/<int:problem_id>/delete', methods=['POST'])
@login_required
def delete_problem(problem_id):
    # Wyszukanie problemu po id.
    problem = Problem.query.get_or_404(problem_id)
    # Jesli zalogowany uzytkownik nie jest autorem to zwroc 404.
    if problem.author != current_user:
        abort(403)
    # Usuniecie problemu.
    db.session.delete(problem)
    db.session.commit()
    flash(f'Problem został usunięty.', 'success')
    return redirect(url_for('post.problems'))


# Funkcja widoku aktualizacji problemu.
@post.route('/problem/<int:problem_id>/update', methods=['GET', 'POST'])
@login_required
def update_problem(problem_id):
    # Wyszukanie problemu po id.
    problem = Problem.query.get_or_404(problem_id)
    # Jesli zalogowany uzytkownik nie jest autorem to zwroc 404.
    if problem.author != current_user:
        abort(403)
    # Utworzenie formularza edycji.
    form = ProblemForm()
    # Jesli formularz zostal wypelniony to zaktualizuj problem.
    if form.validate_on_submit():
        problem.title = form.title.data
        problem.category = form.category.data
        problem.content = form.content.data
        db.session.commit()
        flash(f'Twój problem został edytowany.', 'success')
        return redirect(url_for('post.problem', problem_id=problem.id))
    elif request.method == 'GET':
        # Jesli formularz nie zostal wypelniony to zwroc aktualny obiekt problemu.
        form.title.data = problem.title
        form.category.data = problem.category
        form.content.data = problem.content
    return render_template("post/create_problem.html", form=form, legend='Edytuj problem')


# Funkcja widoku usuwania komentarzu.
@post.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    # Wyszukanie komentarzu po id.
    comment = Comment.query.get_or_404(comment_id)
    # Jesli zalogowany uzytkownik nie jest autorem to zwroc 404.
    if comment.author != current_user:
        abort(403)
    # Usuniecie komentarzu.
    db.session.delete(comment)
    db.session.commit()
    # Przekierowanie na ta sama strone.
    url = request.referrer
    flash(f'Komentarz został usunięty.', 'success')
    return redirect(url)

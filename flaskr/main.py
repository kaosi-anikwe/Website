from flaskr import create_app, db
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_user, login_required, logout_user, current_user
from flaskr.models import *


main = Blueprint('main', __name__)

@main.route('/home')
def base():
    # get all courses for current user
    courses = current_user.courses
    courses_info = []

    for course in courses:
        courses_info.append(
            {
                "link": course.link,
                "title": course.title
            }
        )

    return render_template('home.html', courses_info=courses_info)

@main.route("/courses")
def all_courses():
    # get all courses
    courses = Courses.query.all()
    courses_info = []

    for course in courses:
        courses_info.append(
            {
                "link": course.link,
                "title": course.title
            }
        )

    return render_template('courses.html', courses_info=courses_info)

@main.route("/courses/<int:course_id>")
def show_course(course_id):
    # get all info for particular course
    course = Courses.query.get(course_id)
    course_info = []

    course_info.append(
        {
            "link": course.link,
            "title": course.title,
            "category": course.category,
            "summary": course.summary,
            "requirements": course.requirements,
            "duration": course.duration,
            "lectures": course.lectures,
        }
    )

    return render_template("show_course.html", course_info=course_info)

@main.route("/add-course", methods=["GET", "POST"])
def add_course():
    if request.method == "GET":
        return render_template("add_course.html")
    
    data = request.form

    link = data.get("link")
    title = data.get("title")
    category = data.get("category")
    summary = data.get("summary")
    requirements = data.get("requirements")
    duration = data.get("duration")
    lectures = data.get("lectures")
    quizzes = data.get("quizzes")

    try:
        new_course = Courses(
            link = link,
            title = title,
            category = category,
            summary = summary,
            requirements = requirements,
            duration = duration,
            lectures = int(lectures),
            quizzes = int(quizzes)
        )
        new_course.insert()
        message = "Course added successfully"
    except:
        message = "Failed to add course"
    finally:
        flash(message)
        return redirect(url_for("main.add_course"))

@main.route("/edit-user")
def show_users():
    users = Users.query.all()

    return render_template("show_user.html", users=users)

@main.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    user = Users.query.get(user_id)
    if request.method == "GET":
        return render_template("edit_user.html", user=user)
    
    data = request.form
    courses = data.getlist("courses") # list of course ids
     
    try:
        # remove old courses
        get_courses = user.courses
        user_courses = [user_course.course_id for user_course in get_courses]

        for course_id in courses:
            for user_course in user_courses:
                if user_course not in courses:
                    course = Courses.query.get(user_course)
                    user.courses.remove(course)
                    user_courses.pop(user_courses.index(user_course))
        user.update()

        # add new courses
        get_courses = user.courses
        user_courses = [user_course.course_id for user_course in get_courses]

        for course_id in courses:
            for user_course in user_courses:
                if course_id not in user_courses:
                    course = Courses.query.get(course_id)
                    user.courses.append(course)
                    user_courses.append(course_id)
        user.update()
        
        message = "User updated successfully"
    except:
        message = "Failed to update user"
    finally:
        flash(message)
        return redirect(url_for("main.show_users"))

@main.route("/complete/<int:course_id>")
def complete(course_id):
    for course in current_user.courses:
        if course.user_id == current_user.id and course.course_id == course_id:
            if not course.completed:
                course.completed = True
                current_user.update()
                break
    
    return jsonify(
        {
            "success": True
        }
    )
    

from flaskr import create_app, db
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import current_user
from flaskr.models import *


main = Blueprint('main', __name__)

@main.route('/home')
def base():
    # get all courses for current user
    # courses = current_user.courses
    # courses = Enrolled.query.filter(Enrolled.user_id == current_user.id).all()
    courses = Courses.query.join(Enrolled).filter(Enrolled.user_id == current_user.id).filter(Courses.id == Enrolled.course_id).all()
    courses_info = []

    for course in courses:
        courses_info.append(
            {
                "video_id": course.video_id,
                "thumbnail": course.thumbnail,
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
                "video_id": course.video_id,
                "thumbnail": course.thumbnail,
                "title": course.title
            }
        )

    return render_template('courses.html', courses_info=courses_info)

@main.route("/courses/<int:course_id>")
def show_course(course_id):
    # get all info for particular course
    course = Courses.query.get(course_id)
    check_enrolled = Enrolled.query.filter(Enrolled.course_id == course_id, Enrolled.user_id == current_user.id).first()
    enrolled = True if check_enrolled else False

    return render_template("show_course.html", course=course, enrolled=enrolled)

@main.route("/courses/enroll/<int:course_id>")
def enroll(course_id):
    # enroll in a course
    try:
        enrolled = Enrolled()
        course = Courses.query.get(course_id)
        enrolled.course = course
        current_user.courses.append(enrolled)

        return jsonify(
            {
                "success": True
            }
        )
    except:
        return jsonify(
            {
                "success": False
            }
        )

@main.route("/courses/add-course", methods=["GET", "POST"])
def add_course():
    if request.method == "GET":
        return render_template("add_course.html")
    
    data = request.form

    video_id = data.get("video_id")
    title = data.get("title")
    category = data.get("category")
    summary = data.get("summary")
    requirements = data.get("requirements")
    duration = data.get("duration")
    lectures = data.get("lectures")
    quizzes = data.get("quizzes")
    thumbnail = f"https://img.youtube.com/vi/{video_id}/0.jpg"
    
    try:
        new_course = Courses(
            title = title,
            category = category,
            summary = summary,
            requirements = requirements,
            duration = duration,
            lectures = int(lectures),
            quizzes = int(quizzes),
            video_id = video_id,
            thumbnail = thumbnail
        )
        new_course.insert()
        message = "Course added successfully"
    except:
        message = "Failed to add course"
    finally:
        flash(message)
        return redirect(url_for("main.add_course"))


@main.route("/courses/complete/<int:course_id>")
def complete(course_id):
    enrolled_course = Enrolled.query.filter(Enrolled.course_id == course_id, Enrolled.user_id == current_user.id).first()

    try:
        enrolled_course.completed == True
        enrolled_course.update()
#         for course in enrolled_courses:
#             if course.user_id == current_user.id and course.course_id == course_id:
#                 if not course.completed:
#                     course.completed = True
#                     course.percent_complete = 100
#                     current_user.update()
#                     break

        return jsonify(
            {
                "success": True
            }
        )
    except:
        return jsonify(
            {
                "success": False
            }
        )

@main.route("/user/edit-user")
def show_users():
    users = Users.query.all()

    return render_template("show_user.html", users=users)

@main.route("/user/edit-user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    user = Users.query.get(user_id)
    if request.method == "GET":
        return render_template("edit_user.html", user=user)
    
    data = request.form
    courses = data.getlist("courses") # list of course ids
     
    try:
        # remove old courses
        get_courses = Courses.query.join(Enrolled).filter(Enrolled.user_id == current_user.id).filter(Courses.id == Enrolled.course_id).all()

        user_courses = [course.id for course in get_courses]

        for course_id in courses:
            for user_course in user_courses:
                if user_course not in courses:
                    course = Courses.query.get(user_course)
                    user.courses.remove(course)
                    user_courses.pop(user_courses.index(user_course))
        user.update()

        # add new courses
        get_courses = Courses.query.join(Enrolled).filter(Enrolled.user_id == current_user.id).filter(Courses.id == Enrolled.course_id).all()
        user_courses = [course.id for course in get_courses]

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

@main.route("/user/courses/update/<int:course_id>", methods=["GET", "POST"])
def update_course(course_id):
    percent_complete = request.args.get("percent_complete")
    enrolled_course = Enrolled.query.filter(Enrolled.course_id == course_id, Enrolled.user_id == current_user.id).first()
    try:
        enrolled_course.percent_complete = percent_complete
        enrolled_course.update()

        return jsonify(
            {
                "success": True
            }
        )
    except:
        return jsonify(
            {
                "success": False
            }
        )
        
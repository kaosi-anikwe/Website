from flaskr import create_app, db
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
    abort,
)
from flask_login import current_user, login_required
from flaskr.models import *


main = Blueprint("main", __name__)


@main.route("/home")
@login_required
def index():
    # get all courses for current user
    # courses = current_user.courses
    # courses = Enrolled.query.filter(Enrolled.user_id == current_user.id).all()
    courses = []
    enrolled_courses = []
    completed_courses = []

    get_courses = (
        Courses.query.join(Enrolled)
        .filter(Enrolled.user_id == current_user.id)
        .filter(Courses.id == Enrolled.course_id)
        .all()
    )

    for course in get_courses:
        enroll = Enrolled.query.filter(Enrolled.user_id == current_user.id, Enrolled.course_id == course.id).first()
        if not enroll.completed:
            courses.append(
                {
                    "course_id": course.id,
                    "thumbnail": course.thumbnail,
                    "title": course.title,
                    "category": course.category,
                    "percent_complete": enroll.percent_complete
                }
            )
        else:
            completed_courses.append(
                {
                    "course_id": course.id,
                    "thumbnail": course.thumbnail,
                    "title": course.title,
                    "category": course.category,
                }
            )

    return render_template("home.html", courses=courses, completed_courses=completed_courses)


@main.route("/courses")
@login_required
def all_courses():
    # get all courses
    get_courses = Courses.query.all()
    check_enrolled = Enrolled.query.all()
    courses = []

    for course in get_courses:
        enrolled = False
        for enroll in check_enrolled:
            if enroll.user_id == current_user.id and enroll.course_id == course.id:
                enrolled = True
        courses.append(
            {
                "course_id": course.id,
                "title": course.title,
                "category": course.category,
                "summary": course.summary,
                "requirements": course.requirements,
                "duration": course.duration,
                "lectures": course.lectures,
                "quizzes": course.quizzes,
                "thumbnail": course.thumbnail,
                "title": course.title,
                "category": course.category,
                "enrolled": enrolled
            }
        )

    return render_template("courses.html", courses=courses)


@main.route("/courses/<int:course_id>")
@login_required
def show_course(course_id):
    # get all info for particular course
    course = Courses.query.get(course_id)
    enrolled = Enrolled.query.filter(
        Enrolled.course_id == course_id, Enrolled.user_id == current_user.id
    ).first()
    # enrolled = True if check_enrolled else False

    return render_template("show_course.html", course=course, enrolled=enrolled)


@main.route("/courses/enroll/<int:course_id>")
@login_required
def enroll(course_id):
    # enroll in a course
    # try:
    enrolled = Enrolled()
    course = Courses.query.get(course_id)
    enrolled.course = course
    enrolled.user_id = current_user.id
    current_user.courses.append(enrolled)
    current_user.update()

    return jsonify({"success": True})
    # except:
    #     return jsonify({"success": False})


@main.route("/courses/add-course", methods=["GET", "POST"])
@login_required
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
            title=title,
            category=category,
            summary=summary,
            requirements=requirements,
            duration=duration,
            lectures=int(lectures),
            quizzes=int(quizzes),
            video_id=video_id,
            thumbnail=thumbnail,
        )
        new_course.insert()
        message = "Course added successfully"
        return redirect(url_for("main.add_course"))
    except:
        return jsonify({"success": False})



@main.route("/courses/complete/<int:course_id>")
@login_required
def complete(course_id):
    enrolled_course = Enrolled.query.filter(
        Enrolled.course_id == course_id, Enrolled.user_id == current_user.id
    ).first()

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

        return jsonify({"success": True})
    except:
        return jsonify({"success": False})


@main.route("/user/edit-user")
@login_required
def show_users():
    users = Users.query.filter(Users.account == "student").all()
    courses = []
    enrolled = []

    for user in users:
        get_enrolled = []
        get_courses = (
            Courses.query.join(Enrolled)
            .filter(Enrolled.user_id == user.id)
            .filter(Courses.id == Enrolled.course_id)
            .all()
        )
        for course in get_courses:
            enroll = Enrolled.query.filter(Enrolled.user_id == user.id, Enrolled.course_id == course.id).one_or_none()
            get_enrolled.append(enroll) if enroll else get_enrolled.append(None)
        courses.append(get_courses)
        enrolled.append(get_enrolled)


    return render_template("show_user.html", users=users, courses=courses, enrolled=enrolled)


@main.route("/user/edit-user/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = Users.query.get(user_id)
    if request.method == "GET":
        enrolled = []
        courses = Courses.query.all()

        for course in courses:
            enroll = Enrolled.query.filter(Enrolled.user_id == user.id, Enrolled.course_id == course.id).one_or_none()
            enrolled.append(enroll) if enroll else enrolled.append(None)

        return render_template("edit_user.html", user=user, courses=courses, enrolled=enrolled)

    data = request.form
    courses = data.getlist("courses")  # list of course ids
    courses = [int(course) for course in courses]
    temp_list = []
    get_courses = (
        Courses.query.join(Enrolled)
        .filter(Enrolled.user_id == user_id)
        .filter(Courses.id == Enrolled.course_id)
        .all()
    )
    try:
        user_courses = [course.id for course in get_courses]

        # remove old courses
        for course_id in user_courses:
            if course_id not in courses:
                course = Courses.query.get(course_id)
                enrolled = Enrolled.query.filter(Enrolled.course_id == course_id, Enrolled.user_id == user_id).one()
                user.courses.remove(enrolled)
                enrolled.delete()
            else:
                temp_list.append(course_id)

        # add new courses
        for course_id in courses:
            if course_id not in temp_list:
                enrolled = Enrolled()
                course = Courses.query.get(course_id)
                enrolled.course = course
                enrolled.course_id = course_id
                enrolled.user_id = user_id
                user.courses.append(enrolled)
                enrolled.insert()

        return redirect(url_for("main.show_users"))
    except:
        return "failed"



@main.route("/user/courses/update/<int:course_id>", methods=["GET", "POST"])
@login_required
def update_course(course_id):
    percent_complete = int(request.args.get("percent_complete"))
    enrolled_course = Enrolled.query.filter(
        Enrolled.course_id == course_id, Enrolled.user_id == current_user.id
    ).first()
    try:
        if percent_complete == 100:
            enrolled_course.completed = True        
        if percent_complete > enrolled_course.percent_complete:
            enrolled_course.percent_complete = percent_complete
        enrolled_course.update()

        return jsonify({"success": True})
    except:
        return jsonify({"success": False})
        
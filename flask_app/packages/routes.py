from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import package_client
from ..forms import PackageReviewForm, SearchForm, PackageReportBugForm
from ..models import User, Review, BugReport
from ..utils import current_time

packages = Blueprint('packages', __name__, static_folder='static', template_folder='templates')


""" ************ View functions ************ """


@packages.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("packages.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)

@packages.route("/all_packages", methods=["GET", "POST"])
def all_packages():
    return render_template("all_packages.html", all_package_info= zip(package_client.all_package_names, package_client.all_package_descriptions))


@packages.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = package_client.search(query)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("packages.index"))

    return render_template("query.html", query=query, results=results)


@packages.route("/packages/<package_name>", methods=["GET", "POST"])
def package_detail(package_name):
    try:
        result = package_client.retrieve_package_by_name(package_name)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    review_form = PackageReviewForm()
    if review_form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=review_form.text.data,
            date=current_time(),
            package_name=package_name
        )
        review.save()

        return redirect(request.path)

    bug_form = PackageReportBugForm()
    if bug_form.validate_on_submit() and current_user.is_authenticated:
        bug = BugReport(
            commenter=current_user._get_current_object(),
            content=bug_form.text_bug.data,
            date=current_time(),
            package_name=package_name
        )
        bug.save()

        return redirect(request.path)

    reviews = Review.objects(package_name=package_name)
    bug_reports = BugReport.objects(package_name=package_name)
    # reviews = []
    # bug_reports = []

    return render_template(
        "package_detail.html", review_form=review_form, bug_form=bug_form,
        package=result, reviews=reviews, bug_reports=bug_reports
    )

@packages.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)
    bug_reports = BugReport.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews, bug_reports=bug_reports)


# @packages.route("/test")
# def test():
#     return render_template("test.html")
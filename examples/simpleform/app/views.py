from flask import flash, render_template
from flask_appbuilder import SimpleFormView
from flask_babel import lazy_gettext as _

from . import appbuilder, db
from .forms import MyForm
import requests


class MyFormView(SimpleFormView):
    form = MyForm
    form_title = "This is my first form view"
    message = "My form was submitted"

    def form_get(self, form):
        form.field1.data = "This was prefilled"
        api_url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
        payload = {}
        response = requests.request("GET", api_url, data=payload, verify=False)
        if response.status_code == 200:
            data = str(response.json()['Results'][0]["Make_ID"])
            # Pre-fill the form with data from the API
            form.field1.data = data
        else:
            flash('Failed to retrieve data from the API', 'danger')
    def form_post(self, form):
        # post process form
        flash(self.message, "info")


appbuilder.add_view(
    MyFormView,
    "My form View",
    icon="fa-group",
    label=_("My form View"),
    category="My Forms",
    category_icon="fa-cogs",
)

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()

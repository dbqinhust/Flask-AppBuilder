from flask import flash, render_template, redirect, url_for
from flask_appbuilder import SimpleFormView, BaseView, expose
from flask_babel import lazy_gettext as _
from flask_appbuilder.security.decorators import has_access

from . import appbuilder, db
from .forms import MyForm, ItemForm
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


class CustomView(BaseView):
    default_view = 'display_items'

    @expose('/form', methods=['GET', 'POST'])
    @has_access
    def display_form(self):
        form = ItemForm()
        if form.validate_on_submit():
            # Process the form data here
            name = form.name.data
            description = form.description.data

            # You could store the data in a list, send it to an API, etc.
            # Example: items.append({'name': name, 'description': description})

            flash(f'Item {name} added successfully!', 'success')
            return redirect(url_for('CustomView.display_form'))

        return self.render_template('form.html', form=form)

    @expose('/items')
    @has_access
    def display_items(self):
        # Example list of items
        items = [
            {'name': 'Item 1', 'description': 'Description 1'},
            {'name': 'Item 2', 'description': 'Description 2'},
        ]
        return self.render_template('items.html', items=items)


appbuilder.add_view(
    CustomView,
    "My item View",
    icon="fa-group",
    label=_("My item View"),
    category="My Forms",
    category_icon="fa-cogs",
)
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

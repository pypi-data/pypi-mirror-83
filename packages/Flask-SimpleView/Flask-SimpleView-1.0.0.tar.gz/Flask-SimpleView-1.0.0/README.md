# Very simple wrapper around Flask

## Install
```
pip install flask_simpleview
```

## Use
An example for a simple view:
```
from flask_simpleview import Flask, SimpleView

# this works exactly the same as flask.Flask
# flask_simpleview.Flask is subclassed from flask.Flask
# the only difference is the addition of 2 methods: `add_view` and `add_api`
app = Flask(__name__)

# and the same blurb again:
# this works exactly the same as flask.Blueprint
# flask_simpleview.Blueprint is subclassed from flask.Blueprint
# the only difference is the addition of 2 methods: `add_view` and `add_api`
blueprint = Blueprint('blueprint', __name__)

# as Flask and Blueprint are the same as their parent classes
# this will obviously work
app.register_blueprint(blueprint)

# This works exactly the same as flask.views.MethodView
# flask_simpleview.SimpleView is subclassed from flask.views.MethodView
# the only difference is that you encapsulate the rule (route) and 
# the endpoint in the class
class SignUp(SimpleView):
    rule = '/sign-up'
    endpoint = 'sign_up'
    template = 'sign_up.html'

    def get(self):
        # just assuming a form for the demonstration
        form = SignUpForm()
        # you don't need to pass the template string, if registered above
        return self.render_template(form=form)

    def post(self):
        form = SignUpForm(request.form)
        if form.validate_on_submit():
            sign_up_user_from_form(form)
            # the SimpleView class has access to all flask functions
            # `return self.thing` is the same as `return getattr(flask, 'thing')`
            return self.redirect(self.url_for('login'))
        else:
            return self.render_template(form=form)

app.add_view(SignUp)
blueprint.add_view(SignUp)
```

With a blueprint:
```
from flask_simpleview import Blueprint, Login

auth = Blueprint('auth', __name__)

class Login(SimpleView):
    rule = '/login'
    endpoint = 'login'
    template = 'login.html'

    def get(self):
        return self.render_template()

    def post(self):
        try:
            login_user(request.form)
            return self.redirect(self.url_for('app.dashboard'))
        except LoginFailed as e:
            return self.render_template(errors=e)

auth.add_view(Login)
```

Or if you want to specify the template in `self.render_template`:
```
class SignUp(SimpleView):
    rule = '/sign-up'
    endpoint = 'sign_up'

    def get(self):
        return self.render_template('sign_up.html')
```

No need for views just to have templates:
```
class LegacyDashboardRedirect(SimpleView):
    rule = '/dashboard/v1/home'
    endpoint = 'v1_dashboard'

    def get(self):
        return self.redirect(self.url_for('v2_dashboard'))
```

Or for apis:
```
class UsersAPI(SimpleView):
    rule = '/api/users'
    endpoint = 'users'
    
    def get(self):
        user_id = request.args.get('id')
        if user_id:
            return self.jsonify(db.session.query(User).get(user_id).to_json())
        else:
            return self.jsonify([u.to_json() for u in db.session.query(User)]
```

You don't have to use `self` either, you can use flask of course:
```
from flask import redirect

class AnotherView(SimpleView):
    rule = '/another-view'
    endpoint = 'another_view'
    
    def get(self):
        return redirect('https://www.example.com')
```



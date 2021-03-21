from flask import Flask, make_response,render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
#app.config['SECRETE_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)

#forms entry point
#class NameForm(Form):
    # name = StringField('What is your name?', validators = [Required])
    # submit = SubmitField('Submit')
#rendering templates

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = Form()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
            
    return render_template('index.html', form=form, name=name)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

#error handling route page not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#internal error handling
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



if __name__ == "__main__":
    app.run(debug=True)
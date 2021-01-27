from notes_app import app, db 
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import current_user, login_user, login_required, logout_user
from notes_app.models import User, Note 
from notes_app.forms import LoginForm, RegistrationForm, NotesForm, UpdateProfile



# Setting up views (routes)
@app.route('/')
def home():
    return render_template('home.html')




@app.route('/notes_app', methods=['GET', 'POST'])
@login_required
def notes_app():

    prototype = db.session.query(Note.id, Note.title, Note.text, Note.date).filter_by(user_id=current_user.id).all()


    form = NotesForm()

    if form.validate_on_submit():
        # link note to a particular user id. done.
        note = Note(title=form.title.data,
        text=form.text.data, user_id=current_user.id)

        db.session.add(note)
        db.session.commit()

        flash('Note created!')

        form.text.data = ''
        form.title.data = ''


        submitted_notes = Note.query.all()
        
        data_notes = Note.query.filter_by(user_id=current_user.id).all()
        print('submitted by the user: ', data_notes)

        filtered = db.session.query(Note.text).filter_by(user_id=current_user.id).all()
        print('Text only: ', filtered)


        # grab the specific bits of the whole data
        prototype = db.session.query(Note.id, Note.title, Note.text, Note.date).filter_by(user_id=current_user.id).all()
        print('This is prototype', prototype)

        some_test = db.session.query(Note.id).filter_by(user_id=current_user.id).all()
        print(some_test)


        return render_template('notes_app.html', form=form, test_display=prototype)


    return render_template('notes_app.html', form=form, test_display=prototype)


# user is going to click on a button link with the id
@login_required
@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Note.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/notes_app')
    except:
        return 'There was a problem deleting that note...'
    



@login_required
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    form = NotesForm()

    note_to_update = Note.query.get_or_404(id)

    if note_to_update.author != current_user:
        abort(403)

    

    # if form.validate_on_submit()

    if request.method == 'POST':
        # grabbing data from the uesr submitted form
        # (where name='text')
        # {{form.title}} {{form.text}}

        note_to_update.title = request.form['title']
        note_to_update.text = request.form['text']

        # note_to_update.title = form.title.data
        # note_to_update.text = form.text.data

        try:
            #that's it!
            db.session.commit()
            return redirect('/notes_app')
        except:
            return "There was a problem updating that note..."

    else:
        return render_template('update_note.html', form=form, note_to_update=note_to_update)


    



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    # giving the user the option to update their info.
    form = UpdateProfile()

    if form.validate_on_submit():

        # whether it's the username and/or email
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash("User account updated!")

    elif request.method == 'GET':
        # not submitting anything, just grabbing their 
        # current username and current email
        form.username.data = current_user.username 
        form.email.data = current_user.email 
    return render_template('update_profile.html', form=form)





@app.route('/logout')
@login_required
def logout():
    # calling imported function
    logout_user()
    flash('you logged out')
    return redirect(url_for('home'))




@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # in models, there's a method..
        # verifying the password is correct and that the user exists
        # python compiler moves from left to right. Which means
        # it first checks the first condition and if it's true, it moves to the second one, and so on.
        if user is not None and user.check_password(form.password.data):
            # imported function
            login_user(user)
            flash('logged in successfully')

            # if a user was trying to visit a page that requires a login
            # flask saves that URL as "next"
            next = request.args.get('next')

            # if next exists, otherwise go to welcome page.
            if next == None or not next[0] == '/':
                next = url_for('notes_app')

            return redirect(next)
        
    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
        username=form.username.data,
        password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("thanks for registration!")

        return redirect(url_for('login'))
    return render_template('register.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)





























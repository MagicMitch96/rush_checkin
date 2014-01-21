from flask import flash, redirect, render_template, request, Response, url_for

from app import app, db, basic_auth, basedir, LOG
from models import Rushee
from forms import RusheeForm

import os

def flash_errors(form):
    for field, errors in form.errors.items():
        for err in errors:
            flash("Please fill out %s" % getattr(form, field).label.text)

@app.route('/', methods=['GET', 'POST'])
def add():
    form = RusheeForm()
    if form.validate_on_submit():
        LOG.info(form.pic.data)
        rushee = Rushee(form.name.data, form.computing_id.data,
                        form.year.data, form.dorm.data,
                        form.pic.data)
        db.session.add(rushee)
        db.session.commit()

        flash('Thanks for checking in')
        LOG.info("Successfully logged: %s (%s)" % 
                 (form.name.data, form.computing_id.data))

        return redirect(url_for('add'))
    else:
        flash_errors(form)
    return render_template('add.html', form=form)

@app.route('/admin')
@app.route('/admin/<date>')
@basic_auth.required
def show_data(date=False):
    total_count = Rushee.query.count()
    if date:
        rushees = Rushee.query.filter(Rushee.event == date). \
                filter(Rushee.decided == 0)
    else:
        rushees = Rushee.query.filter(Rushee.decided == 0)

    decide_count = len(list(rushees))
    return render_template('admin.html', rushees=rushees, total_count=total_count,
                           decide_count=decide_count)

@app.route('/decision/<rushee>/<decision_type>')
def decision(rushee, decision_type):
    rushee = Rushee.query.filter(Rushee.id == rushee)[0]
    rushee.decided = decision_type
    db.session.commit()

    LOG.info("Wrote %s to %s list" % (rushee.name, decision_type))
    flash('Successfully added %s to %s list' % (rushee.name, decision_type))

    return redirect(request.referrer)

@app.route('/download/<list_type>')
def download_list(list_type):
    rushee = Rushee.query.filter(Rushee.decided == list_type)
    the_list = str("NAME,COMPUTING,YEAR,DORM<br/>")
    for r in rushee:
        the_list += str("%s,%s,%s,%s<br/>" % (r.name, r.computing_id, r.year, r.dorm))

    return Response("%r" % the_list, mimetype='text/html')

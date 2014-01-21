from flask import flash, redirect, render_template, request, url_for

from app import app, db, basic_auth, basedir, LOG
from models import Rushee
from forms import RusheeForm

import os

@app.route('/', methods=['GET', 'POST'])
def add():
    form = RusheeForm()
    if form.validate_on_submit():
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
    rushee.decided = 1
    db.session.commit()

    filename = os.path.join(basedir, "static/lists/%s.tsv" % decision_type)
    with open(filename, "a+b") as rushee_list:
        rushee_list.write("%r\t%r\t%r\t%r\n" % (str(rushee.name),
                                              str(rushee.computing_id),
                                              str(rushee.year),
                                              str(rushee.dorm)))
        LOG.info("Wrote %s to %s list" % (rushee.name, decision_type))
    flash('Successfully added %s to %s list' % (rushee.name, decision_type))
    return redirect(request.referrer)

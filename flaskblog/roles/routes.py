from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Role
from flaskblog.roles.forms import RoleForm

roles = Blueprint('roles',__name__)


@roles.route("/role/new", methods=['GET', 'POST'])
@login_required
def new_role():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(rolename=form.rolename.data, description=form.description.data, authorrole=current_user)
        db.session.add(role)
        db.session.commit()
        flash('Your Role has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('roles/create_role.html', title='New Role',
                           form=form, legend='New Role')

@roles.route("/roles", methods=['GET', 'POST'])
@login_required
def all_role():
    roles = Role.query.all()
    return render_template('roles/all_role.html', roles=roles)

@roles.route("/role/<int:role_id>")
def role(role_id):
    role = Role.query.get_or_404(role_id)
    return render_template('roles/role.html', title=role.rolename, role=role)


@roles.route("/role/<int:role_id>/update", methods=['GET', 'POST'])
@login_required
def update_role(role_id):
    role = Role.query.get_or_404(role_id)
    if role.authorrole != current_user:
        abort(403)
    form = RoleForm()
    if form.validate_on_submit():
        role.rolename = form.rolename.data
        db.session.commit()
        flash('Your Role has been updated!', 'success')
        return redirect(url_for('roles.role', role_id=role.id))
    elif request.method == 'GET':
        form.rolename.data = role.rolename
    return render_template('roles/create_role.html', title='Update Role',
                           form=form, legend='Update Role')


@roles.route("/role/<int:role_id>/delete", methods=['POST'])
@login_required
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)
    if role.author != current_user:
        abort(403)
    db.session.delete(role)
    db.session.commit()
    flash('Your Role has been deleted!', 'success')
    return redirect(url_for('main.home'))

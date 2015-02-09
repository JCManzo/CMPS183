# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index requires the user to be logged in in order to display notes.
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
@auth.requires_login()
def index():
    """
    list notes (after authenticating user)
    """
    notes = db(db.note.user_id==auth.user.id) \
                .select(db.note.body, db.note.id,\
                 orderby=~db.note.last_opened)

    message = 'Hello %(first_name)s,' % auth.user + ' you have ' \
                    + str(len(notes)) + ' note(s).'
    return dict(notes=notes, message=message)

@auth.requires_login()
def read():
    """
    display the note with the selected id if it exists.
    """
    n = request.args(0) or redirect(URL('index'))
    record = db((db.note.id==int(n)) & (db.note.user_id==auth.user.id))
    if record.isempty():
        result = 'Note with id ' + str(n) + ' does not exist.'
    else:
        row = record.select().first()
        row.update_record(last_opened=request.now)
        result=DIV(P(row.body, _class='reading_note', _id=row.id), _id='opened_note')
    return dict(result=result, parameter=str(n))


@auth.requires_login()
def delete():
    """
    deletes note with selected id upon confirmation
    """
    n = request.args(0) or redirect(URL('index'))

    record = db((db.note.id==int(n)) & (db.note.user_id==auth.user.id))
    if record.isempty():
        message = 'Note with id ' + str(n) + ' does not exist.'
    else:
        row = record.select().first()
        result=DIV(P(row.body, _class='reading_note'), _id='opened_note')
        form = FORM('', INPUT(_type='submit',_value='YES', _id='del_submit'))
        if form.process().accepted:
            record.delete()
            redirect(URL('index'))

    return dict(result=result,form=form)
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@auth.requires_login()
def add():
    response.flash=T("Note added")
    form = FORM(
               TEXTAREA(_name='body', requires=IS_NOT_EMPTY(), _id='add_body', _placeholder='Write something...'),
               INPUT(_type='submit', _class='sub_button'),
               _id='note_form')
    if form.process().accepted:
        session.visitor_name = form.vars.visitor_name
        mBody  = request.vars.body
        noteID = db.note.insert(user_id=auth.user.id, body=mBody)
        redirect(URL('index'))
    return dict(form=form)

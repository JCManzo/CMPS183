# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    form = SQLFORM(db.line_item)

    if form.process().accepted:
        response.flash = 'Order accepted'
    elif form.errors:
        response.flash = 'Order has errors'

    result = db(db.line_item.id>0)
    sum = db.line_item.item_total.sum()
    summation = 'Your total cost so far is $' + str(db().select(sum).first()[sum])
    if result.isempty():
        result = 'Your cart is empty.'
    else:
        result = db(db.line_item.id>0).select(db.line_item.ALL)

    message = 'Hello %(first_name)s. ' % auth.user

    return dict(message=message, result=result, form=form, summation=summation)


def get_item_price():
    option = request.vars.what
    items = db(db.products.name==option).select(db.products.ALL)

    item_price = 0
    for item in items:
        item_price = item.price
    return "$('#line_item_item_price').val('%s');" % item_price

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


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


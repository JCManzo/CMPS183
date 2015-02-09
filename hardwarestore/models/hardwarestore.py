# Juan C. Manzo
# CS183
# Homework 2


# The name of the product is the record representation
db.define_table('products',
                    Field('name', 'string'),
                    Field('on_hand','integer'),
                    Field('price', 'double'),
                    Field('on_order','integer'),
                    format='%(name)s')

# Validates:
#    - email: email field must be a valid field or empty
#    - phone: phone number must be a vaid 10 digit number
#         •  number must include a space/dash
#
# The name of the contact is the record representation
db.define_table('contact',
                    Field('name', 'string'),
                    Field('phone', 'string', requires=IS_EMPTY_OR(IS_MATCH('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$', error_message='Phone number must be a 10 digit number'))),
                    Field('email', 'string', requires=IS_EMPTY_OR(IS_EMAIL())),
                    Field('note', 'string'),
                    format='%(name)s')

# A supplier table references the contacts table
db.define_table('supplier',
                    Field('name','string'),
                    Field('address', 'string'),
                    Field('contacts', 'list:reference contact'),
                    format='%(name)s')

# Compute adds ups the total price of the purchase.
# The purchase 'id' is the record representation for this table.
# Price of each is stored as a list of strings because list:double
# is not possible.
db.define_table('purchase',
                    Field('purchase_date', 'datetime', default=request.now),
                    Field('items_bought', 'list:reference products'),
                    Field('price_of_each', 'list:string'),
                    Field('quantity_of_each', 'list:integer'),
                    Field('total_price',
                         compute=lambda x: sum([float(a)*float(b) for a, b in zip(x['quantity_of_each'], x['price_of_each'])])),
                    redefine=True,
                    format='%(id)s')

# A customer can refer to their purchase by the date it was made on.
# Validates:
#    - email: email field must be a valid field or empty
#    - phone: phone number must be a vaid 10 digit number
#         •  number must include a space/dash
db.define_table('customer',
                    Field('name', 'string'),
                    Field('phone', 'string', requires=IS_EMPTY_OR(IS_MATCH('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$', error_message='Phone number must be a 10 digit number'))),
                    Field('email', 'string', requires=IS_EMPTY_OR(IS_EMAIL())),
                    Field('purchases', 'list:reference purchase'),
                    format='%(name)s')

db.define_table('line_item',
                    Field('item_name', 'reference products'),
                    Field('item_count', 'integer', requires=IS_NOT_EMPTY()),
                    Field('item_price', 'double'),
                    Field('item_total',
                              compute=lambda x: x['item_count'] * x['item_price']))
## Controller Script Python "validate_sendto"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=send_to_address='',send_from_address=''
##title=validates the email adresses

from Products.CMFPlone import PloneMessageFactory as _
plone_utils=context.plone_utils

if not send_to_address:
    state.setError('send_to_address',
                   _(u'Please submit an email address.'),
                   'email_required')

if not plone_utils.validateEmailAddresses(send_to_address):
    state.setError('send_to_address',
                   _(u'Please submit a valid email address.'),
                   'email_required')

if not send_from_address:
    state.setError('send_from_address',
                   _(u'Please submit an email address.'),
                   'email_required')

if not plone_utils.validateSingleEmailAddress(send_from_address):
    state.setError('send_from_address',
                   _(u'Please submit a valid email address.'),
                   'email_required')

captcha = context.REQUEST.get('captcha')
captcha_result = context.restrictedTraverse('@@captcha').verify(captcha)

if not captcha_result:
    state.setError('captcha',
                   context.utranslate(u'Please provide the message here above correctly, case sensitive.',
                                      domain='communesplone.layout', )
                   )
    state.set(status='failure')

if state.getErrors():
    context.plone_utils.addPortalMessage(
        _(u'Please correct the indicated errors.'), 'error')
    return state.set(status='failure')
else:
    return state

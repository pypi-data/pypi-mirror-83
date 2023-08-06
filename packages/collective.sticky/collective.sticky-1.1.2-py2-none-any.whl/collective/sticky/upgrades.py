# -*- coding: utf-8 -*-


def upgrade_to_two(context):
    context.runImportStepFromProfile('profile-collective.sticky:default',
                                     'plone.app.registry')

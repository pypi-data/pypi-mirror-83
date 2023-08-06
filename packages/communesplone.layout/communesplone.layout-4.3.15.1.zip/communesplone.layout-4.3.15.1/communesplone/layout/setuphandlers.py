# -*- coding: utf-8 -*-


def setupVarious(context):

    if context.readDataFile('communesplone.layout_various.txt') is None:
        return


def simplify(context):
    """
        Layout simplification
    """
    if context.readDataFile('communesplone.layout_simplify.txt') is None:
        return

    site = context.getSite()

    # Add a full-layout group
    groups_tool = site.portal_groups
    group_id = "full-layout"
    if not group_id in groups_tool.getGroupIds():
        groups_tool.addGroup(group_id, title='Full edition layout')
        groups_tool.addPrincipalToGroup('Administrators', "full-layout")
        groups_tool.addPrincipalToGroup('Site Administrators', "full-layout")

    # Clean user interface
    site.manage_permission('Sharing page: Delegate roles', ('Manager', 'Site Administrator', ), acquire=0)
    site.manage_permission('Modify view template', ('Manager', 'Site Administrator', ), acquire=0)
    site.manage_permission('Review portal content', ('Manager', 'Site Administrator', 'Reviewer'), acquire=0)
    site.manage_permission('Modify constrain types', ('Manager', 'Site Administrator', ), acquire=0)
    site.manage_permission('CMFPlacefulWorkflow: Manage workflow policies', ('Manager', 'Site Administrator', ),
                           acquire=0)

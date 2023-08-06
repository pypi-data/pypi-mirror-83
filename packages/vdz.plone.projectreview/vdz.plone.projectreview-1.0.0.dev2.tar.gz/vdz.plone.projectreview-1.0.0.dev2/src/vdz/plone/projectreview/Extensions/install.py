from Products.CMFCore.utils import getToolByName

def uninstall(portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')
    if not reinstall:
        setup_tool.runAllImportStepsFromProfile('profile-vdz.plone.projectreview:uninstall')
        return "Uninstalled vdz.plone.projectreview"

    setup_tool.runAllImportStepsFromProfile('profile-vdz.plone.projectreview:default')
    return "Reinstalled vdz.plone.projectreview"

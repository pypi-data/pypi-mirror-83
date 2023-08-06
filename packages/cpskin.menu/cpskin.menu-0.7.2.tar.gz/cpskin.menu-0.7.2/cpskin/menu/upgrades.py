PROFILE_ID = 'profile-cpskin.menu:default'


def upgrade_1000_to_1001(context):
    context.runImportStepFromProfile(PROFILE_ID, 'cssregistry')


def upgrade_1001_to_1002(context):
    context.runImportStepFromProfile(PROFILE_ID, 'jsregistry')


def upgrade_1002_to_1003(context):
    context.runImportStepFromProfile(PROFILE_ID, 'jsregistry')


def move_cpskin_actions(context):
    context.runImportStepFromProfile('profile-cpskin.menu:to1005', 'actions')
    context.runImportStepFromProfile('profile-cpskin.menu:default', 'actions')

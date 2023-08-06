# ============================================================================
# ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s cpskin.menu -t test_banner.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path cpskin cpskin.menu.testing.CPSKIN_MENU_ROBOT_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot cpskin/menu/tests/robot/test_direct_access.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================
*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Variables ***


*** Test cases ***


Test direct access visibility
    Click LOISIRS menu

    Click Element  css=ul.navTreeLevel0 a#loisirs-art_et_culture

    # Direct access visible
    Element Should Be Visible  css=ul.direct_access a#loisirs-art_et_culture-artistes-abba
    Element Should Be Visible  css=ul.direct_access a#loisirs-art_et_culture-artistes-rockers-john_lennon

    # Direct access non visible from another folder
    Element Should Not Be Visible  css=ul.direct_access a#loisirs-tourisme-promenades

Test direct access link
    Click LOISIRS menu

    Click Element  css=ul.navTreeLevel0 a#loisirs-art_et_culture

    Click Element       css=ul.direct_access a#loisirs-art_et_culture-artistes-rockers-john_lennon
    Location Should Be  ${PLONE_URL}/loisirs/art_et_culture/artistes/rockers/john_lennon


*** Keywords ***


Click LOISIRS menu
    Element Should Be Visible  css=li#portaltab-loisirs a
    Click Element              css=li#portaltab-loisirs a
    Location Should Be         ${PLONE_URL}

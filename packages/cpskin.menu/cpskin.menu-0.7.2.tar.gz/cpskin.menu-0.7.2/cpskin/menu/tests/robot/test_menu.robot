# ============================================================================
# ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s cpskin.menu -t test_menu.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path cpskin cpskin.menu.testing.CPSKIN_MENU_ROBOT_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot [-i current] cpskin/menu/tests/robot/test_menu.robot
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


*** Test Cases ***


Test menu
    Click LOISIRS Menu
    Element Should Be Visible  css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Click Element              css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Element Should Be Visible  css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Click Element              css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Element Should Be Visible  css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Click Element              css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata

    Wait Until Page Contains Element  xpath=//h1[contains(text(),'Tata')]
    Location Should Be                ${PLONE_URL}/loisirs/art_et_culture/artistes/tata

Test loading with 3 levels
    Click LOISIRS Menu

    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Is Homepage
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-bibliotheques
    Location Should Be  ${PLONE_URL}/loisirs/art_et_culture/bibliotheques

Test loading with 4 levels
    Click LOISIRS Menu

    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Is Homepage
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Is Homepage
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Location Should Be  ${PLONE_URL}/loisirs/art_et_culture/artistes/tata

Test begin on other page than root
    Go To  ${PLONE_URL}/commune/services_communaux/finances

    Element Should Be Visible  css=li#portaltab-loisirs a
    Click Element              css=li#portaltab-loisirs a
    Location Should Be  ${PLONE_URL}/commune/services_communaux/finances

    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Should Be  ${PLONE_URL}/commune/services_communaux/finances
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Should Be  ${PLONE_URL}/commune/services_communaux/finances
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Location Should Be  ${PLONE_URL}/loisirs/art_et_culture/artistes/tata

Test keyboard navigation
    Click LOISIRS Menu

    Focus                      css=a#loisirs-art_et_culture
    Element Should Be Visible  css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Focus                      css=a#loisirs-art_et_culture-artistes
    Element Should Be Visible  css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Click Element              css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-tata
    Location Should Be         ${PLONE_URL}/loisirs/art_et_culture/artistes/tata


Test level 5 not in menu
    Click LOISIRS Menu

    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Is Homepage
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Is Homepage
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-rockers
    Location Should Be  ${PLONE_URL}/loisirs/art_et_culture/artistes/rockers

Test fourth level navigation folder not working in wrong place
    Click LOISIRS Menu

    Click Element       css=ul.navTreeLevel0 a#loisirs-art_et_culture
    Location Is Homepage
    Click Element       css=ul.navTreeLevel1 a#loisirs-art_et_culture-artistes
    Location Is Homepage
    Click Element       css=ul.navTreeLevel2 a#loisirs-art_et_culture-artistes-cinema
    # Menu not deployed
    Location Should Be  ${PLONE_URL}/loisirs/art_et_culture/artistes/cinema

    Page Should Contain  Kinepolis

Test menu visible when location is subfolder
    [Tags]  current
    Go To  ${PLONE_URL}/loisirs/art_et_culture
    Element Should Not Be Visible  css=ul.navTreeLevel0 a#loisirs-art_et_culture


*** Keywords ***

Location Is Homepage
    Location Should Be  ${PLONE_URL}


Click LOISIRS Menu
    Element Should Be Visible  css=li#portaltab-loisirs a
    Click Element              css=li#portaltab-loisirs a
    Location Is Homepage

*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


*** Test cases ***

Test enabling / disabling banner on Plone site and sub folder
    Log in as site owner
    Go to  ${PLONE_URL}

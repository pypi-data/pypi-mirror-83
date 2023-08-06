*** Settings ***
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Suite Setup
Suite Teardown  Close all browsers


*** Test Cases ***
Site Administrator can view ckeditor
    Go to homepage
    Page should contain  imio.ckeditortemplates
    Open add new menu
    Click Link  id=document
    Page Should Contain Element  cke_1_contents


*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Site Administrator

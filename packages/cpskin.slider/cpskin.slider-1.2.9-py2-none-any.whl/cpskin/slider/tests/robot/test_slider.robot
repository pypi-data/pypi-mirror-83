# bin/robot-server --reload-path cpskin cpskin.slider.testing.CPSKIN_SLIDER_ROBOT_TESTING
# bin/robot cpskin/slider/tests/robot/test_slider.robot
*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Suite setup  Set Selenium speed  1s

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers

*** Variables ***


*** Test cases ***

Test News Item exists
    Enable autologin as  Site Administrator
    Click link  css=#portaltab-slider-folder a
    Element Should Contain  css=div#slider-slidercollection ul.slides li.flex-active-slide div h2 a  Foire aux boudins
    Click Element  css=div#carousel-slidercollection ul.slides li:nth-child(2)
    Element Text Should Be  css=div#slider-slidercollection ul.slides li.flex-active-slide div h2 a  Festival de danse folklorique

Test Slider and Carousel
    Enable autologin as  Site Administrator
    Click link  css=#portaltab-slider-folder a
    Page Should Not Contain Element  css=div#slider-slidercollection ul.slides li:nth-child(3).flex-active-slide
    Click Element  css=div#carousel-slidercollection ul.slides li:nth-child(2)
    Page Should Contain Element  css=div#slider-slidercollection ul.slides li:nth-child(3).flex-active-slide

# Test Url Carousel
#     Enable autologin as  Site Administrator
#     Click link  css=#portaltab-slider-folder a
#     Page Should Not Contain Element  css=div#slider-slidercollection ul.slides li:nth-child(3).flex-active-slide
#     Click link  Festival de danse folklorique
#     Location Should Be  ${PLONE_URL}/slider-folder/2-festival-de-danse-folklorique


*** Keywords ***

Logged as owner
    Log in as site owner

# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.printrss -t test_rss_feed.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.printrss.testing.COLLECTIVE_PRINTRSS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/printrss/tests/robot/test_rss_feed.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Variables ***
# ${BROWSER} =  GoogleChrome

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a rss_feed
  Given a logged-in site administrator
    and an add rss_feed form
   When I type 'Test Linux feed' into the title field
    and I type 'http://www.linux.com/feeds/all-content' into the url field
    and I submit the form
   Then a rss_feed with the title 'Test Linux feed' has been created

Scenario: As a site administrator I can view a rss_feed
  Given a logged-in site administrator
    and a rss_feed 'Test Linux feed'
   When I go to the rss_feed view
   Then I can see the rss_feed title 'Test Linux feed'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  test

an add rss_feed form
  Go To  ${PLONE_URL}/++add++rss_feed

a rss_feed 'Test Linux feed'
  Create content  type=rss_feed  id=test-linux-feed  title=Test Linux feed


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I type '${url}' into the url field
  Input Text  name=form.widgets.url  ${url}

I submit the form
  Click Button  Save

I go to the rss_feed view
  Go To  ${PLONE_URL}/test-linux-feed
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a rss_feed with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the rss_feed title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

Test Setup
  Open test browser
  Set Window Size  1280  800

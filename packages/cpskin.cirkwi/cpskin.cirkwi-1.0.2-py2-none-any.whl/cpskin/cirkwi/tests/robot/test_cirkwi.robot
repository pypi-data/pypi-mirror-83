# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.messagesviewlet -t test_message.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.messagesviewlet.testing.COLLECTIVE_MESSAGESVIEWLET_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/messagesviewlet/tests/robot/test_message.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Test Setup
Test Teardown  Close all browsers




*** Test Cases ***************************************************************

Scenario: I can add a cirkwi and test its view
  Given a logged-in site administrator
   I create a new cirkwi 'My cirkwi' '3249' '570' 'fr'
   Then a cirkwi 'My cirkwi' has been created with bad domain message 'Domaine non autorisé'

*** Keywords *****************************************************************
    
I create a new cirkwi '${title}' '${host}' '${outil}' '${language}'
  and add cirkwi form
  Input Text  name=form.widgets.IDublinCore.title  ${title}
  Input Text  name=form.widgets.cdf_host  ${host}
  Input Text  name=form.widgets.cdf_outils  ${outil}
  Input Text  name=form.widgets.cdf_lang  ${language}
  and I submit the form
    
      
# --- Given ------------------------------------------------------------------

Test Setup
  Open test browser
  Set Window Size  1280  800
 
a logged-in site administrator
  Enable autologin as  test
  
add cirkwi form
  Go To  ${PLONE_URL}/++add++cirkwi


# --- WHEN -------------------------------------------------------------------

I submit the form
  Click Button  Save  

  
# --- THEN -------------------------------------------------------------------

a cirkwi '${title}' has been created with bad domain message '${message}'
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created
  Sleep  3
  Page should contain  ${message}
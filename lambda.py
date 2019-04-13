"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function

# --------------- Functions related to the session attributes

# set a session attribute
def set_attribute(key, value):
    session_attributes[key] = value

# return a single session attribute
def get_attribute(key):
    return session_attributes[key]


# return those session attributes that are none
def get_none_session_attributes():

    lst_none_attributes = []

    for key in session_attributes:
        if session_attributes[key] == 'none':
            lst_none_attributes.append(key)

    return lst_none_attributes

# --------------- Helpers that build all of the responses ----------------------
session_attributes = {'drtype': 'none', 'location': 'none', 'startTime': 'none', 'endTime': 'none'}
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_session_attribute_respose(attribute, intent):
    # attribute is the type of attribute to be set
    # intent is the intent from the Alexa skill

    # get a list of available attributes
    lst_attributes = list(session_attributes.keys())
    # print(lst_attributes)
    card_title = "test"
    # check if the attribute exists in the list of attributes!
    if attribute not in lst_attributes:
        speech_output = "(get_session_attribute_respose) This attribute is not in the list of attributes. Repeat please."

    else:

        # check if the attribute is none, if it is not, return response that this attribute is already set
        none_session_attributes = get_none_session_attributes()
        if attribute not in none_session_attributes:
            speech_output = "(get_session_attribute_respose) This attribute is already set. Do another one."

        # set the attribute and output the response alexa-style
        else:
            attributeFromAlexa = 'none_in_get_sess_attrib'
            # THIS SHOULD BE CODED UNIFORMLY IN ALEXA
            if attribute == 'location':
                attributeFromAlexa = intent['slots']['location']['value']
            if attribute == 'drtype':
                attributeFromAlexa = intent['slots']['type']['value']


            set_attribute(attribute, attributeFromAlexa)
            none_session_attributes = get_none_session_attributes()

            speech_output = f"Ok. I have set the type to {attribute}. I am missing {none_session_attributes}"

    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False


    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    card_title = "Welcome"
    speech_output = "Welcome to your custom alexa application!"
    # set_attribute('drtype', 'none')
    # set_attribute('location', 'none')
    # set_attribute('startTime', 'none')
    # set_attribute('endTime', 'none')
    print(session_attributes)
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific
        variables from a previous state stored in an external database
    """
    set_attribute('drtype', 'none')
    set_attribute('location', 'none')
    set_attribute('startTime', 'none')
    set_attribute('endTime', 'none')
    # Add additional code here as needed
    pass



def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    # set_attribute('drtype', 'none')
    # set_attribute('location', 'none')
    # set_attribute('startTime', 'none')
    # set_attribute('endTime', 'none')
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(session_attributes)
    # Dispatch to your skill's intent handlers
    if intent_name == "getType":
        return get_session_attribute_respose('drtype', intent)
    # elif intent_name == "getLocation":
    #     return get_session_attribute_respose('location', intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
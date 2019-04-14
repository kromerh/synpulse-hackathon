"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function
import random
import datetime
from datetime import date, timedelta

# --------------- Mockup DataBase, get from SQL

DB_id = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10}
DB_name = {0: 'Dr. Müller', 1: 'Dr. Lu', 2: 'Dr. Frankenstein', 3: 'Dr. Rappen', 4: 'Dr. Mayer', 5: 'Dr. Herz', 6: 'Dr. Wiemer', 7: 'Dr. Boo', 8: 'Dr. Who', 9: 'Dr. Simic'}
DB_plz = {0: '8046',
 1: '8050',
 2: '8047',
 3: '8050',
 4: '8048',
 5: '8049',
 6: '8046',
 7: '8047',
 8: '8049',
 9: '8047'}
DB_type = {0: 'orthopedist', 1: 'cardiologist', 2: 'general physician',3: 'general physician',4: 'general physician',5: 'cardiologist',6: 'general physician',7: 'general physician',8: 'general physician',9: 'emergency section'}
DB_start = {0: '2019-04-15',
 1: '2019-04-20',
 2: '2019-05-02',
 3: '2019-04-15',
 4: '2019-04-20',
 5: '2019-05-02',
 6: '2019-04-22',
 7: '2019-04-22',
 8: '2019-06-01',
 9: '2019-04-15'}
DB_end = {0: '2019-06-30',
 1: '2019-08-02',
 2: '2019-08-20',
 3: '2019-05-02',
 4: '2019-08-01',
 5: '2019-07-10',
 6: '2019-07-11',
 7: '2019-06-21',
 8: '2019-06-20',
 9: '2019-08-02'}

def numCountsInDict(aDict, attribute):
    cnts = dict()
    if attribute in aDict.values():
        for item in aDict.values():
            if item == attribute:
                cnts[item] = cnts.get(item, 0) + 1

        return list(cnts.values())[0]
    else:
        return 0


# --------------- Alexa Phrases and functions related

missing_attributes_phrases = {'drtype': ['The type of doctor you are looking for is required to book your appointment.'],
'plz': ['In which region shall I search? Please tell me a postal code.', 'Tell me a postal code, please.' ],
'start_time': ['When do you wish to get an appointment at the earliest?', 'From when shall I book the appointment?'],
'end_time': ['When should be the latest appointment?', 'And the latest appointmen?']}

confirmationPhrases = ['Ok!', 'Great!', 'Thank you!', 'Roger that!', 'Copy that!', 'I received this!']


def phrases_missing_attributes(missing_attributes):
    #

    confirmation = confirmationPhrases[random.randint(0,len(confirmationPhrases)-1)]

    out_phrase = []

    out_phrase.append(confirmation)

    for item in missing_attributes:
        missingPhrase = missing_attributes_phrases[item][random.randint(0,len(missing_attributes_phrases[item])-1)]
        out_phrase.append(missingPhrase)
    # print(f'out_phrase {out_phrase}')
    res = " ".join(out_phrase)
    return res

# --------------- Functions related to the session attributes

# set a session attribute
def set_attribute(key, value):
    session_attributes[key] = value
    entriesInDB = -1
    if key == 'drtype':
        entriesInDB = numCountsInDict(DB_type, value)
        # print(f'entriesInDB {entriesInDB}')
    if key == 'plz':
        entriesInDB = numCountsInDict(DB_plz, value)
        # print(f'entriesInDB {entriesInDB}')
    return entriesInDB

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
session_attributes = {'drtype': 'none', 'plz': 'none', 'start_time': 'none', 'end_time': 'none'}
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
def get_session_attribute_respose(intent):
    # attribute is the type of attribute to be set
    # intent is the intent from the Alexa skill


    card_title = "test"
    numEntriesInDB = 0
    # print(f'session_attributes in get_session_attribute_respose {session_attributes}')

    # get a list of available attributes
    lst_attributes = list(session_attributes.keys())

    # check which intents there are to be set
    intent_keys = list(intent['slots'].keys())  # which intents there are in the intent dictionary
    attributes_to_set = []

    for k in intent_keys:
        if 'value' in intent['slots'][k]:
            attributes_to_set.append(k)

    print(f'attributes_to_set {attributes_to_set}')
    # for each intent, get the corresponding attribute and check if the value is not alreay set
    none_session_attributes = get_none_session_attributes()
    for attribute in attributes_to_set:
        try:
            attributeFromAlexa = intent['slots'][attribute]['value']
        except:
            attributeFromAlexa = 'PANIC'

        if attribute == 'type':
            attribute = 'drtype' # type is reserved in python

        # check if the attribute exists in the list of attributes!
        if attribute not in lst_attributes:
            speech_output = "(get_session_attribute_respose) This attribute is not in the list of attributes. Repeat please."

        else:

            # check if the attribute is none, if it is not, return response that this attribute is already set

            if attribute not in none_session_attributes:
                speech_output = "(get_session_attribute_respose) This attribute is already set. Do another one."

            # set the attribute and output the response alexa-style
            else:
                print(f'attribute to set {attribute}')
                numEntriesInDB = set_attribute(attribute, attributeFromAlexa)
                print(f'numEntriesInDB {numEntriesInDB}')

    none_session_attributes = get_none_session_attributes()

    if len(none_session_attributes) > 0:  # some empty session attributes, Alexa still will wait for some input
        # go through the non set attributes and create a response based on the values that are missing
        print(f'none_session_attributes {none_session_attributes}')
        resp_phrase = phrases_missing_attributes(none_session_attributes)
        if numEntriesInDB > 0:
            resp_phrase = resp_phrase.split('!')
            confirmation = confirmationPhrases[random.randint(0,len(confirmationPhrases)-1)]

            resp_phrase[0] = f'{confirmation} I found {numEntriesInDB} records in my database.'
            resp_phrase = " ".join(resp_phrase)
        speech_output = resp_phrase
    else:

        # # all attributes filled, appointment will be booked

        confirm = confirmationPhrases[random.randint(0,len(confirmationPhrases)-1)]

        # # what are the attribute values
        # # session_attributes = {'drtype': 'none', 'plz': 'none', 'start_time': 'none', 'end_time': 'none'}
        attribute_values = []
        for k in session_attributes:
            attribute_values.append(session_attributes[k])

        # appointment_date = '2019-05-17' # make up a random appointment date
        start_time = datetime.datetime.strptime(session_attributes['start_time'],'%Y-%m-%d')
        end_time = datetime.datetime.strptime(session_attributes['end_time'],'%Y-%m-%d')

        delta = end_time - start_time         # timedelta

        dates = [start_time + timedelta(i) for i in range(delta.days + 1)]

        appointment_date = dates[random.randint(0,len(dates)-1)]
        appointment_date = datetime.datetime.strftime(appointment_date,'%Y-%m-%d')
        # appointment_date = '2019-04-30'
        appointment_time = '14:00' # make up a random appointment date

        # speech_output = '42'
        speech_output = f'{confirm} I will book an appointment with a doctor of type {attribute_values[0]}, in postal code {attribute_values[1]}. Your appointment is on {appointment_date} at {appointment_time}.'
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False


    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    card_title = "Welcome"
    speech_output = "Welcome to Doctor Who, your automated doctor booking system. How can I help you?"

    # set_attribute('drtype', 'none')
    # set_attribute('plz', 'none')
    # set_attribute('start_time', 'none')
    # set_attribute('end_time', 'none')
    print(session_attributes)
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for booking with Dr. Who! Get well soon. " \
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
    set_attribute('plz', 'none')
    set_attribute('start_time', 'none')
    set_attribute('end_time', 'none')
    # Add additional code here as needed
    pass



def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    # set_attribute('drtype', 'none')
    # set_attribute('plz', 'none')
    # set_attribute('start_time', 'none')
    # set_attribute('end_time', 'none')
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # find out what slots there are in the
    # print(session_attributes)
    # Dispatch to your skill's intent handlers
    if intent_name == "getType":
        return get_session_attribute_respose(intent)
    elif intent_name == "getLocation":
        return get_session_attribute_respose(intent)
    elif intent_name == "getStartTime":
        return get_session_attribute_respose(intent)
    elif intent_name == "getEndTime":
        return get_session_attribute_respose(intent)
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
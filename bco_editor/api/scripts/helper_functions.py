# Helper definitions and functions for all classes.

from ..models import bco_object
from ..serializers import BcoGetSerializer

# For regex.
import re

# For JSON parsing and schema validation.
import json
import jsonref
import jsonschema

# For creating BCO IDs.
from django.conf import settings

# Define regex for individual fields in a BCO.
# ...

# Check for a valid object ID.
def check_object_id_format(object_id_pass):

    # Arguments
    # ---------

    #  object_id_pass:  the ID that we are checking for validity.

    # There are only two valid formats for an object ID,
    # 'New' or a URI of the form acronym://part/part/part/acronym_integer_v_integer
    # We can check for both of these using regex.

    # Create a flag to indicate failure of format.
    format_failure = True

    # Try the easy one first.
    if object_id_pass != 'New':

        # Check the URI regex.
        # Source:  https://stackoverflow.com/questions/12595051/check-if-string-matches-pattern
        # Source:  https://mathiasbynens.be/demo/url-regex

        # if bool(re.match(r"_^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\x{00a1}-\x{ffff}0-9]+-?)*[a-z\x{00a1}-\x{ffff}0-9]+)(?:\.(?:[a-z\x{00a1}-\x{ffff}0-9]+-?)*[a-z\x{00a1}-\x{ffff}0-9]+)*(?:\.(?:[a-z\x{00a1}-\x{ffff}]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$_iuS", object_id_pass)) is False:
        # format_failure = True

        # Try each valid URI pattern.
        for prefix in settings.BCO_PREFIXES:

            # Construct the valid URI regex.
            regex_pattern = prefix + '://' + settings.BCO_ROOT + '/' + settings.BCO_TAG + '_(\d+)_v_(\d+)'

            # See if we match the pattern.
            if bool(re.match(regex_pattern, object_id_pass)) is True:
                # Format success.
                format_failure = False

                # Break the loop, no need to check further patterns.
                break

    else:

        # Brand new object, so no need to check for format failure.
        format_failure = False

    # Return based on the validity.
    if format_failure is True:
        return 'OBJECT_ID_FORMAT_ERROR'

# Check for a set of keys.
def check_key_set_exists(data_pass, key_set):

    # Arguments
    # ---------

    # data_pass:  the 'raw' request data.

    # Go over each key in the key set and see if it exists
    # the in request data.

    # Returns
    # -------

    # None: all keys were present
    # dict: items 'error' and 'associated_key'

    # Assume all keys are present.
    return_value = None

    for current_key in key_set:

        # Was this key found?
        try:

            data_pass[current_key]

        except:

            print('Key ' + current_key + ' not found in request.  This message will only show up in the terminal.')

            # Return the error.
            return_value = {'error': 'INVALID_' + current_key.upper() + '_FAILURE', 'associated_key': current_key}

            # Get out of the loop.
            break

    # Return the return value.
    return return_value


# Check that what was provided was JSON.
def check_json_exists(data_pass, key_set):

    # Arguments
    # --------

    # data_pass:  the 'raw' request data.
    #  key_set:  the keys to check for JSON.

    # Simply check if what was provided was actually JSON.

    # Returns
    # -------

    # None:  the provided data was JSON.
    # JSON_CONVERSION_ERROR:  the provided data was not JSON.

    # Assume all data is JSON.
    return_value = None

    for current_key in key_set:

        # Was this key found?
        try:

            # First, try to convert the payload string into a JSON object.
            json_payload = json.loads(s=data_pass[current_key])

        except:

            print('JSON conversion failure with given payload.  This message will only show up in the terminal.')

            # Return the error.
            return_value = {'error': 'JSON_CONVERSION_ERROR', 'associated_key': current_key}

            # Get out of the loop.
            break

    # Return the return value.
    return return_value


# Check for schema compliance...
'''
# Check for a valid payload.
def check_payload_format_post(payload_pass):

    print(payload_pass)
    # Arguments
    # ---------

    # payload_pass:  the payload that we are checking for validity.

    # The payload for the post must contain a valid JSON object.
    try:

        # First, try to convert the payload string into a JSON object.
        json_payload = json.loads(s=payload_pass)

    except:

        print('JSON conversion failure with given payload.  This message will only show up in the terminal.')

        # Return the error.
        return 'JSON_CONVERSION_ERROR'

    else:

        # The payload is of a valid format, but does it have all
        # the required fields for a BCO?
        print('Schema comp feature to come...')
        # First, get the schema.
        schema = jsonref.load_uri(uri=settings.SCHEMA_27912020_LOCATION, jsonschema=True)
        print(schema)

        # Now see if the validation is good.

        try:

            jsonschema.validate(json_payload, schema)

        except:

            print('Schema template match failure.  This message will only show up in the terminal.')

            # Return the error.
            return 'SCHEMA_MISMATCH_ERROR'
'''

def check_payload_get(payload_pass):
    print('hi')

def check_payload_patch(payload_pass):
    print('te')

# Generate unique object IDs.
def generate_object_id(existing_id=False, version_flag=False):

    # Arguments
    # ---------

    #  existing_id:  an ID that is passed for version updating.

    # version_flag:  if true, we don't need a completely new
    #                object ID, we just need potentially need a new version.
    #                We say potentially need because if existing_id doesn't
    #                exist in the database, then we'll just use existing_id
    #                as the new ID.

    # First, get all BCOs.  These objects are returned as JSON, so
    # we can work with them more easily.
    bco_objects = BcoGetSerializer(bco_object.objects.all(), many=True).data

    # Completely new object or just a new version?
    if version_flag is False:

        # Do we have anything?
        if len(bco_objects) > 0:

            # Get all the IDs.

            # Define a list to hold the object IDs.
            bco_object_ids = []

            # Now go through each object and get its ID.
            for current_object in bco_objects:
                # Extract and append the object ID.
                bco_object_ids.append(current_object['object_id'])

            # Define a variable to hold our new object number.
            new_object_number = 0

            # Define a variable to keep track of the maximum
            # number found so far as we go through the object IDs.
            max_number = -1

            # We want to see what the most react object number is.
            for current_object_id in bco_object_ids:

                # Split on '/', keeping only the last (non-URI) part.
                split_up = current_object_id.split('/')[-1]

                # Split again and keep the number.
                # Note the type conversion from string to int.
                split_up = int(split_up.split('_')[1])

                # Is this greater than our current maximum?
                if split_up > max_number:
                    max_number = split_up

            # Increment the max number and stringify.
            new_number = str(max_number + 1)

            # Create the brand-new object.
            created_id = 'https://' + settings.BCO_ROOT + '/' + settings.BCO_TAG + '_' + new_number + '_v_1'

        else:

            # No objects, so just construct a new one.
            created_id = 'https://' + settings.BCO_ROOT + '/' + settings.BCO_TAG + '_1_v_1'

    else:

        # We may just need a new version of the 'same' object.

        # Get the current version number.
        # Note the type conversion from string to int.
        current_version_number = existing_id.split('/')[-1]
        current_version_number = int(current_version_number.split('_')[-1])

        # Increment the version number.
        # Note the type conversion from int to string.
        incremented = str(current_version_number + 1)

        # Re-form the ID.
        created_id = existing_id.split('/')
        id_helper = created_id[-1]
        id_helper = id_helper.split('_')
        id_helper[len(id_helper) - 1] = incremented
        id_helper = '_'.join(id_helper)
        created_id[len(created_id) - 1] = id_helper
        created_id = '/'.join(created_id)

        # Does this ID already exist (this is possible when incrementing versions
        # for objects if the requester does not realize they are sending a
        # version of the object that is not the latest one)?

        already_exists_flag = False

        for current_object in bco_objects:

            # Does the object ID already exist?
            if current_object['object_id'] == created_id:
                already_exists_flag = True

        # Return based on the existence of the created ID.
        if already_exists_flag is False:
            return created_id
        else:
            return 'VERSION_INCREMENT_ERROR'

    # Return our new ID.
    return created_id

# Retrieve an object from the database.
def retrieve_object(object_id_pass):

    # Arguments
    # ---------

    # object_id_pass:  the ID that we are trying to retrieve.

    try:

        return bco_object.objects.get(object_id=object_id_pass)

    except bco_object.DoesNotExist:

        return 'OBJECT_ID_DOES_NOT_EXIST'

# Commit a draft BCO.
def commit_object_draft(object_id_pass):

    # Arguments
    # ---------

    # object_id_pass:  the ID that we are committing.
    #                  Committed BCOs cannot be edited.

    # Get the object for this ID.
    retrieved = retrieve_object(object_id_pass=object_id_pass)

    # Serialize the object, but only for the 'state' field.
    # Source:  https://stackoverflow.com/questions/50129567/django-rest-update-one-field

    serializer = BcoGetSerializer(retrieved, partial=True)

    # Is the object already committed?

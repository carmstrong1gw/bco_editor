# Based on the "Class Based API View" example at https://codeloop.org/django-rest-framework-course-for-beginners/

# Create your views here.

from .models import bco_object_ieee_2791_2020
from .serializers import Bco27912020Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# For creating BCO IDs.
from django.conf import settings

# For regex.
import re

# For JSON parsing and schema validation.
import json
import jsonref
import jsonschema


class Bco27912020APIView(APIView):


    # Description
    # -----------

    # Follow the basic CRUD (create, read, update, delete) paradigm.
    # A good description of each of these can be found at https://www.restapitutorial.com/lessons/httpmethods.html


    # Helper definitions and functions

    # Define regex for individual fields in a BCO.
    # ...

    # Check for a valid object ID.
    def check_object_id(self, object_id_pass):


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

            #if bool(re.match(r"_^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\x{00a1}-\x{ffff}0-9]+-?)*[a-z\x{00a1}-\x{ffff}0-9]+)(?:\.(?:[a-z\x{00a1}-\x{ffff}0-9]+-?)*[a-z\x{00a1}-\x{ffff}0-9]+)*(?:\.(?:[a-z\x{00a1}-\x{ffff}]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$_iuS", object_id_pass)) is False:
                #format_failure = True

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
        print(format_failure)
        # Return based on the validity.
        if format_failure is True:
            return 'OBJECT_ID_FORMAT_ERROR'


    # Check for a valid payload.
    def check_payload_post(self, payload_pass):

        print(payload_pass)
        # Arguments
        # ---------

        #  payload_pass:  the payload that we are checking for validity.


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

            # First, get the schema.
            schema = jsonref.load_uri(uri=settings.SCHEMA_27912020_LOCATION, jsonschema=True)
            print(schema)

            # Now see if the validation is good.
            '''
            try:

                jsonschema.validate(json_payload, schema)

            except:

                print('Schema template match failure.  This message will only show up in the terminal.')

                # Return the error.
                return 'SCHEMA_MISMATCH_ERROR'
            '''



    def check_payload_get(self, payload_pass):
        print('hi')

    def check_payload_patch(self, payload_pass):
        print('te')

    def check_payload_delete(self, payload_pass):
        print('te')

    # Generate unique object IDs.
    def generate_object_id(self, existing_id=False, version_flag=False):


        # Arguments
        # ---------

        #  existing_id:  an ID that is passed for version updating.

        # version_flag:  if true, we don't need a completely new
        #                object ID, we just need a new version.


        # First, get all BCOs.  These objects are returned as JSON, so
        # we can work with them more easily.
        bco_objects = Bco27912020Serializer(bco_object_ieee_2791_2020.objects.all(), many=True).data

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

            # We just need a new version of the 'same' object.

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
            id_helper[len(id_helper)-1] = incremented
            id_helper = '_'.join(id_helper)
            created_id[len(created_id)-1] = id_helper
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




    # For creating.
    def post(self, request):

        # Serialize the request.
        serializer = Bco27912020Serializer(data=request.data)

        # Did the request pass validation?
        if serializer.is_valid():

            # The serialization is valid, so now we need to generate
            # a unique object ID.
            # Source:  https://stackoverflow.com/questions/36783122/django-rest-framework-perform-create-you-cannot-call-save-after-accessing
            # Another possible solution:  https://stackoverflow.com/questions/22210046/django-form-what-is-the-best-way-to-modify-posted-data-before-validating

            # Get a new object ID based on whether or not the
            # incoming data asks for a new ID or a new version.
            incoming_object_id = request.data['object_id']

            # Make sure that the object ID is of a valid format.
            object_id_format_check = self.check_object_id(object_id_pass=incoming_object_id)

            # Did we pass the format test?
            if object_id_format_check == 'OBJECT_ID_FORMAT_ERROR':
                return Response('OBJECT_ID_FORMAT_ERROR.  Make sure the object ID matches the URI standard for your installation.  In particular, if you are creating a new object, make sure that object_id=\'New\' has no spaces.', status=status.HTTP_400_BAD_REQUEST)

            # Make sure that the payload is of a valid format
            # and meets the requirements of the given schema.
            incoming_payload = request.data['payload']
            payload_checks = self.check_payload_post(payload_pass=incoming_payload)

            # Did we pass the tests?
            if payload_checks == 'JSON_CONVERSION_ERROR':
                return Response('JSON_CONVERSION_ERROR.  Check your payload to ensure that it is a quoted JSON object.', status=status.HTTP_400_BAD_REQUEST)
            elif payload_checks == 'SCHEMA_MISMATCH_ERROR':
                return Response('SCHEMA_MISMATCH_ERROR.  The payload provided did not meet the required fields for the'
                                ' schema at ' + settings.SCHEMA_27912020_LOCATION + '.',
                                status=status.HTTP_400_BAD_REQUEST)




            # The object ID and the payload are valid, so proceed to
            # generate a new ID and store the payload.
            if request.data['object_id'] == 'New':
                new_object_id = self.generate_object_id()
            else:
                new_object_id = self.generate_object_id(existing_id=incoming_object_id, version_flag=True)

            # Did we get a nice new ID or did someone try to
            # get a new version of something that already got
            # incrementally versioned?
            if new_object_id == 'VERSION_INCREMENT_ERROR':
                return Response('VERSION_INCREMENT_ERROR.  Make sure you send the latest version of this BCO.', status=status.HTTP_409_CONFLICT)

            # Save the object ID and the payload.
            serializer.save(object_id=new_object_id)

            # Everything went properly in the request.
            return Response('POSTed object with object_id \'' + incoming_object_id + '\' successfuly saved with object ID \'' + new_object_id + '\'.', status=status.HTTP_201_CREATED)

        else:

            # Something went wrong in the request.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    # For reading.
    def get(self, request):

        bco_objects = bco_object_ieee_2791_2020.objects.all()

        # Get one object or many?  Use the payload to determine
        # how many we get (can use a list of object IDs to retrieve).
        serializer = Bco27912020Serializer(bco_objects, many=True)

        return Response(serializer.data)




    # For patching (updating).
    def patch(self, request):
        print('hi')




    # For deleting.
    def delete(self, request):

        article = self.get_object(id)

        article.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



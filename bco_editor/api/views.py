# Based on the "Class Based API View" example at https://codeloop.org/django-rest-framework-course-for-beginners/

# Create your views here.

from .models import bco_object_ieee_2791_2020
from .serializers import Bco27912020Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# For creating BCO IDs.
from django.conf import settings

class Bco27912020APIView(APIView):


    # Description
    # -----------

    # Follow the basic CRUD (create, read, update, delete) paradigm.
    # A good description of each of these can be found at https://www.restapitutorial.com/lessons/httpmethods.html


    # Helper functions.

    # Generate unique object IDs.
    def generate_object_id(self, request_pass, existing_id=False, version_flag=False):


        # Additional arguments
        # --------------------

        # request_pass:  just a passthrough variable for the original request.

        #  existing_id:  an ID that is passed for version updating.

        # version_flag:  if true, we don't need a completely new
        #                object ID, we just need a new version.


        # Create a variable to hold our created id.
        created_id = ''

        # Completely new object or just a new version?
        if version_flag is False:

            # First, get all BCOs.  These objects are returned as JSON, so
            # we can work with them more easily.
            bco_objects = self.get(request_pass)

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
                split_up = current_object_id.split('/')[:-1]

                # Split again and keep the number.
                # Note the type conversion from string to int.
                split_up = int(split_up.split('_')[1])

                # Is this greater than our current maximum?
                if split_up > max_number:
                    max_number

            # Increment the max number and stringify.
            new_number = str(max_number + 1)

            # Create the brand-new object.
            created_id = 'https://' + settings.BCO_ROOT + '/' + settings.BCO_TAG + '_' + new_number + '_v_1'

        else:

            # We just need a new version of the 'same' object.

            # Get the current version number.
            # Note the type conversion from string to int.
            current_version_number = existing_id.split('/')[:-1]
            current_version_number = int(current_version_number.split('_')[:-1])

            # Increment the version number.
            incremented = current_version_number + 1

            # Re-form the ID.
            created_id = existing_id.split('/')
            id_helper = created_id[:-1]
            id_helper = id_helper.split('_')
            id_helper[len(id_helper)-1] = incremented
            id_helper = '_'.join(id_helper)
            created_id[len(created_id)-1] = id_helper
            created_id = '/'.join(created_id)

        # Return our new ID.
        return created_id




    # For creating.
    def post(self, request):

        serializer = Bco27912020Serializer(data=request.data)

        if serializer.is_valid():

            # The serialization is valid, so now we need to generate
            # a unique object ID (passing through the original request).
            #new_object_id = self.generate_object_id(request)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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



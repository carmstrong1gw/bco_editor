from django.db import models

# Create your models here.

# Explanation of optional fields:  https://stackoverflow.com/questions/16349545/optional-fields-in-django-models
# TextField is used here because it has no character limit.

# Generic BCO model.
class bco_object(models.Model):

	# The unique object ID.

	# Field is required.
	object_id = models.TextField()

	# The schema under which the object falls.

	# Field is optional.
	schema = models.TextField(blank=True, null=True)

	# The entirety of the BCO.

	# Field is optional.
	bco = models.TextField(blank=True, null=True)

	# The state of the object, is it a draft or is it committed?

	# Field is optional.
	state = models.TextField(blank=True, null=True)

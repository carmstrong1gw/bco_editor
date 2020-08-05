from django.db import models

# Create your models here.

# IEEE 2791-2020
class bco_object_ieee_2791_2020(models.Model):

	# The unique object ID.
	object_id = models.TextField()

	# The payload, essentially the entirety of the BCO.
	# TextField is used here because it has no character limit.

	# Field is optional.
	# Source:  https://stackoverflow.com/questions/16349545/optional-fields-in-django-models
	payload = models.TextField(blank=True, null=True)

	# The state of the object, is it a draft or is it commited?

	# Field is optional.
	# Source:  https://stackoverflow.com/questions/16349545/optional-fields-in-django-models
	state = models.TextField(blank=True, null=True)

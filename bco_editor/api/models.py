from django.db import models

# Create your models here.

# IEEE 2791-2020
class bco_object_ieee_2791_2020(models.Model):

	# The unique object ID.
	object_id = models.TextField()

	# The payload, essentially the entirety of the BCO.
	# TextField is used here because it has no character limit.
	payload = models.TextField()

	def __str__(self):
		return self.object_id

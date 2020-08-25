from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

def authenticate(user_id, password):
	"""
	Handle authenticate process
	"""
	user = None
	
	if '@' in user_id: # if user_id is an email
		try: 
			User.objects.get(email=user_id)
		except:
			return None
		else:
			user = User.objects.get(email=user_id)

	else: # if user_id is a username
		try:
			User.objects.get(username=user_id)
		except:
			return None
		else:
			user = User.objects.get(username=user_id)

	# Verify password
	if check_password(password, user.password):
		return user
	
	return None
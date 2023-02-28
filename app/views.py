from django.shortcuts import redirect
from django.views import View
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import Error as OAuth2ClientError
from googleapiclient.discovery import build
from django.http import JsonResponse


class GoogleCalendarInitView(View):

	def get(self, request):
		flow = OAuth2WebServerFlow(
		 client_id=
		 '721314022781-je48sfkofi0b4nsvnhjn9mvqgc93jvsd.apps.googleusercontent.com',
		 client_secret='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',
		 scope='https://www.googleapis.com/auth/calendar.readonly',
		 redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/',
		)

		auth_url = flow.step1_get_authorize_url()
		return redirect(auth_url)


class GoogleCalendarRedirectView(View):

	def get(self, request, *args, **kwargs):
		code = request.GET.get('code')
		if not code:
			return redirect('/rest/v1/calendar/init/')

		# Exchange authorization code for access token
		try:
			flow = OAuth2WebServerFlow(
			 client_id=
			 '721314022781-je48sfkofi0b4nsvnhjn9mvqgc93jvsd.apps.googleusercontent.com',
			 client_secret='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',
			 scope='https://www.googleapis.com/auth/calendar',
			 redirect_uri=request.build_absolute_uri('/rest/v1/calendar/redirect/'))
			credentials = flow.step2_exchange(code)
			access_token = credentials.access_token
		except OAuth2ClientError as e:
			return JsonResponse({'error': str(e)}, status=400)

		# Get list of events from calendar
		try:
			service = build('calendar', 'v3', credentials=credentials)
			events_result = service.events().list(calendarId='primary',
			                                      maxResults=10,
			                                      singleEvents=True,
			                                      orderBy='startTime').execute()
			events = events_result.get('items', [])
		except Exception as e:
			return JsonResponse({'error': str(e)}, status=500)

		return JsonResponse({'access_token': access_token, 'events': events})

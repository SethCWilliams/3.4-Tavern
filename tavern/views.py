from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.utils import timezone

from .models import Location, Lunch


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """
        Return the last five published contests (not including those set to be
        published in the future).
        """
        lunches = Lunch.objects.filter(
            date__lte=timezone.now()
        ).order_by('date')[:5]

        context = {
            'latest_lunches': lunches
        }

        return context


class LunchDetailView(TemplateView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        available_options = Location.objects.all()
        # The contest primary key is included on the url: localhost:8000/5/
        # We use value capturing in our urls.py to get the # 5 and save it to pk
        # The pk variable is in the dictionary self.kwargs, and we can use .get() on
        # the self.kwargs dict.
        vote_pk = self.kwargs.get('pk')

        # Now that we have the primary key for the contest, use the ORM to get the
        # object from the database
        vote = Lunch.objects.get(pk=vote_pk)

        # Create a context dictionary that will be sent to our template
        context = {
            'details': available_options,
            'vote': vote,
        }

        # Our get_context_data() function always expects us to return a context dict
        return context


class LunchResultsView(TemplateView):
    template_name = 'results.html'

    def get_context_data(self, **kwargs):
        # The contest primary key is included on the url: locahost:8000/5/results/
        # We use value capturing in our urls.py to get the # 5 and save it to pk
        # The pk variable is in the dictionary self.kwargs, and we can use .get() on
        # the self.kwargs dict.
        vote_pk = self.kwargs.get('pk')

        # Now that we have the primary key for the contest, use the ORM to get the
        # object from the database
        vote = Lunch.objects.get(pk=vote_pk)

        # Create a context dictionary that will be sent to our template
        context = {
            'vote': vote
        }

        # Our get_context_data() function always expects us to return a context dict
        return context


# This view will not be a template view since we won't actually show a screen.
# Once a user submits to this screen we will redirect.
class LunchVoteView(View):

    # We are going to receive a POST request with this view, so we're going to create a method called post.
    def post(self, request, **kwargs):
        # The contest primary key is included on the url: locahost:8000/5/vote/
        # We use value capturing in our urls.py to get the # 5 and save it to pk
        # The pk variable is in the dictionary self.kwargs, and we can use .get() on
        # the self.kwargs dict.
        vote_pk = self.kwargs.get('pk')

        # Now that we have the primary key for the contest, use the ORM to get the
        # object from the database
        vote = Lunch.objects.get(pk=vote_pk)

        # The user selected a picture that they wanted to vote for in the contest.
        # They selected one of the radio buttons: <input name="photo" value="2" .../>
        # When they submitted the form, the name of the input got sent to the server with the value in the input.
        # We can use the input name get the value from the POST dictionary.
        lunch_spot_voted_for_id = self.request.POST.get('location')

        # Now we want to take our contest and lookup the photo object that the user selected
        selected_lunch_spot = vote.location_set.get(pk=lunch_spot_voted_for_id)

        selected_lunch_spot.votes += 1
        selected_lunch_spot.save()

        # Now get the URL for our results screen using the route name from urls.py
        results_url = reverse('tavern:results', args=(vote.pk,))

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(results_url)

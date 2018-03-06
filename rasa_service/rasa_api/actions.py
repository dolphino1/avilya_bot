from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet


class ActionVolunteer(Action):
    def name(self):
        return 'action_volunteer'

    def run(self, dispatcher, tracker, domain):
        # dispatcher.utter_attachment("www.google.com/lala")
        # dispatcher.utter_message("As a part of our general approach to \
        #     Corporate Social Responsibility, the Company is very supportive \
        #     of personal volunteering efforts. I’ll send you a file detailing \
        #     the projects people are currently involved in with a list of the \
        #     project leaders.")
        dispatcher.utter_custom_message({"response_text": "wow", "file_upload_name": "volunteer_projects.png"})
        return []


class ActionHarassmentPolicy(Action):
    def name(self):
        return 'action_harassment_policy'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Yes, the company treats this area very \
            seriously. You can find our company “Dignity at Work” policy \
            here;  P:/Company_DatW_Policy_doc. The contact person for your \
            area in the context of the policy is Paddy \
            (paddy.smith@company.com) and you can contact them directly in \
            full confidence if you wish to discuss any aspect of the policy \
            or have any concerns.")
        return []


class ActionGiveMaternityLeavePolicy(Action):
    def name(self):
        return 'action_give_maternity_leave_policy'

    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot("topic")
        context = tracker.get_slot("context")
        if topic and context:
            dispatcher.utter_message(context)
            dispatcher.utter_message(topic)
        else:
            dispatcher.utter_message("I don't know what you meant")
        return []


class ActionGiveDentalPolicy(Action):
    def name(self):
        return 'action_give_dental_policy'

    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot("topic")
        if topic:
            dispatcher.utter_message(topic)
        else:
            dispatcher.utter_message("I don't know what you meant")
        return []


class ActionSearchConcerts(Action):
    def name(self):
        return 'action_search_concerts'

    def run(self, dispatcher, tracker, domain):
        concerts = [
            {"artist": "Foo Fighters", "reviews": 4.5},
            {"artist": "Katy Perry", "reviews": 5.}
        ]
        description = ", ".join([c["artist"] for c in concerts])
        dispatcher.utter_message("{}".format(description))
        return [SlotSet("concerts", concerts)]


class ActionSearchVenues(Action):
    def name(self):
        return 'action_search_venues'

    def run(self, dispatcher, tracker, domain):
        venues = [
            {"name": "Big Arena", "reviews": 4.5},
            {"name": "Rock Cellar", "reviews": 5.}
        ]
        dispatcher.utter_message("here are some venues I found")
        description = ", ".join([c["name"] for c in venues])
        dispatcher.utter_message("{}".format(description))
        return [SlotSet("venues", venues)]


class ActionShowConcertReviews(Action):
    def name(self):
        return 'action_show_concert_reviews'

    def run(self, dispatcher, tracker, domain):
        concerts = tracker.get_slot("concerts")
        dispatcher.utter_message("concerts from slots: {}".format(concerts))
        return []


class ActionShowVenueReviews(Action):
    def name(self):
        return 'action_show_venue_reviews'

    def run(self, dispatcher, tracker, domain):
        venues = tracker.get_slot("venues")
        dispatcher.utter_message("venues from slots: {}".format(venues))
        return []

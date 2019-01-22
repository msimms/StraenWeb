# Copyright 2018 Michael J Simms
"""Schedules computationally expensive analysis tasks"""

from bson.json_util import dumps
from ActivityAnalyzer import analyze_activity
import Keys

class AnalysisScheduler(object):
    """Class for scheduling computationally expensive analysis tasks."""

    def __init__(self):
        self.enabled = True
        super(AnalysisScheduler, self).__init__()

    def add_to_queue(self, activity, activity_user_id):
        """Adds the activity ID to the list of activities to be analyzed."""
        if not self.enabled:
            return

        if Keys.ACTIVITY_USER_ID_KEY not in activity:
            activity[Keys.ACTIVITY_USER_ID_KEY] = activity_user_id
        analysis_obj = analyze_activity.delay(dumps(activity))
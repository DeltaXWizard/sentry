from collections import defaultdict
from datetime import timedelta

from django.db.models import Avg, F
from django.db.models.functions import TruncDay
from rest_framework.response import Response

from sentry.api.base import EnvironmentMixin
from sentry.api.bases.team import TeamEndpoint
from sentry.api.utils import get_date_range_from_params
from sentry.models import GroupHistory, GroupHistoryStatus, Project


class TeamTimeToResolutionEndpoint(TeamEndpoint, EnvironmentMixin):
    def get(self, request, team):
        """
        Return a a time bucketed list of mean group resolution times for a given team.
        """
        project_list = Project.objects.get_for_team_ids(team_ids=[team.id])
        start, end = get_date_range_from_params(request.GET)
        history_list = (
            GroupHistory.objects.filter(
                status=GroupHistoryStatus.RESOLVED,
                project__in=project_list,
                date_added__gte=start,
                date_added__lte=end,
            )
            .annotate(bucket=TruncDay("date_added"))
            .values("bucket", "prev_history_date")
            .annotate(ttr=F("date_added") - F("prev_history_date"))
            .annotate(avg_ttr=Avg("ttr"))
        )
        sums = defaultdict(dict)
        for gh in history_list:
            key = str(gh["bucket"])
            if "sum" in sums[key]:
                sums[key]["sum"] += gh["ttr"]
                sums[key]["count"] += 1
            else:
                sums[key] = {"sum": gh["ttr"], "count": 1}
        current_day = start.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        end_day = end.replace(hour=0, minute=0, second=0, microsecond=0)
        avgs = {}
        while current_day <= end_day:
            key = str(current_day)
            if key in sums:
                avg = int((sums[key]["sum"] / sums[key]["count"]).total_seconds())
                count = sums[key]["count"]
            else:
                avg = 0
                count = 0

            avgs[key] = {"avg": avg, "count": count}

            current_day += timedelta(days=1)

        return Response(avgs)

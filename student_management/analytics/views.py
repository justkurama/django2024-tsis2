from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg
from django.db.models import Prefetch
from .models import ApiRequestLog, CourseViewLog
from users.models import User
from courses.models import Course

class APIUsageMetricsView(APIView):
    def get(self, request):
        total_requests = ApiRequestLog.objects.count()
        requests_per_user = ApiRequestLog.objects.values('user__username').annotate(count=Count('id')).order_by('-count')
        most_active_users = requests_per_user[:5]
        unique_users = User.objects.filter(apirequestlog__isnull=False).distinct().count()
        avg_requests_per_user = total_requests / unique_users if unique_users > 0 else 0

        data = {
            "total_requests": total_requests,
            "requests_per_user": requests_per_user,
            "most_active_users": most_active_users,
            "unique_users": unique_users,
            "avg_requests_per_user": avg_requests_per_user,
        }
        return Response(data)

class CoursePopularityMetricsView(APIView):
    def get(self, request):
        most_viewed_courses = CourseViewLog.objects.values('course__name').annotate(count=Count('id')).order_by('-count')[:5]
        least_viewed_courses = CourseViewLog.objects.values('course__name').annotate(count=Count('id')).order_by('count')[:5]

        data = {
            "most_viewed_courses": most_viewed_courses,
            "least_viewed_courses": least_viewed_courses,
        }
        return Response(data)
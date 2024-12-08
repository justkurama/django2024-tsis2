from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import ApiRequestLog, CourseViewLog
from users.models import User
from courses.models import Course

class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser')
        self.course = Course.objects.create(name='Test Course')
        ApiRequestLog.objects.create(user=self.user, endpoint='/api/test/', method='GET')
        CourseViewLog.objects.create(user=self.user, course=self.course)

    def test_api_usage_metrics(self):
        response = self.client.get(reverse('api-usage'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_requests', response.data)
        self.assertIn('requests_per_user', response.data)
        self.assertIn('most_active_users', response.data)
        self.assertIn('unique_users', response.data)
        self.assertIn('avg_requests_per_user', response.data)

    def test_course_popularity_metrics(self):
        response = self.client.get(reverse('course-popularity'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('most_viewed_courses', response.data)
        self.assertIn('least_viewed_courses', response.data)
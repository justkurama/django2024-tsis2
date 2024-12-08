from django.utils.timezone import now
from django.core.mail import send_mail
from celery import shared_task
import logging

from attendance.models import Attendance
from grades.models import Grade
from students.models import Student

logger = logging.getLogger(__name__)

SENDER_EMAIL = "tolebayevk0723@gmail.com"

@shared_task
def send_attendance_reminder(student_name, student_email):
    try:
        send_mail(
            subject="Daily Attendance Reminder",
            message=f"Dear {student_name},\n\nYou have not marked your attendance for today. Please log in and mark your attendance now.",
            from_email=SENDER_EMAIL,
            recipient_list=[student_email],
        )
        logger.info(f"Attendance reminder sent to {student_email}")
        return {"success": 1, "failed": 0}
    except Exception as e:
        logger.error(f"Failed to send email to {student_email}: {e}")
        return {"success": 0, "failed": 1}


@shared_task
def notify_grade_update(student_id, course_name, grade):
    try:
        student = Student.objects.get(id=student_id)
        send_mail(
            subject="Grade Update Notification",
            message=f"Your grade for {course_name} has been updated to {grade}.",
            from_email=SENDER_EMAIL,
            recipient_list=[student.email],
        )
        logger.info(f"Grade update notification sent to {student.email}")
        return f"Grade update notification sent to {student.name}."
    except Student.DoesNotExist:
        logger.error(f"Student with id {student_id} does not exist.")
        return f"Student with id {student_id} does not exist."


@shared_task
def generate_daily_report():
    today = now().date()
    attendance_summary = Attendance.objects.filter(date=today).count()
    grades_summary = Grade.objects.filter(date=today).count()

    admin_email = SENDER_EMAIL
    send_mail(
        subject="Daily Report",
        message=f"Today's Attendance: {attendance_summary}\nGrades Updated: {grades_summary}",
        from_email=admin_email,
        recipient_list=[admin_email],
    )
    logger.info("Daily report sent to admin.")
    return "Daily report sent to admin."


@shared_task
def send_weekly_performance_summary():
    students = Student.objects.all()
    for student in students:
        grades = Grade.objects.filter(student=student)
        summary = "Weekly Performance Summary:\n\n"
        for grade in grades:
            summary += f"{grade.course.name}: {grade.grade}\n"
        send_mail(
            subject="Weekly Performance Summary",
            message=summary,
            from_email=SENDER_EMAIL,
            recipient_list=[student.email],
        )
    logger.info(f"Weekly summaries sent to {students.count()} students.")
    return f"Weekly summaries sent to {students.count()} students."

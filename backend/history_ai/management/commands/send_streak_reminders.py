"""Bugun hali mashq qilmagan va ketma-ketligi (streak) uzilish arafasida bo'lgan
foydalanuvchilarga eslatma email yuboradi. Kuni har kuni bir marta (masalan kechqurun)
ishga tushirish uchun mo'ljallangan (Render Cron Job yoki boshqa rejalashtiruvchi orqali):

    python manage.py send_streak_reminders
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from ...services import gamification


class Command(BaseCommand):
    help = "Streak uzilish arafasida bo'lgan foydalanuvchilarga eslatma email yuboradi."

    def handle(self, *args, **options):
        today = timezone.localdate()
        User = get_user_model()
        sent = 0
        skipped_no_email = 0

        users = (
            User.objects.filter(is_active=True)
            .exclude(email='')
            .select_related('learning_settings')
        )
        for user in users:
            st = gamification.get_settings(user)
            if not st.email_reminders or st.last_reminder_sent == today:
                continue
            info = gamification.streak_info(user)
            # Faqat ketma-ketligi bor, bugun hali faol bo'lmagan va muzlatish bilan
            # avtomatik qoplanmaydigan (ya'ni haqiqatan xavf ostidagi) foydalanuvchilarga yuboriladi.
            if info['current'] < 1 or info['active_today']:
                continue
            if not user.email:
                skipped_no_email += 1
                continue
            name = user.first_name or user.username
            send_mail(
                f"{name}, {info['current']} kunlik ketma-ketligingiz uzilmoqda!",
                f"Salom, {name}!\n\n"
                f"Siz {info['current']} kun ketma-ket mashq qilib kelayapsiz - zo'r natija! "
                "Lekin bugun hali hech narsa o'rganmadingiz, bugun tugashidan oldin bir nechta "
                "savolga javob bering, ketma-ketlik uzilmasin.\n\n"
                f"Davom eting: {settings.FRONTEND_URL}\n",
                settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True,
            )
            st.last_reminder_sent = today
            st.save(update_fields=['last_reminder_sent'])
            sent += 1

        self.stdout.write(self.style.SUCCESS(
            f"{sent} ta eslatma yuborildi (email yo'q: {skipped_no_email})."
        ))

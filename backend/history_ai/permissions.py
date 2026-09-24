from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """Faqat o'qituvchi (is_staff) generatsiyani ishga tushira oladi.

    Hozircha alohida rol modeli qurmasdan Django'ning mavjud is_staff
    maydonidan foydalanamiz; ERP'ga qo'shilganda haqiqiy rol tizimiga
    almashtirish oson (faqat shu klassni yangilash kifoya).
    """

    message = "Faqat o'qituvchi AI natija yaratishni ishga tushira oladi."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

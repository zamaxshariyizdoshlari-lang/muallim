"""Do'stlar: so'rov yuborish/qabul qilish va ular bilan ball solishtirish.

Bitta juft foydalanuvchi orasida faqat bitta `Friendship` yozuvi bo'ladi (kim so'rov
yuborganidan qat'iy nazar `status='accepted'` bo'lsa ikki tomonlama hisoblanadi).
"""
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum

from ..models import Friendship, XPEvent
from . import gamification

User = get_user_model()


def _pair(a_id, b_id):
    return Friendship.objects.filter(
        Q(from_user_id=a_id, to_user_id=b_id) | Q(from_user_id=b_id, to_user_id=a_id)
    ).first()


def send_request(user, target_username):
    target = User.objects.filter(username__iexact=target_username.strip()).exclude(id=user.id).first()
    if not target:
        return None, "Bunday foydalanuvchi topilmadi."
    existing = _pair(user.id, target.id)
    if existing:
        if existing.status == Friendship.STATUS_ACCEPTED:
            return None, "Siz allaqachon do'stsiz."
        return None, "So'rov allaqachon yuborilgan."
    Friendship.objects.create(from_user=user, to_user=target, status=Friendship.STATUS_PENDING)
    return target, None


def accept_request(user, from_username):
    fr = Friendship.objects.filter(
        from_user__username__iexact=from_username.strip(), to_user=user, status=Friendship.STATUS_PENDING,
    ).first()
    if not fr:
        return False
    fr.status = Friendship.STATUS_ACCEPTED
    fr.save(update_fields=['status'])
    return True


def decline_or_cancel(user, other_username):
    """Kiruvchi so'rovni rad etish YOKI o'zi yuborgan so'rovni bekor qilish."""
    deleted, _ = Friendship.objects.filter(
        Q(from_user=user, to_user__username__iexact=other_username)
        | Q(to_user=user, from_user__username__iexact=other_username),
        status=Friendship.STATUS_PENDING,
    ).delete()
    return deleted > 0


def remove_friend(user, other_username):
    deleted, _ = Friendship.objects.filter(
        Q(from_user=user, to_user__username__iexact=other_username)
        | Q(to_user=user, from_user__username__iexact=other_username),
        status=Friendship.STATUS_ACCEPTED,
    ).delete()
    return deleted > 0


def _public_user(u, weekly_by_user):
    return {
        'username': u.username,
        'name': u.first_name or u.username,
        'xp': gamification.total_xp(u),
        'weekly_points': weekly_by_user.get(u.id, 0),
        'streak': gamification.streak_info(u)['current'],
    }


def friends_summary(user):
    accepted = Friendship.objects.filter(
        Q(from_user=user) | Q(to_user=user), status=Friendship.STATUS_ACCEPTED,
    ).select_related('from_user', 'to_user')
    friend_users = [f.to_user if f.from_user_id == user.id else f.from_user for f in accepted]

    incoming = Friendship.objects.filter(to_user=user, status=Friendship.STATUS_PENDING).select_related('from_user')
    outgoing = Friendship.objects.filter(from_user=user, status=Friendship.STATUS_PENDING).select_related('to_user')

    all_ids = [u.id for u in friend_users] + [user.id]
    weekly = dict(
        XPEvent.objects.filter(user_id__in=all_ids, created_at__gte=gamification.week_start())
        .values('user_id').annotate(s=Sum('points')).values_list('user_id', 's')
    )

    me = _public_user(user, weekly)
    friends = sorted(
        [_public_user(u, weekly) for u in friend_users], key=lambda r: r['weekly_points'], reverse=True,
    )
    return {
        'me': me,
        'friends': friends,
        'incoming': [{'username': f.from_user.username, 'name': f.from_user.first_name or f.from_user.username} for f in incoming],
        'outgoing': [{'username': f.to_user.username, 'name': f.to_user.first_name or f.to_user.username} for f in outgoing],
    }


def search_users(user, query, limit=8):
    q = query.strip()
    if len(q) < 2:
        return []
    friends_and_pending = Friendship.objects.filter(Q(from_user=user) | Q(to_user=user)).values_list(
        'from_user_id', 'to_user_id',
    )
    exclude_ids = {user.id}
    for a, b in friends_and_pending:
        exclude_ids.update([a, b])
    users = (
        User.objects.filter(username__icontains=q).exclude(id__in=exclude_ids)[:limit]
    )
    return [{'username': u.username, 'name': u.first_name or u.username} for u in users]

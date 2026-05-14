from .forms import LabelForm
from .models import Email, Label, Recipient


def mail_sidebar(request):
    if not request.user.is_authenticated:
        return {}

    unread_count = (
        Recipient.objects.filter(user=request.user, has_read=False)
        .exclude(email__status=Email.Status.DELETED)
        .exclude(email__deleted_by=request.user)
        .distinct()
        .count()
    )

    return {
        "sidebar_unread_count": unread_count,
        "sidebar_labels": Label.objects.filter(owner=request.user),
        "sidebar_label_form": LabelForm(),
    }

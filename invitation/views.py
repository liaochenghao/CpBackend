from rest_framework import mixins, viewsets
from invitation.models import Invitation
from invitation.serializer import InvitationSerializer


class InvitationView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        inviter = self.request.query_params.get('inviter')
        invitee = self.request.query_params.get('invitee')
        if inviter:
            queryset = queryset.filter(inviter=inviter)
        if invitee:
            queryset = queryset.filter(invitee=invitee)
        return queryset

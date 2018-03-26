from DimeAPI.models import UserProfile
from DimeAPI.serializer import UserProfileSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class UserProfileView(generics.ListAPIView):
    model = UserProfile
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    lookup_url_kwarg = 'User_Id'
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        return UserProfile.objects.filter(pk=self.request.user.user_profile.pk)


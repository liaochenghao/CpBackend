from rest_framework import routers
from user_info.views import UserInfoView, UserInfoDetailView

router = routers.SimpleRouter()
router.register(r'user_info', UserInfoView)
router.register(r'user_detail', UserInfoDetailView)

urlpatterns = router.urls

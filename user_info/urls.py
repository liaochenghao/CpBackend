from rest_framework import routers
from user_info.views import UserInfoView

router = routers.SimpleRouter()
router.register(r'user_info', UserInfoView)
urlpatterns = router.urls

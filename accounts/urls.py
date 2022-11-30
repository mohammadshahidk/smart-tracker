from rest_framework.routers import SimpleRouter

from accounts.models import ProjectUser

from accounts.views import SignupView
from accounts.views import LoginView

router = SimpleRouter()

router.register(r'signup', SignupView, basename='Sign-Up')
router.register(r'login', LoginView, basename='Log-in')

urlpatterns = router.urls

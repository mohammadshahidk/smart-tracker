from rest_framework.routers import SimpleRouter

from accounts.models import ProjectUser

from accounts import views as account_views

router = SimpleRouter()

router.register(r'signup', account_views.SignupView, basename='Sign-Up')
router.register(r'login', account_views.LoginView, basename='Log-in')
router.register(r'password/reset', account_views.PasswordResetView, basename='password-reset')
router.register(r'users', account_views.UserView, basename='account-view')

urlpatterns = router.urls

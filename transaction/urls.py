from rest_framework.routers import SimpleRouter

from transaction import views as trans_views

router = SimpleRouter()

router.register(r'account', trans_views.AccountView, basename='sources')
router.register(
    r'transaction', trans_views.TransactionView, basename='transactions')

urlpatterns = router.urls

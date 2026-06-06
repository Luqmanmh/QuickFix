from django.urls import path, include
from . import views

urlpatterns = [
  path("usermng/login", views.LoginView.as_view(), name="login"),
  path("usermng/refresh", views.TokenRefreshCookieView.as_view(), name="refresh"),
  path("usermng/signup", views.SignupView.as_view(), name="signup"),
  path("usermng/verify-email", views.VerifyEmailView.as_view(), name="verify email"),
  
  path("shop/itemlist", views.ProductShopItemListView.as_view(), name="item list for shop"),
  path("shop/autocomplete", views.ProductAutocompleteView.as_view(), name="item autocomplete for search"),
  path("shop/details/<str:id>", views.ProductDetailView.as_view(), name="item shop details"),
  
  path("manage/list", views.ProductManageListView.as_view(), name="Staff Item List"),
  
  path("category/list", views.CategoryListView.as_view(), name="category list"),
  
  path("supplier/list", views.SupplierListView.as_view(), name="Supplier list"),
  
  path("cartitem/action", views.CartItemsView.as_view(), name="cart items actions"),
  
  path("batch/action", views.BatchActionsView.as_view(), name="batch actions"),
  
  path("product/action", views.ProductActionsView.as_view(), name="product actions"),
  path("product/activate", views.ProductActivateView.as_view(), name="product activate"),
  
  path("order/create", views.CreateOrderView.as_view(), name="Order create"),
  path("order/list", views.OrderListView.as_view(), name="User Order List"),
  path("order/manage/list", views.OrderManageListView.as_view(), name="Staff Order List"),
  path("order/prepready/<str:id>", views.PrepReadyOrderView.as_view(), name="set to Prep Or ready"),
  path("order/scan", views.cashierOrderView.as_view(), name="cashier scan qr"),
  path("order/pay/<str:id>", views.OrderOnSItePayView.as_view(), name="set to paid"),
  path("order/complete/<str:id>", views.OrderCompleteView.as_view(), name="set to complete"),
  
  path("orderitem/manage/<str:id>", views.OrderItemsListView.as_view(), name="Order Item for Phar"),
  path("orderitem/setbatch", views.setOrderItemBatch.as_view(), name="Order Item set batch"),
]

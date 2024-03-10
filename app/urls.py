
from django.urls import path
from .views import columns, index,get_csvfile,other_page,crud,signin,signup,na_value

urlpatterns = [
    path("",index.home,name = "home"),
    path("signup",signup.signup,name = "signup"),
    path("signin",signin.signin,name = "signin"),
    path("signout",signin.signout,name = "signout"),
    path("upload_csv",get_csvfile.upload_csv,name = "upload_csv"),
    path("delete_file/<str:id>/", crud.delete_file, name="delete_file"),
    path("show_data/<str:id>/", crud.show_data, name="show_data"),
    path("dasboard",crud.dasboard,name = "dasboard"),
    path("delete_columns/<str:id>/",columns.delete_columns, name="delete_columns"),
    path("rename_columns/<str:id>/",columns.rename_columns, name="rename_columns"),
    path('other_page', other_page.other_page, name='other_page'),
    path("dropna/<str:id>/",na_value.dropna,name = "dropna"),
    path("fillna/<str:id>/",na_value.fillna,name = "fillna"),

]


from django.contrib import admin
from .models import WhyChooseUs, Feedback, User, ReviewUser, Catalog, BasketUser, OrderUser,OrderStatus
# Register your models here.

admin.site.register(WhyChooseUs)
admin.site.register(Feedback)
admin.site.register(User)
admin.site.register(ReviewUser)
admin.site.register(Catalog)
admin.site.register(BasketUser)
admin.site.register(OrderUser)
admin.site.register(OrderStatus)
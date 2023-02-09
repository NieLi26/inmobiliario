# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import CustomUser


# def create_user_subscription(sender, instance, created, **kwargs):
#     form_used = kwargs.get('form_used')
#     if created:
#         print(form_used)
#     pass

# post_save.connect(create_user_subscription, CustomUser)
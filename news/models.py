from datetime import date, time
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

from concurrency.models import ConcurrentModel



class Article(ConcurrentModel):
    title = models.CharField(
        max_length=100
    )
    ingress = models.TextField(
        blank=True,
        null=True,
    )
    content = RichTextUploadingField(
        blank=True,
        null=True,
    )
    banner = models.ImageField(
        blank=True,
        null=True,
        default=None,
        upload_to='web/img/article/banners',
    )
    published = models.BooleanField(default=False)
    pinned = models.BooleanField(
        default=False,
    )
    datetime_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = (
            '-datetime_created',
        )


class Event(Article):
    start_date = models.DateField(
        default=date.today,
    )
    start_time = models.TimeField(
        default=time.min,
    )
    end_date = models.DateField(
        null=True,
    )
    end_time = models.TimeField(
        null=True,
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    location_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
    )
    location_url_embed = models.URLField(
        max_length=250,
        blank=True,
        null=True,
    )
    location_off_campus = models.BooleanField(
        default=False
    )
    signup_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
    )
    facebook_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
    )

    registration_closed_time = models.DateTimeField(
        null=False,
        default=timezone.now
    )

    class Meta:
        ordering = (
            '-start_date',
            '-start_time'
        )
    
    def register(self, registration):
        """
        :param registration
        :return The registration now in the chosen pool
        """
        
        # Check if the registration is registered after registration closed time
        if self.registration_closed_time < timezone.now:
            # TODO: Should rais an error? What error? Where do we deffine this?
            raise Exception("It's to late for registrations!")
        
        user = registration.user
        all_pools = self.pools.all()
        possible_pools = self.get_possible_pools(
            user=user, pools=all_pools
        )

        # If no pools are available, the user is not able to register for the event
        if not possible_pools:
            # TODO: Should raise an error for not beeing able to join the event. Less generic exception?
            raise Exception("The user is not able to register for the event!")

        # Check if possible pools are full. If they are, then add user to waiting list
        free_pools = self.get_open_pools(pools=possible_pools)
        if not free_pools:
            return registration.add_to_waiting_list()
        if len(free_pools) == 1:
            return registraion.register_to_pole(free_pools[0])

        choces_pool = self.get_most_exclusive_pool(free_pools)
        return registraion.register_to_pole(pool)


    def get_possible_pools(self, user, pools):
        legal_pools = []
        for pool in pools:
            if pool.check_user_accessability(user):
                legal_pools.append(pool)
        return legal_pools

    def get_open_pools(self, pools):
        open_pools = []
        for pool in pools:
            if not pool.is_full:
                open_pools.append(pool)
        return open_pools

    def get_most_exclusive_pool(self, pools):
        # TODO: Find the most exclusive pool from the list of pools
        return pools[0]

    def unregister(self):
        # TODO: Remove user from the pole and register the first person from the waiting list
        #       to join the event.
        pass


    # TODO: Is this needed? Already have the Registration add to waiting list function!
    # Needed if somone needs to remove somone from the event registraion. Should this be an option?
    def add_to_waiting_list(self, user):
        # TODO: Adds user to waiting list
        return self.registrations.update_or_create(
            event=self,
            user=user,
            defaults={
                "pool": None,
                "unregistration_date": None
            }
        )[0]

    def bump_from_waiting_list(self):
        # TODO: Take users from waiting list with earliest registration that has the possibility of joining the event
        #       remove them from the waiting list, and add them to the open pool
        pass

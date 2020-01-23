from django.db import models, transaction

from user_profile.models import Profile
from news.models import Event
from groups.models import InheritanceGroup
# Import constants
from constants import *

class Registration(models.Model):

    user = models.ForeignKey(
        Profile,
        related_name="registrations",
        on_delete=models.CASCADE,
    )
    event = models.ForeignKey(
        Event,
        related_name="registrations",
        on_delete=models.CASCADE,
    )
    pool = models.ForeignKey(
        Pool,
        null=True,
        related_name='registrations',
        on_delete=models.CASCADE,
    )

    # Registration data
    registration_date = models.DateTimeField()
    unregistration_date = models.DateTimeField()
    # Extra user data
    feedback = models.CharField(max_length=255, blank=True)
    photo_consent = models.CharField(
        max_length=32,
        default=constants.UNKNOWN,
        choices=constants.PHOTO_CONSENT_CHOICES,
    )

    # Property (Necessary?)
    @property
    def on_waitinglist(self):
        return False

    @property
    def waitinglist_possition(self):
        # TODO
        return 0

    def __str__(self):
        return str(self.user)+"|"+str(self.event)
    
    class Meta:
        unique_together("user", "event")
        ordering = ["registration_date"]

    # Method for seting photo-consent after signup
    def register_to_pole(self, pool):
        allowed=False
        # Use to lock rown until transaction is ower
        with transaction.atomic():
            current_pool = Pool.objects.select_for_update().get(pk=pool.id)
            if current_pool.places == 0 or current_pool.counter < current_pool.places:
                current_pool.increment_counter()
                allowed=True
        if allowed:
            return self.add_to_pool(pool)
        else:
            return self.add_to_waitinglist()
            

    def add_to_pool(self, pool, **kwargs):
        self.set_values(
            pool=pool,
            registration_date=timezone.now(),
            unregistration_date=None,
            **kwargs,
        )
    
    def add_to_waitinglist(self, **kwargs):
        self.set_values(
            pool=None,
            registration_date=timezone.now(),
            unregistration_date=None,
            **kwargs,
        )

    def unregister(self):
        if self.pool:
            # Use to lock rown until transaction is ower
            with transaction.atomic():
                current_pool = Pool.objects.select_for_update().get(pk=self.pool.id)
                current_pool.decrement_counter()
        return self.set_values(
            pool=None,
            unregistration_date=timezone.now(),
        )

    def set_values(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save(update_fields=kwargs.keys())
        return self




class Pool(models.Model):
    places = models.IntegerField(
        # TODO: Allow only positive integers
        default=0,
        min_value=0,
    )
    # Groups with access to this pool
    access_group = models.ForeignKey(
        InheritanceGroup,
        "access_pool",
        on_delete=models.SET_NULL,
        blank=True,
    )
    event = models.ForeignKey(
        Event,
        related_name='pools',
        on_delete=models.CASCADE,
    )
    counter = models.IntegerField(
        default=0,
        min_value=0
    )
    # Date for signup activation
    activation_date = models.DateTimeField()


    @property
    def is_full(self):
        if self.places == 0:
            return False
        return self.registrations.count() >= self.places

    @property
    def places_left(self):
        return self.places - self.registrations.count()

    def is_activated(self):
        return self.activation_date <= timezone.now()

    @property
    def registration_count(self):
        return self.registrations.count()

    def increment_counter(self):
        self.counter += 1
        self.save(update_fields=["counter"])
        return self

    def decrement_counter(self):
        self.counter -= 1
        self.save(update_fields=["counter"])
        return self
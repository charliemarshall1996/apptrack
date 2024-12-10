from django.db import models
from django.dispatch import Signal
from django.utils import timezone

# Create your models here.
target_reset = Signal()


class Streak(models.Model):
    current_streak_start = models.DateTimeField(
        null=True, blank=True, auto_now_add=True)
    current_streak = models.IntegerField(default=0, null=True, blank=True)

    longest_streak_start = models.DateTimeField(null=True, blank=True)
    longest_streak_end = models.DateTimeField(null=True, blank=True)
    longest_streak = models.IntegerField(default=0, null=True, blank=True)

    def increment(self):
        self.current_streak += 1
        self.save()

    def reset(self):
        now = timezone.now()
        if self.current_streak > self.longest_streak:
            self.longest_streak_start = self.current_streak_start
            self.longest_streak_end = now
            self.longest_streak = self.current_streak
        self.current_streak_start = now
        self.current_streak = 0
        self.save()


class Target(models.Model):
    profile = models.OneToOneField(
        'accounts.Profile', on_delete=models.CASCADE, related_name='target')
    target_applications_made = models.IntegerField(default=0)
    current_applications_made = models.IntegerField(default=0)
    total_targets_met = models.IntegerField(default=0)
    streak = models.ForeignKey(
        Streak, on_delete=models.CASCADE, related_name='target', null=True)
    last_reset = models.DateTimeField(auto_now=True)

    @property
    def met(self):
        return self.current_applications_made >= self.target_applications_made

    def reset(self, from_save=False):
        # get now
        now = timezone.now()

        # if there is a target
        if self.target_applications_made > 0:
            if now.date() > self.last_reset.date():
                if self.met:
                    self.total_targets_met += 1
                    self.streak.increment()
                else:
                    self.streak.reset()
                self.current_applications_made = 0
                self.last_reset = now
                target_reset.send(sender=self.__class__, instance=self)
                if not from_save:
                    self.save()

    def increment(self):
        self.current_applications_made += 1
        self.save()

    def decrement(self):
        self.current_applications_made -= 1
        self.save()

    def _reset_if_target_changed(self):
        original = Target.objects.get(pk=self.pk)
        if original:
            if original.target_applications_made != self.target_applications_made:
                self.current_applications_made = 0
                self.last_reset = timezone.now()
                target_reset.send(sender=self.__class__, instance=self)

    def save(self, *args, **kwargs):
        if not self.streak:
            self.streak = Streak()
            self.streak.save()
        self._reset_if_target_changed()
        self.reset(from_save=True)
        super().save(*args, **kwargs)

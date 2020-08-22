from django.db import models

from iow.apps.core.models import Base


class Discount(Base):
    begins_at = models.DateTimeField(null=True)
    ends_at = models.DateTimeField(null=True)
    percentage = models.IntegerField(default=10)
    code = models.CharField(max_length=10)

    def __str__(self):
        return 'Discount %s -> %s: %s' % (
            self.begins_at, self.ends_at, self.percentage
        )

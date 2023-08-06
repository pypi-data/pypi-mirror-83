from django.db import models
from dj_pony.hashedfield.fields import BinaryHashedField, EncodedHashedField
import sentinel


UseHashValue = sentinel.create("UseHashedValueInstead")


class HashingQueryset(models.QuerySet):
    def get_or_create(self, defaults=None, **kwargs):
        """
        Look up an object with the given kwargs, creating one if necessary.
        Return a tuple of (object, created), where created is a boolean
        specifying whether an object was created.
        """
        # The get() needs to be targeted at the write database in order
        # to avoid potential transaction consistency problems.
        self._for_write = True
        for _k, _v in kwargs.items():
            if _v is UseHashValue:
                for field in self.model._meta.get_fields():
                    if isinstance(field, (BinaryHashedField, EncodedHashedField)):
                        field_name = field.attname
                        if _k == field_name:
                            field.compute_hashed_value(self.model)
                            kwargs[_k] = field.value_from_object(self.model)
        try:
            return self.get(**kwargs), False
        except self.model.DoesNotExist:
            params = self._extract_model_params(defaults, **kwargs)
            return self._create_object_from_params(kwargs, params)
        # return super(PreHashManager, self).get_or_create(defaults=None, **kwargs)


class PreHashManager(models.Manager):
    def get_queryset(self):
        return HashingQueryset(model=self.model, using=self._db, hints=self._hints)



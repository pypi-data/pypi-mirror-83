from dj_pony.hashedfield.fields import BinaryHashedField, EncodedHashedField


class PreHashMixin:
    '''Mixin to precalculate the hashed fields on a model for easier use with unique indexes.'''
    def calculate_hashes(self):
        for field in self._meta.fields:
            if isinstance(field, (BinaryHashedField, EncodedHashedField)):
                field.compute_hashed_value(self)



import hashlib
import base64
from django.db import models
from typing import Callable
from enum import Flag, auto


def no_encoding(data: bytes) -> bytes:
    return data


class DjangoFieldType(Flag):
    BinaryField = auto()
    CharField = auto()


class Encoding(Flag):
    Base16 = auto()  # binascii.b2a_hex / binascii.a2b_hex
    Base32 = auto()  # base64.b32encode / base64.b32decode
    # Base36 = auto()
    # Base58 = auto()
    # Base62 = auto()
    Base64 = auto()  # base64.standard_b64encode / base64.standard_b64decode
    UrlSafeBase64 = auto()  # base64.urlsafe_b64encode / base64.urlsafe_b64decode
    Ascii85 = auto()  # base64.a85encode / base64.a85decode
    Base85 = auto()  # base64.b85encode / base64.b85decode


class Hash(Flag):
    SHA1 = auto()
    SHA2_256 = auto()
    SHA2_512 = auto()
    SHA3_256 = auto()
    SHA3_512 = auto()


BINARY_HASH_FIELD_CONFIG = {
    Hash.SHA1: {"max_length": 160, "hash_func": hashlib.sha1},
    Hash.SHA2_256: {"max_length": 256, "hash_func": hashlib.sha256},
    Hash.SHA2_512: {"max_length": 512, "hash_func": hashlib.sha512},
    Hash.SHA3_256: {"max_length": 256, "hash_func": hashlib.sha3_256},
    Hash.SHA3_512: {"max_length": 512, "hash_func": hashlib.sha3_512},
}

ENCODED_HASH_FIELD_CONFIG = {
    Hash.SHA1: {
        Encoding.Base16: {
            "max_length": 40,
            "hash_func": hashlib.sha1,
            "encoding_func": base64.b16encode,
        },
        Encoding.Base32: {
            "max_length": 32,
            "hash_func": hashlib.sha1,
            "encoding_func": base64.b32encode,
        },
        Encoding.Base64: {
            "max_length": 28,
            "hash_func": hashlib.sha1,
            "encoding_func": base64.standard_b64encode,
        },
        Encoding.UrlSafeBase64: {
            "max_length": 28,
            "hash_func": hashlib.sha1,
            "encoding_func": base64.urlsafe_b64encode,
        },
        Encoding.Ascii85: {
            "max_length": 25,
            "hash_func": hashlib.sha1,
            "encoding_func": base64.a85encode,
        },
        Encoding.Base85: {
            "max_length": 25,
            "hash_func": hashlib.sha1,
            "encoding_func": base64.b85encode,
        },
    },
    Hash.SHA2_256: {
        Encoding.Base16: {
            "max_length": 64,
            "hash_func": hashlib.sha256,
            "encoding_func": base64.b16encode,
        },
        Encoding.Base32: {
            "max_length": 56,
            "hash_func": hashlib.sha256,
            "encoding_func": base64.b32encode,
        },
        Encoding.Base64: {
            "max_length": 44,
            "hash_func": hashlib.sha256,
            "encoding_func": base64.standard_b64encode,
        },
        Encoding.UrlSafeBase64: {
            "max_length": 44,
            "hash_func": hashlib.sha256,
            "encoding_func": base64.urlsafe_b64encode,
        },
        Encoding.Ascii85: {
            "max_length": 40,
            "hash_func": hashlib.sha256,
            "encoding_func": base64.a85encode,
        },
        Encoding.Base85: {
            "max_length": 40,
            "hash_func": hashlib.sha256,
            "encoding_func": base64.b85encode,
        },
    },
    Hash.SHA2_512: {
        Encoding.Base16: {
            "max_length": 128,
            "hash_func": hashlib.sha512,
            "encoding_func": base64.b16encode,
        },
        Encoding.Base32: {
            "max_length": 104,
            "hash_func": hashlib.sha512,
            "encoding_func": base64.b32encode,
        },
        Encoding.Base64: {
            "max_length": 88,
            "hash_func": hashlib.sha512,
            "encoding_func": base64.standard_b64encode,
        },
        Encoding.UrlSafeBase64: {
            "max_length": 88,
            "hash_func": hashlib.sha512,
            "encoding_func": base64.urlsafe_b64encode,
        },
        Encoding.Ascii85: {
            "max_length": 80,
            "hash_func": hashlib.sha512,
            "encoding_func": base64.a85encode,
        },
        Encoding.Base85: {
            "max_length": 80,
            "hash_func": hashlib.sha512,
            "encoding_func": base64.b85encode,
        },
    },
    Hash.SHA3_256: {
        Encoding.Base16: {
            "max_length": 64,
            "hash_func": hashlib.sha3_256,
            "encoding_func": base64.b16encode,
        },
        Encoding.Base32: {
            "max_length": 56,
            "hash_func": hashlib.sha3_256,
            "encoding_func": base64.b32encode,
        },
        Encoding.Base64: {
            "max_length": 44,
            "hash_func": hashlib.sha3_256,
            "encoding_func": base64.standard_b64encode,
        },
        Encoding.UrlSafeBase64: {
            "max_length": 44,
            "hash_func": hashlib.sha3_256,
            "encoding_func": base64.urlsafe_b64encode,
        },
        Encoding.Ascii85: {
            "max_length": 40,
            "hash_func": hashlib.sha3_256,
            "encoding_func": base64.a85encode,
        },
        Encoding.Base85: {
            "max_length": 40,
            "hash_func": hashlib.sha3_256,
            "encoding_func": base64.b85encode,
        },
    },
    Hash.SHA3_512: {
        Encoding.Base16: {
            "max_length": 128,
            "hash_func": hashlib.sha3_512,
            "encoding_func": base64.b16encode,
        },
        Encoding.Base32: {
            "max_length": 104,
            "hash_func": hashlib.sha3_512,
            "encoding_func": base64.b32encode,
        },
        Encoding.Base64: {
            "max_length": 88,
            "hash_func": hashlib.sha3_512,
            "encoding_func": base64.standard_b64encode,
        },
        Encoding.UrlSafeBase64: {
            "max_length": 88,
            "hash_func": hashlib.sha3_512,
            "encoding_func": base64.urlsafe_b64encode,
        },
        Encoding.Ascii85: {
            "max_length": 80,
            "hash_func": hashlib.sha3_512,
            "encoding_func": base64.a85encode,
        },
        Encoding.Base85: {
            "max_length": 80,
            "hash_func": hashlib.sha3_512,
            "encoding_func": base64.b85encode,
        },
    },
}


class HashedBinaryField(models.BinaryField):
    description = "Hash another field on this model and store the result in BinaryField."

    def __init__(self, *args, original_field_name, selected_hash_function, **kwargs):
        """
        :param original: name of the field storing the value to be hashed
        @keyword original_field_name: The name of the original field to hash the value of.
        """
        self.original_field_name: str = original_field_name
        self.selected_hash_function: Hash = selected_hash_function
        self.max_length: int = BINARY_HASH_FIELD_CONFIG[self.selected_hash_function]["max_length"]
        self.hash_function: Callable = BINARY_HASH_FIELD_CONFIG[self.selected_hash_function]["hash_func"]
        self.blank = kwargs["blank"] if "blank" in kwargs else False
        self.null = kwargs["null"] if "null" in kwargs else False
        self.editable = False
        kwargs["max_length"] = self.max_length
        kwargs["editable"] = self.editable
        super(HashedBinaryField, self).__init__(*args, **kwargs)

    # TODO: Put a layer in here to ensure that both fields have the same null and blank values.
    #  I can't make this automatic as the field gets instantiated without the model at one point.
    # @property
    # def null(self):
    #     if hasattr('model', self):
    #         # noinspection PyProtectedMember
    #         original_field: models.Field = next(
    #             __field for __field in self.model._meta.fields if __field.attname == self.original_field_name
    #         )
    #         if self.null != original_field.null:
    #             raise RuntimeError("")
    #     else:
    #         return self.null
    #
    # @null.setter
    # def null(self, value):
    #     print(f"Throwing away a value passed to {__name__}. Value was: '{value}'")
    #
    # @property
    # def blank(self):
    #     return self.original_field.blank
    #
    # @blank.setter
    # def blank(self, value):
    #     return print(f"Throwing away a value passed to {__name__}. Value was: '{value}'")
    #
    # def clone(self):
    #     return super(HashedBinaryField, self).clone()
    #     # """
    #     # Uses deconstruct() to clone a new copy of this Field.
    #     # Will not preserve any class attachments/attribute names.
    #     # """
    #     # name, path, args, kwargs = self.deconstruct()
    #     # return self.__class__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for superfluous_keyword_argument in ["max_length", "editable"]:
            if superfluous_keyword_argument in kwargs:
                del kwargs[superfluous_keyword_argument]
        kwargs["original_field_name"] = self.original_field_name
        kwargs["selected_hash_function"] = self.selected_hash_function
        return name, path, args, kwargs

    def pre_save(self, model_instance: models.Model, add):
        original_value: models.Field = getattr(model_instance, self.original_field_name)
        original_bytes: bytes = str(original_value).encode("utf-8")
        hashed_value: bytes = self.hash_function(original_bytes).digest()
        setattr(model_instance, self.attname, hashed_value)
        return super(HashedBinaryField, self).pre_save(model_instance, add)


class EncodedHashedField(models.CharField):
    description = "Hash another field on this model and store the encoded result in a CharField."

    def __init__(self, *args, original_field_name, hash_with, encode_as, **kwargs):
        """
        :param original: name of the field storing the value to be hashed
        """
        self.original_field_name: str = original_field_name
        self.hash_enum: Hash = hash_with
        self.encoding_enum: Encoding = encode_as
        config = ENCODED_HASH_FIELD_CONFIG.get(self.hash_enum, {}).get(self.encoding_enum, None)
        if config is None:
            raise RuntimeError

        self.max_length: int = config["max_length"]
        self.encoding_function = config["encoding_func"]
        self.hash_function = config["hash_func"]
        self.blank = kwargs["blank"] if "blank" in kwargs else False
        self.null = kwargs["null"] if "null" in kwargs else False
        self.editable = False
        kwargs["max_length"] = self.max_length
        kwargs["editable"] = self.editable
        super(EncodedHashedField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for superfluous_keyword_argument in ["max_length", "editable"]:
            if superfluous_keyword_argument in kwargs:
                del kwargs[superfluous_keyword_argument]
        kwargs["original_field_name"] = self.original_field_name
        kwargs["hash_with"] = self.hash_enum
        kwargs["encode_as"] = self.encoding_enum
        return name, path, args, kwargs

    def pre_save(self, model_instance: models.Model, add):
        original_value: models.Field = getattr(model_instance, self.original_field_name)
        original_bytes: bytes = str(original_value).encode("utf-8")
        hash_bytes: bytes = self.hash_function(original_bytes).digest()
        encoded_bytes = self.encoding_function(hash_bytes).decode("utf-8")
        setattr(model_instance, self.attname, encoded_bytes)
        return super(EncodedHashedField, self).pre_save(model_instance, add)

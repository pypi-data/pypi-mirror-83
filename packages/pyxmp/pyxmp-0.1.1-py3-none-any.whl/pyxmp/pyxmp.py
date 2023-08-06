import logging

import pyexiv2


logger = logging.getLogger(__name__)


def read(img_bytes: bytes):
    meta = pyexiv2.ImageMetadata.from_buffer(img_bytes)
    meta.read()

    xmp_dict = {}
    for key in meta.xmp_keys:
        xmp_dict[key] = meta[key].raw_value
    pyexiv2.xmp.closeXmpParser()
    return xmp_dict


def inject(
    img_bytes: bytes,
    metadata,
    namespace_name: str,
    namespace_prefix: str
):
    meta = pyexiv2.ImageMetadata.from_buffer(img_bytes)
    meta.read()

    try:
        pyexiv2.xmp.register_namespace(namespace_name, namespace_prefix)
    except KeyError as e:
        logger.warning(e)
    except ValueError:
        raise

    for info in metadata:
        key_prefix = f'Xmp.{namespace_prefix}'
        provider = _to_camel_case(info.get('provider'))
        name = _to_camel_case(info.get('name'))
        xmp_key = '.'.join([key_prefix, provider, name])
        meta[xmp_key] = info['value']
        meta.write()
    pyexiv2.xmp.closeXmpParser()
    return meta.buffer


def _flatten_to_xmp_format(src: dict, target: dict, xmp_key: str) -> dict:
    for key, val in src.items():
        new_xmp_key = _xmp_key_join(xmp_key, _to_camel_case(key))
        if isinstance(val, dict):
            target = _flatten_to_xmp_format(val, target, new_xmp_key)
        else:
            target[new_xmp_key] = val
    return target


def _to_camel_case(s: str) -> str:
    # Make each word starts with captital
    s = " ".join(w[0].upper() + w[1:] for w in s.split())
    # Make the first character lower case
    s = s[0].lower() + s[1:]
    return s.replace(' ', '')


def _xmp_key_join(key: str, suffix: str) -> str:
    return '.'.join([key, _to_camel_case(suffix)])

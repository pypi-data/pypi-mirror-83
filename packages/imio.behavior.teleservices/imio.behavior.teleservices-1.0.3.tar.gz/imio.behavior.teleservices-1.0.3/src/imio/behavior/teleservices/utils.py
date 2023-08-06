# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import base64
import datetime
import hashlib
import hmac
import random
import urllib
import urlparse


def sign_url(url, key, orig, algo="sha256", timestamp=None, nonce=None):
    parsed = urlparse.urlparse(url)
    new_query = sign_query(parsed.query, key, orig, algo, timestamp, nonce)
    return urlparse.urlunparse(parsed[:4] + (new_query,) + parsed[5:])


def sign_query(query, key, orig, algo="sha256", timestamp=None, nonce=None):
    if timestamp is None:
        timestamp = datetime.datetime.utcnow()
    timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    if nonce is None:
        nonce = hex(random.getrandbits(128))[2:-1]
    new_query = query
    if new_query:
        new_query += "&"
    new_query += urllib.urlencode(
        (("algo", algo), ("orig", orig), ("timestamp", timestamp), ("nonce", nonce))
    )
    signature = base64.b64encode(sign_string(new_query, str(key), algo=algo))
    new_query += "&signature=" + urllib.quote(signature)
    return new_query


def sign_string(s, key, algo="sha256", timedelta=30):
    digestmod = getattr(hashlib, algo)
    hash = hmac.HMAC(key, digestmod=digestmod, msg=s)
    return hash.digest()


def add_behavior(type_name, behavior_name):
    """Add a behavior to a type"""
    fti = queryUtility(IDexterityFTI, name=type_name)
    if not fti:
        return
    behaviors = list(fti.behaviors)
    if behavior_name not in behaviors:
        behaviors.append(behavior_name)
        fti._updateProperty("behaviors", tuple(behaviors))

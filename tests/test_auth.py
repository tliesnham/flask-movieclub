import pytest
from flask import g, session
from movieclub.db import get_db


def test_register(client, app)
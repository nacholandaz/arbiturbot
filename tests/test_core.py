import os
import sys
from datetime import datetime
sys.path.append(".")
import core

message = {
    'created_at': datetime.now(),
    'user_id': "528117649489@c.us",
    'text': "Como hacer para comprar un depa",
}

def test_recieve_message(mocker):
    mocker.patch("core.move_conversation", return_value=True)
    result = core.recieve_message(message)
    expected = True
    assert result == expected
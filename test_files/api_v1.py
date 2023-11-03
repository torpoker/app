MOCKED_ACCOUNT_RESPONSE = {}
# Mock-Antwort für den Beitrittsbestätigungs-POST-Request
MOCKED_CONFIRM_RESPONSE = {
    'table': 27
}

MOCKED_TABLES_RESPONSE = {
    'tables': [
        {'id': 27, 'name': 'Mercury', 'sb': 1, 'bb': 2, 'online': 0, 'seats': 6},
        {'id': 28, 'name': 'Venus', 'sb': 1, 'bb': 2, 'online': 0, 'seats': 6},
        {'id': 29, 'name': 'Earth', 'sb': 2, 'bb': 4, 'online': 0, 'seats': 6},
        {'id': 30, 'name': 'Mars', 'sb': 5, 'bb': 10, 'online': 0, 'seats': 6},
        {'id': 31, 'name': 'Jupiter', 'sb': 10, 'bb': 20, 'online': 0, 'seats': 6},
        {'id': 32, 'name': 'Saturn', 'sb': 20, 'bb': 40, 'online': 0, 'seats': 6},
        {'id': 33, 'name': 'Uranus', 'sb': 40, 'bb': 80, 'online': 0, 'seats': 6},
        {'id': 34, 'name': 'Neptune', 'sb': 100, 'bb': 200, 'online': 0, 'seats': 6}
    ],
    'unit': 'mXMR',
    'currency': 'monero',
    'mindeposit': '0.03'
}


MOCKED_ACCOUNT_INFO_RESPONSE = {
    'account': {'name': 'anonymous', 'stack': 30}
}

MOCKED_SEND_COMPLETED_RESPONSE = {
    'status': 'completed'
}

MOCKED_SEND_POST_RESPONSE = {
    'address': 'xxx111'
}

MOCKED_JOIN_TABLE_RESPONSE = {
    'table': 27,
    'min': 30,
    'max': 200,
    'redirect': False
}


# Mock-Antwort für GET-Request zum Abrufen des aktuellen Tischzustands
MOCKED_TABLE_STATE_RESPONSE = {
    'data': {
        'table': 27,
        'maxtime': 120,
        'board': ['', '', '', '', ''],
        'maxbet': 2,
        'pot': 3,
        'result': None,
        'players': {
            '1': {
                'name': 'anonymous',
                'stack': 29,
                'position': 1,
                'button': True,
                'bet': 1,
                'card1': 'AP',
                'card2': '8K',
                'turn': True,
                'timer': 1698762519,
                'timeleft': 99,
                'timeleftSec': 119
            },
            '2': {
                'name': 'anonymous',
                'stack': 28,
                'position': 2,
                'button': False,
                'bet': 2,
                'card1': 'back',
                'card2': 'back',
                'turn': False,
                'timer': 0
            }
        },
        'myturn': True,
        'mybet': 1,
        'mystack': 29
    },
    'messages': []
}
#---------------------------------------------

# Mock-Antwort für den Call-POST-Request
MOCKED_CALL_RESPONSE = {
    'table': 27
}

# Mock-Antwort für den GET-Request nach dem Call-Button-Klick
MOCKED_TABLE_STATE_AFTER_CALL_RESPONSE = {
    'data': {
        'table': 27,
        'maxtime': 120,
        'board': ['', '', '', '', ''],
        'maxbet': 2,
        'pot': 4,
        'result': None,
        'players': {
            '1': {
                'name': 'anonymous',
                'stack': 28,
                'position': 1,
                'button': True,
                'bet': 2,
                'card1': 'AP',
                'card2': '8K',
                'turn': False,
                'timer': 0
            },
            '2': {
                'name': 'anonymous',
                'stack': 28,
                'position': 2,
                'button': False,
                'bet': 2,
                'card1': 'back',
                'card2': 'back',
                'turn': True,
                'timer': 1698762584,
                'timeleft': 99,
                'timeleftSec': 119
            }
        },
        'myturn': False,
        'mybet': 2,
        'mystack': 28
    },
    'messages': []
}

#State after Oponent checks too
MOCKED_TABLE_STATE_AFTER_ENEMY_CHECK_RESPONSE = {
    'data': {
        'table': 27,
        'maxtime': 120,
        'board': ['3T', '8T', 'DC', '', ''],
        'maxbet': 0,
        'pot': 4,
        'result': None,
        'players': {
            '1': {'name': 'anonymous', 'stack': 28, 'position': 1, 'button': True, 'bet': 0, 'card1': 'AP', 'card2': '8K', 'turn': False, 'timer': 0},
            '2': {'name': 'anonymous', 'stack': 28, 'position': 2, 'button': False, 'bet': 0, 'card1': 'back', 'card2': 'back', 'turn': True, 'timer': 1698762625, 'timeleft': 87, 'timeleftSec': 105}
        },
        'myturn': False,
        'mybet': 0,
        'mystack': 28
    },
    'messages': []
}

#----------------------------------flop------------------------
#Oponent check
MOCKED_TABLE_STATE_AFTER_FLOP_RESPONSE = {
    'data': {
        'table': 27,
        'maxtime': 120,
        'board': ['3T', '8T', 'DC', '', ''],
        'maxbet': 0,
        'pot': 4,
        'result': None,
        'players': {
            '1': {'name': 'anonymous', 'stack': 28, 'position': 1, 'button': True, 'bet': 0, 'card1': 'AP', 'card2': '8K', 'turn': True, 'timer': 1698762687, 'timeleft': 89, 'timeleftSec': 107},
            '2': {'name': 'anonymous', 'stack': 28, 'position': 2, 'button': False, 'bet': 0, 'card1': 'back', 'card2': 'back', 'turn': False, 'timer': 0}
        },
        'myturn': True,
        'mybet': 0,
        'mystack': 28
    },
    'messages': []
}

#check
MOCKED_CHECK_RESPONSE = {'table': 27}


MOCKED_TABLE_STATE_AFTER_TURN_RESPONSE = {
    'data': {
        'table': 27,
        'maxtime': 120,
        'board': ['3T', '8T', 'DC', 'VT', ''],
        'maxbet': 0,
        'pot': 4,
        'result': None,
        'players': {
            '1': {'name': 'anonymous', 'stack': 28, 'position': 1, 'button': True, 'bet': 0, 'card1': 'AP', 'card2': '8K', 'turn': False, 'timer': 0},
            '2': {'name': 'anonymous', 'stack': 28, 'position': 2, 'button': False, 'bet': 0, 'card1': 'back', 'card2': 'back', 'turn': True, 'timer': 1698762714, 'timeleft': 99, 'timeleftSec': 119}
        },
        'myturn': False,
        'mybet': 0,
        'mystack': 28
    },
    'messages': []
}

#------------------------------Turn-----------------------------
MOCKED_TABLE_STATE_AFTER_OPPONENT_CHECK_TURN = {
    'data': {
        'table': 27,
        'maxtime': 120,
        'board': ['3T', '8T', 'DC', 'VT', ''],
        'maxbet': 0,
        'pot': 4,
        'result': None,
        'players': {
            '1': {
                'name': 'anonymous', 'stack': 28, 'position': 1, 'button': True,
                'bet': 0, 'card1': 'AP', 'card2': '8K',
                'turn': True, 'timer': 1698762736, 'timeleft': 80, 'timeleftSec': 96
            },
            '2': {
                'name': 'anonymous', 'stack': 28, 'position': 2, 'button': False,
                'bet': 0, 'card1': 'back', 'card2': 'back', 'turn': False, 'timer': 0
            }
        },
        'myturn': True,
        'mybet': 0,
        'mystack': 28
    },
    'messages': []
}

MOCKED_TABLE_STATE_AFTER_RAISE = {
    'data': {
        'table': 27,
        'maxtime': 120,
        'board': ['3T', '8T', 'DC', 'VT', ''],
        'maxbet': 2,
        'pot': 6,
        'result': None,
        'players': {
            '1': {
                'name': 'anonymous', 'stack': 26, 'position': 1, 'button': True,
                'bet': 2, 'card1': 'AP', 'card2': '8K',
                'turn': False, 'timer': 0
            },
            '2': {
                'name': 'anonymous', 'stack': 28, 'position': 2, 'button': False,
                'bet': 0, 'card1': 'back', 'card2': 'back', 'turn': True, 'timer': 1698762763,
                'timeleft': 99, 'timeleftSec': 119
            }
        },
        'myturn': False,
        'mybet': 2,
        'mystack': 26
    },
    'messages': []
}

MOCKED_TABLE_STATE_AFTER_OPPONENT_CALL = {
    'data': {
        'table': 27,
        'maxtime': 120,
        'board': ['3T', '8T', 'DC', 'VT', '9P'],
        'maxbet': 0,
        'pot': 8,
        'result': None,
        'players': {
            '1': {
                'name': 'anonymous', 'stack': 26, 'position': 1, 'button': True,
                'bet': 0, 'card1': 'AP', 'card2': '8K',
                'turn': True, 'timer': 1698762811,
                'timeleft': 91, 'timeleftSec': 110
            },
            '2': {
                'name': 'anonymous', 'stack': 26, 'position': 2, 'button': False,
                'bet': 0, 'card1': 'back', 'card2': 'back', 'turn': False, 'timer': 0
            }
        },
        'myturn': True,
        'mybet': 0,
        'mystack': 26
    },
    'messages': []
}





#--------------------------New Table-----------------------

MOCKED_TABLE_STATE_NEW_ROUND = {
    'data': {
        'table': 27,
        'maxtime': 120,
        'board': ['', '', '', '', ''],
        'maxbet': 2,
        'pot': 3,
        'result': None,
        'players': {
            '1': {
                'name': 'anonymous',
                'stack': 24,
                'position': 1,
                'button': False,
                'bet': 2,
                'card1': 'VC',
                'card2': '5T',
                'turn': False,
                'timer': 0
            },
            '2': {
                'name': 'anonymous',
                'stack': 33,
                'position': 2,
                'button': True,
                'bet': 1,
                'card1': 'back',
                'card2': 'back',
                'turn': True,
                'timer': 1698762839,
                'timeleft': 89,
                'timeleftSec': 107
            }
        },
        'myturn': False,
        'mybet': 2,
        'mystack': 24
    },
    'messages': []
}

#-------------------------logging out-------------------------

MOCKED_QUIT_TABLE_RESPONSE = {}

MOCKED_ACCOUNT_RESPONSE_AFTER_LEAVE = {
    'account': {
        'name': 'anonymous',
        'stack': 25
    }
}

MOCKED_CASHOUT_RESPONSE = {}


#---------------------chat--------------------------------


MOCKED_TABLE_STATUS_AFTER_MESSAGE = {
    'data': {
        'table': 27,
        'players': {
            '1': {
                'name': 'anonymous',
                'stack': 30,
                'position': 1
            }
        },
        'mystack': 30
    },
    'messages': [
        {
            'name': 'anonymous',
            'message': 'im out',
            'timer': 1698787398
        }
    ]
}

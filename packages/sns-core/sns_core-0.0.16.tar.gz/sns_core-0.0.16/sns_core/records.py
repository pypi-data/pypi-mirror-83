from os.path import expanduser, isdir, isfile
from os import mkdir, mknod, path, makedirs
import json
import sqlite3
from datetime import datetime
from dataclasses import dataclass

from .exceptions import SNSrecordException
from .utils import SingletonMeta, SNS_RECORD_PATH
from . import requests

def register_user(identifier, phone_number):
    # write to file
    if not isdir(expanduser(SNS_RECORD_PATH)):
        makedirs(expanduser(SNS_RECORD_PATH))

    if not isfile(expanduser(SNS_RECORD_PATH) + '/user_record.dat'):
        response = requests.user("create", 'server:0.0.0.0', from_='user:' + identifier, PublicKey='test', PhoneNumber=phone_number)[0]

        if response.action == '500':
            return False

        this_user = UserRecord(-1, response.get('From').split(":")[1], {key: value for key, value in response.headers.items() if 'Key' in key}, response.get('FollowerCount'), response.get('FollowingCount'), response.get('PostCount'), response.get('ReactionCount'))
 
        user_file = open(expanduser(SNS_RECORD_PATH) + '/user_record.dat', 'w')
        json.dump(this_user.toMap(), user_file)
        user_file.close()
    else:
        raise SNSrecordException('User is already registered')

    try:
        register_SNSrecords()
        return True
    except:
        return False

class SNSrecord(metaclass=SingletonMeta):
    def __init__(self, this_user=None, database=None):
        if this_user == None or database == None:
            try:
                if not self.this_user:
                    pass
            except:
                raise SNSrecordException('Record is not initialized')
        else: 
            self.this_user = this_user
            self.database = database
            self.circles = ['private', 'direct', 'group']

    def _check_circle(self, circle):
        if not circle.lower() in self.circles:
            raise SNSrecordException('This circle does not exist')

@dataclass
class UserRecord:
    id: int
    identifier: str
    keys: dict
    follower_count: int
    following_count: int
    post_count: int
    reaction_count: int

    def toMap(self) -> dict:
        return {
            'identifier':self.identifier,
            'keys':json.dumps(self.keys),
            'follower_count':self.follower_count,
            'following_count':self.following_count,
            'post_count':self.post_count,
            'reaction_count':self.reaction_count
        }

@dataclass
class GroupRecord:
    id: int
    identifier: str
    keys: dict
    owners: list
    members: list
    visibility: str
    post_count: int
    reaction_count: int

    def toMap(self) -> dict:
        return {
            'identifier':self.identifier,
            'keys':json.dumps(self.keys),
            'owners':json.dumps(self.owners),
            'members':json.dumps(self.members),
            'visibility':self.visibility,
            'post_count':self.post_count,
            'reaction_count':self.reaction_count
        }

@dataclass
class MessageRecord:
    id: int
    circle: str
    identifier: str
    created_at: datetime
    updated_at: datetime
    content: dict

    def toMap(self) -> dict:
        return {
            'identifier':self.identifier,
            'created_at':int(self.created_at.timestamp() * 1000000),
            'updated_at':int(self.updated_at.timestamp() * 1000000),
            'content':json.dumps(self.content)
        }

@dataclass
class PrivateMessageRecord:

    def toMap(self) -> dict:
        return {
            'identifier':self.identifier,
            'created_at':int(self.created_at.timestamp() * 1000000),
            'updated_at':int(self.updated_at.timestamp() * 1000000),
            'content':json.dumps(self.content)
        }

@dataclass
class DirectMessageRecord:
    user_identifier: str
    is_from: bool

    def toMap(self) -> dict:
        return {
            'identifier':self.identifier,
            'user_identifier':self.user_identifier,
            'from':1 if is_from else 0,
            'created_at':int(self.created_at.timestamp() * 1000000),
            'updated_at':int(self.updated_at.timestamp() * 1000000),
            'content':json.dumps(self.content)
        }

@dataclass
class GroupMessageRecord:
    user_identifier: str
    group_identifier: str

    def toMap(self) -> dict:
        return {
            'identifier':self.identifier,
            'user_identifier':self.user_identifier,
            'group_identifier':self.group_identifier,
            'created_at':int(self.created_at.timestamp() * 1000000),
            'updated_at':int(self.updated_at.timestamp() * 1000000),
            'content':json.dumps(self.content)
        }

def register_SNSrecords():
    global _SNSrecordInstance

    if (not path.isfile(expanduser(SNS_RECORD_PATH) + '/user_record.dat')):
        raise SNSrecordException('The user record file does not exist, indicating this user is not registered')

    file_result = json.load(open(expanduser(SNS_RECORD_PATH) + '/user_record.dat'))

    try:
        _this_user = UserRecord(-1, file_result['identifier'], json.loads(file_result['keys']), 
            file_result['follower_count'], file_result['following_count'],
            file_result['post_count'], file_result['reaction_count'])
    except Exception as e:
        print(e)
        raise SNSrecordException('Missing record item')

    _database = sqlite3.connect(expanduser(SNS_RECORD_PATH) + '/sns_records.db')
    _database.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, identifier TEXT UNIQUE, keys TEXT, follower_count INT, following_count INT, post_count INT, reaction_count INT)')
    _database.execute('CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY AUTOINCREMENT, identifier TEXT UNIQUE, keys TEXT, owners TEXT, members TEXT, visibility TEXT, post_count INT, reaction_count INT)')
    _database.execute('CREATE TABLE IF NOT EXISTS private (id INTEGER PRIMARY KEY AUTOINCREMENT, identifier TEXT UNIQUE, created_at INT, updated_at INT, content TEXT)')
    _database.execute('CREATE TABLE IF NOT EXISTS direct (id INTEGER PRIMARY KEY AUTOINCREMENT, identifier TEXT UNIQUE, user_identifier TEXT, [from] INT, created_at INT, updated_at INT, content TEXT)')
    _database.execute('CREATE TABLE IF NOT EXISTS [group] (id INTEGER PRIMARY KEY AUTOINCREMENT, identifier TEXT UNIQUE, user_identifier TEXT, group_identifier TEXT, created_at INT, updated_at INT, content TEXT)')

    SNSrecord(_this_user, _database)
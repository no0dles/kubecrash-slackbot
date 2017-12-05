import pickle
import os
from src.settings import STORE_LIMIT, STORE_FILE


class EventStore(object):
    def __init__(self):
        self.uids = []
        if os.path.isfile(STORE_FILE):
            with open(STORE_FILE, 'rb') as file:
                try:
                    self.uids.extend(pickle.load(file))
                except EOFError:
                    pass

    def contains(self, uid: str):
        for existing_uid in reversed(self.uids):
            if existing_uid == uid:
                return True
        return False

    def store(self, uid: str):
        self.uids.append(uid)
        if len(self.uids) > STORE_LIMIT:
            self.uids.pop(0)
        with open(STORE_FILE, 'wb') as file:
            pickle.dump(self.uids, file)

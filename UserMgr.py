# Copyright 2017 Michael J Simms

import bcrypt
import Keys
import SessionMgr
import StraenDb


MIN_PASSWORD_LEN  = 8

class UserMgr(object):
    """Class for managing users"""

    def __init__(self, session_mgr, root_dir):
        self.database = StraenDb.MongoDatabase(root_dir)
        self.database.connect()
        self.session_mgr = session_mgr
        super(UserMgr, self).__init__()

    def terminate(self):
        """Destructor"""
        self.database = None

    def get_logged_in_user(self):
        """Returns the username associated with the current session."""
        return self.session_mgr.get_logged_in_user()

    def get_logged_in_user_from_cookie(self, auth_cookie):
        """Returns the username associated with the specified authentication cookie."""
        return self.session_mgr.get_logged_in_user_from_cookie(auth_cookie)

    def create_new_session(self, username):
        """Starts a new session."""
        return self.session_mgr.create_new_session(username)

    def clear_session(self):
        """Ends the current session."""
        self.session_mgr.clear_session()

    def authenticate_user(self, email, password):
        """Validates a user against the credentials in the database."""
        if self.database is None:
            raise Exception("No database.")
        if len(email) == 0:
            raise Exception("An email address not provided.")
        if len(password) < MIN_PASSWORD_LEN:
            raise Exception("The password is too short.")

        _, db_hash1, _ = self.database.retrieve_user(email)
        if db_hash1 is None:
            raise Exception("The user could not be found.")
        db_hash2 = bcrypt.hashpw(password.encode('utf-8'), db_hash1.encode('utf-8'))
        if db_hash1 != db_hash2:
            raise Exception("The password is invalid.")
        return True

    def create_user(self, email, realname, password1, password2, device_str):
        """Adds a user to the database."""
        if self.database is None:
            raise Exception("No database.")
        if len(email) == 0:
            raise Exception("An email address not provided.")
        if len(realname) == 0:
            raise Exception("Name not provided.")
        if len(password1) < MIN_PASSWORD_LEN:
            raise Exception("The password is too short.")
        if password1 != password2:
            raise Exception("The passwords do not match.")
        if self.database.retrieve_user(email) is None:
            raise Exception("The user already exists.")

        salt = bcrypt.gensalt()
        computed_hash = bcrypt.hashpw(password1.encode('utf-8'), salt)
        if not self.database.create_user(email, realname, computed_hash):
            raise Exception("An internal error was encountered when creating the user.")

        if len(device_str) > 0:
            user_id, _, _ = self.database.retrieve_user(email)
            self.database.create_user_device(user_id, device_str)
        return True

    def retrieve_user(self, email):
        """Retrieve method for a user."""
        if self.database is None:
            raise Exception("No database.")
        if email is None or len(email) == 0:
            raise Exception("Bad parameter.")
        return self.database.retrieve_user(email)

    def retrieve_user_from_id(self, user_id):
        """Retrieve method for a user."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None:
            raise Exception("Bad parameter.")
        return self.database.retrieve_user_from_id(user_id)

    def retrieve_matched_users(self, name):
        """Returns a list of user names for users that match the specified regex."""
        if self.database is None:
            raise Exception("No database.")
        if name is None or len(name) == 0:
            raise Exception("Bad parameter.")
        return self.database.retrieve_matched_users(name)

    def update_user_email(self, user_id, email, realname):
        """Updates a user's database entry."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None:
            raise Exception("Unexpected empty object: user_id.")
        if len(email) == 0:
            raise Exception("Email address not provided.")
        if len(realname) == 0:
            raise Exception("Name not provided.")

        if not self.database.update_user(user_id, email, realname, None):
            raise Exception("An internal error was encountered when updating the user.")
        return True

    def update_user_password(self, user_id, email, realname, password1, password2):
        """Updates a user's password."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None:
            raise Exception("Unexpected empty object: user_id.")
        if len(email) == 0:
            raise Exception("Email address not provided.")
        if len(realname) == 0:
            raise Exception("Name not provided.")
        if len(password1) < MIN_PASSWORD_LEN:
            raise Exception("The password is too short.")
        if password1 != password2:
            raise Exception("The passwords do not match.")

        salt = bcrypt.gensalt()
        computed_hash = bcrypt.hashpw(password1.encode('utf-8'), salt)
        if not self.database.update_user(user_id, email, realname, computed_hash):
            raise Exception("An internal error was encountered when updating the user.")
        return True

    def delete_user(self, user_id):
        """Removes a user from the database."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None or len(user_id) == 0:
            raise Exception("Bad parameter.")
        return self.database.delete_user(user_id)

    def create_user_device(self, email, device_str):
        """Associates a device with a user."""
        if self.database is None:
            raise Exception("No database.")
        if len(email) == 0:
            return False, "Email address not provided."
        if len(device_str) == 0:
            return False, "Device string not provided."
        user_id, _, _ = self.database.retrieve_user(email)
        return self.database.create_user_device(user_id, device_str)

    def retrieve_user_devices(self, user_id):
        """Returns a list of all the devices associated with the specified user."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None or len(user_id) == 0:
            raise Exception("Bad parameter.")
        devices = self.database.retrieve_user_devices(user_id)
        devices = list(set(devices)) # De-duplicate
        return devices

    def retrieve_user_from_device(self, device_str):
        """Finds the user associated with the device."""
        if self.database is None:
            raise Exception("No database.")
        if len(device_str) == 0:
            return False, "Device string not provided."
        return self.database.retrieve_user_from_device(device_str)

    def list_users_followed(self, user_id):
        """Returns the user ids for all users that are followed by the user with the specified id."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None or len(user_id) == 0:
            raise Exception("Bad parameter.")
        return self.database.retrieve_users_followed(user_id)

    def list_followers(self, user_id):
        """Returns the user ids for all users that follow the user with the specified id."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None or len(user_id) == 0:
            raise Exception("Bad parameter.")
        return self.database.retrieve_followers(user_id)

    def request_to_follow(self, user_id, target_id):
        """Appends a user to the followers list of the user with the specified id."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None or len(user_id) == 0:
            raise Exception("Bad parameter.")
        if target_id is None or len(target_id) == 0:
            raise Exception("Bad parameter.")
        return self.database.create_following_entry(user_id, target_id)

    def update_user_setting(self, user_id, key, value):
        """Create/update method for user preferences."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None:
            raise Exception("Bad parameter.")
        if key is None or len(key) == 0:
            raise Exception("Bad parameter.")
        if value is None or len(value) == 0:
            raise Exception("Bad parameter.")
        return self.database.update_user_setting(user_id, key, value)

    def retrieve_user_setting(self, user_id, key):
        """Retrieve method for user preferences."""
        if self.database is None:
            raise Exception("No database.")
        if user_id is None:
            raise Exception("Bad parameter.")
        if key is None or len(key) == 0:
            raise Exception("Bad parameter.")
        result = self.database.retrieve_user_setting(user_id, key)
        if result is None:
            if key == Keys.DEFAULT_PRIVACY:
                result = Keys.ACTIVITY_VISIBILITY_PUBLIC
            elif key == Keys.PREFERRED_UNITS_KEY:
                result = Keys.UNITS_STANDARD_KEY
            elif key == Keys.GENDER_KEY:
                result = Keys.GENDER_MALE_KEY
            else:
                result = ""
        return result.lower()

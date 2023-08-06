from sqlalchemy import create_engine, Table, Column, Integer, \
    String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import datetime
from common.settings import SERVER_DATABASE


class ServerDB:

    class AllUsers:
        def __init__(self, username, password, fullname=None, email=None):
            self.name = username
            self.last_login = datetime.datetime.now()
            self.full_name = fullname
            self.password = password
            self.email = email
            self.id = None

    class ActiveUsers:
        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    class LoginHistory:
        def __init__(self, name, date, ip, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    class Contacts:
        def __init__(self, user_id):
            self.id = None
            self.user = user_id
            self.con_list = ""

    def __init__(self):

        self.database_engine = create_engine(SERVER_DATABASE,
                                             echo=False, pool_recycle=7200)

        self.metadata = MetaData()

        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime),
                            Column('full_name', String),
                            Column('password', String),
                            Column('email', String)
                            )

        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'),
                                          unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime)
                                   )

        user_login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String),
                                   Column('port', String)
                                   )

        user_contacts = Table("Contacts", self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('user', ForeignKey('Users.id')),
                              Column('con_list', String, default=""))

        self.metadata.create_all(self.database_engine)

        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, user_login_history)
        mapper(self.Contacts, user_contacts)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):

        rez = self.session.query(self.AllUsers).filter_by(name=username)

        if rez.count():
            user = rez.first()
            user.last_login = datetime.datetime.now()

        else:
            user = self.AllUsers(username)
            self.session.add(user)

            self.session.commit()

        new_active_user = self.ActiveUsers(user.id,
                                           ip_address, port,
                                           datetime.datetime.now())
        self.session.add(new_active_user)

        history = self.LoginHistory(user.id, datetime.datetime.now(),
                                    ip_address, port)
        self.session.add(history)

        contacts = self.Contacts(user.id)
        self.session.add(contacts)

        self.session.commit()

    def user_register(self, username, password, fullname,
                      email, ip_address, port):

        rez = self.session.query(self.AllUsers).filter_by(name=username)

        if not rez.count():
            user = self.AllUsers(username, password, fullname, email)
            self.session.add(user)
            self.session.commit()

        self.user_login(username, ip_address, port)

    def fetch_userhash(self, username):

        rez = self.session.query(
            self.AllUsers).filter_by(name=username).first()

        if rez:
            return rez.password
        else:
            return None

    def user_logout(self, username):

        user = self.session.query(
            self.AllUsers).filter_by(name=username).first()

        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        self.session.commit()

    def users_list(self):
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
        )

        return query.all()

    def active_users_list(self):

        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
            ).join(self.AllUsers)

        return query.all()

    def login_history(self, username=None):

        query = self.session.query(self.AllUsers.name,
                                   self.LoginHistory.date_time,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.AllUsers)

        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()

    def add_contact(self, username, other):
        try:
            id_query = self.session.query(
                self.AllUsers.id).filter_by(name=username).first()
            list_query = self.session.query(
                self.Contacts).filter_by(user=id_query[0]).first()

            if list_query:
                if other not in list_query.con_list and username != other:
                    if list_query.con_list:
                        list_query.con_list += ','+other
                    else:
                        list_query.con_list += other

            self.session.commit()
        except Exception as e:
            print(e)

    def fetch_contacts(self, username):
        try:
            id_query = self.session.query(
                self.AllUsers.id).filter_by(name=username).first()
            list_query = self.session.query(
                self.Contacts).filter_by(user=id_query[0]).first()

            return list_query.con_list
        except Exception as e:
            print(e)

            return None

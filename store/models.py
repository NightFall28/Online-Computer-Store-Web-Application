from store import db, app, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)
    position = db.Column(db.Integer,nullable=False)
    is_pending = db.Column(db.Boolean, default=True, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

# class ApplicationBlacklist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
#     date_blacklisted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

#     def __repr__(self):
#         return f"ApplicationBlacklisted('{self.application_id}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)


    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

    money = db.Column(db.Numeric(10,2), nullable=False, default = 0.00)
    has_discount = db.Column(db.Boolean, default=False, nullable=False)

    is_employee = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_customer = db.Column(db.Boolean, default=False, nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)

    employee_title = db.Column(db.Integer, default=1)
    demote_count = db.Column(db.Integer, default=0)

    compliment = db.Column(db.Integer, default=0)
    warning = db.Column(db.Integer, default=0)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}', '{self.money}')"
    
class UserBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.datetime.now())
    #user_blacklisted_id = db.Column(db.Integer, nullable=False, unique=True)
    #user_blacklisted_name = db.Column(db.String(20),nullable=False)
    user_blacklisted_email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f"UserBlacklist('{self.user_blacklisted_id}', '{self.date_posted}')"
    
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    

class Processor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    company = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class LaptopProcessor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    company = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class GraphicCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    company = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spec = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class HardDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spec = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class Motherboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    chipset = db.Column(db.String(80), nullable=False)

class Desktop(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    name = db.Column(db.String(80), nullable=False)
    image_file = db.Column(db.String(30))
    category = db.Column(db.String(80), nullable=False)
    processor = db.Column(db.String(80), nullable=False)
    graphic_card = db.Column(db.String(80), nullable=False)
    operating_system = db.Column(db.String(80), nullable=False)
    memory = db.Column(db.String(80), nullable=False)
    hard_drive = db.Column(db.String(80), nullable=False)
    motherboard = db.Column(db.String(80), nullable=False)
    case = db.Column(db.String(80), nullable=False)

    rating_1 = db.Column(db.Integer, default=0)
    rating_2 = db.Column(db.Integer, default=0)
    rating_3 = db.Column(db.Integer, default=0)
    rating_4 = db.Column(db.Integer, default=0)
    rating_5 = db.Column(db.Integer, default=0)

    price = db.Column(db.Numeric(10,2), nullable=False)

class Laptop(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    name = db.Column(db.String(80), nullable=False)
    image_file = db.Column(db.String(30), nullable=False)
    processor = db.Column(db.String(80), nullable=False)
    graphic_card = db.Column(db.String(80), nullable=False)
    operating_system = db.Column(db.String(80), nullable=False)
    memory = db.Column(db.String(80), nullable=False)
    hard_drive = db.Column(db.String(80), nullable=False)

    rating_1 = db.Column(db.Integer, default=0)
    rating_2 = db.Column(db.Integer, default=0)
    rating_3 = db.Column(db.Integer, default=0)
    rating_4 = db.Column(db.Integer, default=0)
    rating_5 = db.Column(db.Integer, default=0)

    price = db.Column(db.Numeric(10,2), nullable=False)


class EdgeComputingRAM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    RAM = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class EdgeComputingDevices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    processor = db.Column(db.String(200), nullable=False)
    connectivity = db.Column(db.String(200), nullable=False)
    ports = db.Column(db.String(200), nullable=False)
    storage = db.Column(db.String(200), nullable=False)
    power = db.Column(db.String(200), nullable=False)

class EdgeComputing(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    processor = db.Column(db.String(200), nullable=False)
    RAM = db.Column(db.String(200))
    connectivity = db.Column(db.String(200), nullable=False)
    ports = db.Column(db.String(200), nullable=False)
    storage = db.Column(db.String(200), nullable=False)
    power = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(100), nullable=False)

    rating_1 = db.Column(db.Integer, default=0)
    rating_2 = db.Column(db.Integer, default=0)
    rating_3 = db.Column(db.Integer, default=0)
    rating_4 = db.Column(db.Integer, default=0)
    rating_5 = db.Column(db.Integer, default=0)

    price = db.Column(db.Numeric(10,2))

class MacbookList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    processor = db.Column(db.String(200), nullable=False)
    GPU = db.Column(db.String(200), nullable=False)
    display = db.Column(db.String(200), nullable=False)
    ports = db.Column(db.String(200), nullable=False)
    power = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class MacbookAirRAM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    memory = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class MacbookAirStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hard_drive = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class MacbookAir(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    processor = db.Column(db.String(200), nullable=False)
    GPU = db.Column(db.String(200), nullable=False)
    memory = db.Column(db.String(200), nullable=False)
    hard_drive = db.Column(db.String(200), nullable=False)
    display = db.Column(db.String(200), nullable=False)
    ports = db.Column(db.String(200), nullable=False)
    power = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(100), nullable=False)

    rating_1 = db.Column(db.Integer, default=0)
    rating_2 = db.Column(db.Integer, default=0)
    rating_3 = db.Column(db.Integer, default=0)
    rating_4 = db.Column(db.Integer, default=0)
    rating_5 = db.Column(db.Integer, default=0)

    price = db.Column(db.Numeric(10,2), nullable=False)

class iMacList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    processor = db.Column(db.String(200), nullable=False)
    GPU = db.Column(db.String(200), nullable=False)
    ports = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class iMacMemoryList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    memory = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class iMacStoragelist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hard_drive = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class iMacAccessoryList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accessory = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class iMac(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    processor = db.Column(db.String(200), nullable=False)
    GPU = db.Column(db.String(200), nullable=False)
    ports = db.Column(db.String(200), nullable=False)
    color = db.Column(db.String(200), nullable=False)
    memory = db.Column(db.String(200), nullable=False)
    hard_drive = db.Column(db.String(200), nullable=False)
    accessory = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(100), nullable=False)

    rating_1 = db.Column(db.Integer, default=0)
    rating_2 = db.Column(db.Integer, default=0)
    rating_3 = db.Column(db.Integer, default=0)
    rating_4 = db.Column(db.Integer, default=0)
    rating_5 = db.Column(db.Integer, default=0)

    price = db.Column(db.Numeric(10,2), nullable=False)

class CheckoutItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config_id = db.Column(db.Integer)
    is_desktop = db.Column(db.Boolean, default=False)
    is_laptop = db.Column(db.Boolean, default=False)
    is_macbook = db.Column(db.Boolean, default=False)
    is_imac = db.Column(db.Boolean, default=False)
    is_edge_computing = db.Column(db.Boolean, default=False)
    is_customer_desktop = db.Column(db.Boolean, default=False)
    item_name = db.Column(db.String(200), nullable=False)
    is_checkedout = db.Column(db.Boolean, default=False)
    madeby_customer = db.Column(db.Boolean, default=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class DesktopComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desktop_id = db.Column(db.Integer)
    comment = db.Column(db.String(400))
    image_file = db.Column(db.String(80))
    author = db.Column(db.String(80))
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class LaptopComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    laptop_id = db.Column(db.Integer)
    comment = db.Column(db.String(400))
    image_file = db.Column(db.String(80))
    author = db.Column(db.String(80))
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class MacbookComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    macbook_id = db.Column(db.Integer)
    comment = db.Column(db.String(400))
    image_file = db.Column(db.String(80))
    author = db.Column(db.String(80))
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class iMacComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imac_id = db.Column(db.Integer)
    comment = db.Column(db.String(400))
    image_file = db.Column(db.String(80))
    author = db.Column(db.String(80))
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class EdgeComputingComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    edge_computing_id = db.Column(db.Integer)
    comment = db.Column(db.String(400))
    image_file = db.Column(db.String(80))
    author = db.Column(db.String(80))
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class Communicate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    author = db.Column(db.String(80))
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class CommunicateComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer)
    image_file = db.Column(db.String(80))
    author = db.Column(db.String(80))
    content = db.Column(db.String(500))
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer)
    reported_user_id = db.Column(db.Integer)
    content = db.Column(db.String(500))
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    
class CustomerMadeDesktop(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    allow_for_display = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(80), nullable=False)
    image_file = db.Column(db.String(30))
    category = db.Column(db.String(80), nullable=False)
    processor = db.Column(db.String(80), nullable=False)
    graphic_card = db.Column(db.String(80), nullable=False)
    operating_system = db.Column(db.String(80), nullable=False)
    memory = db.Column(db.String(80), nullable=False)
    hard_drive = db.Column(db.String(80), nullable=False)
    motherboard = db.Column(db.String(80), nullable=False)
    case = db.Column(db.String(80), nullable=False)

    rating_1 = db.Column(db.Integer, default=0)
    rating_2 = db.Column(db.Integer, default=0)
    rating_3 = db.Column(db.Integer, default=0)
    rating_4 = db.Column(db.Integer, default=0)
    rating_5 = db.Column(db.Integer, default=0)

    price = db.Column(db.Numeric(10,2), nullable=False)

class CustomerMadeDesktopComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desktop_id = db.Column(db.Integer)
    comment = db.Column(db.String(400))
    image_file = db.Column(db.String(80))
    author = db.Column(db.String(80))
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())


with app.app_context():
    db.create_all()
"""
    DATABASE MODELS.
"""
from peewee import *
import uuid
import datetime
from enum import StrEnum
database = SqliteDatabase('database.sqlite3')

class TRANSACTION_CATEGORIES(StrEnum):
    rent_payment = 'rent_payment'
    utility_bills_payment = 'utility_bills_payment'
    other = 'other'

class TRANSACTION_TYPES(StrEnum):
    income = 'income'
    expense = 'expense'

class TENANT_STATUS(StrEnum):
    active = 'active'
    inactive = 'inactive'

def get_notification_date(object) -> str:
    if object.dates.exists():
        named_dates = object.dates
        named_dates = sorted(named_dates, key=lambda x: x.date)

        current_date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

        for named_date in named_dates:
            date = datetime.datetime.fromisoformat(to_isoformat(named_date.date))
            if date >= current_date:
                return date.strftime("%Y-%m-%d %H:%M")

    return '-'

def get_tenant_status(object) -> str:
    today = datetime.date.today()
    active_lease_contract = LeaseContract.select().where(
        (LeaseContract.tenant == object) &
        (LeaseContract.start_date <= today) &
        (LeaseContract.end_date >= today)
        )

    if active_lease_contract.exists():
        return TENANT_STATUS.active
    return TENANT_STATUS.inactive


def to_isoformat(date) -> str:
    if isinstance(date, str):
        return date
    else:
        return date.isoformat()


class DateTimeUTCField(DateTimeField):
    def db_value(self, value):
        if isinstance(value, str):
            value = datetime.datetime.fromisoformat(value)

        if value and value.tzinfo:
            value = value.astimezone(datetime.timezone.utc)
        
        return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


class BaseModel(Model):
    class Meta:
        database = database

class Tenant(BaseModel):
    id = IntegerField(primary_key=True)

    first_name = CharField(max_length=255, null=False)
    last_name = CharField(max_length=255, null=False)

    phone = CharField(max_length=11, null=False)
    email = CharField(max_length=255, unique=True, null=False)

    parents_address = CharField(max_length=255, null=False, default='')
    parents_phone = CharField(max_length=11, null=False, default='')

    note = TextField(null=False, default='')

    @staticmethod
    def _to_dict(tenant_object):
        if tenant_object is not None:
            return {
                'id': tenant_object.id,
                'first_name': tenant_object.first_name,
                'last_name': tenant_object.last_name,
                'phone': tenant_object.phone,
                'email': tenant_object.email,
                'parents_address': tenant_object.parents_address,
                'parents_phone': tenant_object.parents_phone,
                'note': tenant_object.note,
                'status': get_tenant_status(tenant_object),
            }
        return None

class Owner(BaseModel):
    id = IntegerField(primary_key=True)

    first_name = CharField(max_length=255, null=False)
    last_name = CharField(max_length=255, null=False)

    phone = CharField(max_length=11, null=False)
    email = CharField(max_length=255, unique=True, null=False)

    note = TextField(null=False, default='')

    @staticmethod
    def _to_dict(owner_object):
        if owner_object is not None:
            return {
                'id': owner_object.id,
                'first_name': owner_object.first_name,
                'last_name': owner_object.last_name,
                'phone': owner_object.phone,
                'email': owner_object.email,
                'note': owner_object.note,
            }
        return None

class Apartment(BaseModel):
    id = IntegerField(primary_key=True)
    unique_identifier = UUIDField(default=uuid.uuid4)

    name = CharField(max_length=255, null=False, default='')
    address = CharField(max_length=255, null=False)
    city = CharField(max_length=255, null=False, default='')

    rooms = IntegerField(default=0, null=False)
    apartment_area = FloatField(default=0.0, null=False)
    floor = IntegerField(default=0, null=False)
    beds = IntegerField(null=False)

    note = TextField(null=False, default='')

    owner = ForeignKeyField(Owner, backref='apartments', null=True, on_delete='SET NULL')

    @staticmethod
    def _to_dict(apartment_object):
        if apartment_object is not None:
            return {
                'id': apartment_object.id,
                'unique_identifier': apartment_object.unique_identifier.__str__(),
                'name': apartment_object.name,
                'address': apartment_object.address,
                'city': apartment_object.city,
                'rooms': apartment_object.rooms,
                'apartment_area': apartment_object.apartment_area,
                'floor': apartment_object.floor,
                'beds': apartment_object.beds,
                'note': apartment_object.note,
                'owner': Owner._to_dict(apartment_object.owner),
            }
        return None

class LeaseContract(BaseModel):
    id = IntegerField(primary_key=True)

    start_date = DateField(null=False)
    end_date = DateField(null=False)

    rent_price = FloatField(null=False)
    utilities_included = BooleanField(null=False)
    tax = FloatField(null=False)

    note = TextField(null=False, default='')

    tenant = ForeignKeyField(Tenant, backref='lease_contracts', null=True, on_delete='CASCADE')
    apartment = ForeignKeyField(Apartment, backref='lease_contracts', null=True, on_delete='CASCADE')

    @staticmethod
    def _to_dict(lease_contract_object):
        if lease_contract_object is not None:
            return {
                'id': lease_contract_object.id,
                'start_date': to_isoformat(lease_contract_object.start_date),
                'end_date': to_isoformat(lease_contract_object.end_date),
                'rent_price': lease_contract_object.rent_price,
                'utilities_included': lease_contract_object.utilities_included,
                'tax': lease_contract_object.tax,
                'note': lease_contract_object.note,
                'tenant': Tenant._to_dict(lease_contract_object.tenant),
                'apartment': Apartment._to_dict(lease_contract_object.apartment),
            }
        return None

class UtilityBills(BaseModel):
    id = IntegerField(primary_key=True)

    water = FloatField(default=0.0, null=False)
    electricity = FloatField(default=0.0, null=False)
    tax = FloatField(default=0.0, null=False)

    @staticmethod
    def _to_dict(utility_bills_object):
        if utility_bills_object is not None:
            return {
                'id': utility_bills_object.id,
                'water': utility_bills_object.water,
                'electricity': utility_bills_object.electricity,
                'tax': utility_bills_object.tax,
            }
        return None

class Transaction(BaseModel):
    id = IntegerField(primary_key=True)

    date = DateField(null=False)
    transaction_type = CharField(max_length=7, null=False)
    amount = IntegerField(null=False)
    category = CharField(max_length=30, null=False)

    paid = BooleanField(default=True, null=False)

    description = TextField(null=False, default='')

    lease_contract = ForeignKeyField(LeaseContract, backref='transactions', null=True, on_delete='CASCADE')
    utility_bills = ForeignKeyField(UtilityBills, backref='transaction', null=True, on_delete='SET NULL')

    @staticmethod
    def _to_dict(transaction_object):
        if transaction_object is not None:
            return {
                'id': transaction_object.id,
                'date': to_isoformat(transaction_object.date),
                'transaction_type': transaction_object.transaction_type,
                'amount': transaction_object.amount,
                'category': transaction_object.category,
                'paid': transaction_object.paid,
                'description': transaction_object.description,
                'lease_contract': LeaseContract._to_dict(transaction_object.lease_contract),
                'utility_bills': UtilityBills._to_dict(transaction_object.utility_bills),
            }
        return None

class NamedDate(BaseModel):
    id = IntegerField(primary_key=True)

    name = CharField(max_length=255, default='', null=False)
    date = DateTimeUTCField(null=False)

    @staticmethod
    def _to_dict(named_date_object):
        if named_date_object is not None:
            return {
                'id': named_date_object.id,
                'name': named_date_object.name,
                'date': to_isoformat(named_date_object.date),
            }
        return None

class CellAction(BaseModel):
    id = IntegerField(primary_key=True)

    done = BooleanField(default=False)
    action = CharField(max_length=255, default='', null=False)

    @staticmethod
    def _to_dict(cell_action_object):
        if cell_action_object is not None:
            return {
                'id': cell_action_object.id,
                'done': cell_action_object.done,
                'action': cell_action_object.action
            }
        return None

class Reminder(BaseModel):
    id = IntegerField(primary_key=True)

    date = DateField(null=False)
    notify_owner = BooleanField(default=True, null=False)
    text = CharField(max_length=255, default='', null=False)
    email_subject = CharField(max_length=255, default='', null=False)

    lease_contract = ForeignKeyField(LeaseContract, backref='reminders', null=True, on_delete='CASCADE')
    dates = ManyToManyField(NamedDate, backref='included_in_reminders')

    @staticmethod
    def _to_dict(reminder_object):
        if reminder_object is not None:
            return {
                'id': reminder_object.id,
                'date': to_isoformat(reminder_object.date),
                'notify_owner': reminder_object.notify_owner,
                'text': reminder_object.text,
                'email_subject': reminder_object.email_subject,
                'lease_contract': LeaseContract._to_dict(reminder_object.lease_contract),
                'dates': [NamedDate._to_dict(date) for date in reminder_object.dates],
                'nearest_date': get_notification_date(reminder_object),
            }
        return None

class Task(BaseModel):
    id = IntegerField(primary_key=True)

    date = DateField(null=False)
    notify_owner = BooleanField(default=True, null=False)
    text = CharField(max_length=255, default='', null=False)
    email_subject = CharField(max_length=255, default='', null=False)

    note = TextField(null=False, default='')

    lease_contract = ForeignKeyField(LeaseContract, backref='tasks', null=True, on_delete='CASCADE')
    dates = ManyToManyField(NamedDate, backref='included_in_tasks')
    actions = ManyToManyField(CellAction, backref='included_in_tasks')

    @staticmethod
    def _to_dict(task_object):
        if task_object is not None:
            return {
                'id': task_object.id,
                'date': to_isoformat(task_object.date),
                'notify_owner': task_object.notify_owner,
                'text': task_object.text,
                'email_subject': task_object.email_subject,
                'note': task_object.note,
                'lease_contract': LeaseContract._to_dict(task_object.lease_contract),
                'dates': [NamedDate._to_dict(date) for date in task_object.dates],
                'actions': [CellAction._to_dict(cell_action) for cell_action in task_object.actions],
                'nearest_date': get_notification_date(task_object),
            }
        return None
    
class Tool(BaseModel):
    SN = IntegerField(primary_key=True)
    category = CharField(max_length=255, null=False)
    platform = IntegerField()
    license_type = IntegerField()
    api_support = IntegerField()
    name = CharField(max_length=255, null=False)
    uid = CharField(max_length=255, null=False)
    description = TextField(null = False, default='')
    version = CharField(max_length=255, null=False)
    release_date = DateField(null=False)
    lastupdated_date = DateField(null=False)
    producer = CharField(max_length=255, null=False)
    rating = IntegerField()
    downloadlink = TextField(null=False, default='')
    editor_choice = IntegerField()
    
    @staticmethod
    def _to_dict(tool_object):
        if tool_object is not None:
            return {
                'SN': tool_object.SN,
                'category': tool_object.category,
                'platform': tool_object.platform,
                'license_type': tool_object.license_type,
                'api_support' : tool_object.api_support,
                'name' : tool_object.name,
                'uid' : tool_object.uid,
                'description' : tool_object.description,
                'version' : tool_object.version,
                'release_date' : to_isoformat(tool_object.release_date),
                'lastupdated_date' : to_isoformat(tool_object.lastupdated_date),
                'producer' : tool_object.producer,
                'rating' : tool_object.rating,
                'downloadlink' : tool_object.downloadlink,
                'editor_choice' : tool_object.editor_choice,
            }
        return None

class Reference(BaseModel):
    SN = IntegerField(primary_key=True)
    name = CharField(max_length=255, null=False)
    type = CharField(max_length=255, null=False)
    url = TextField(null = False, default='')
    summary = TextField(null=False, default='')

    @staticmethod
    def _to_dict(reference_object):
        if reference_object is not None:
            return {
                'SN': reference_object.SN,
                'name': reference_object.name,
                'type': reference_object.type,
                'url': reference_object.url,
                'summary': reference_object.summary
            }
        return None

def create_tables():
    with database:
        ReminderNamedDate = Reminder.dates.get_through_model()
        TaskNamedDate = Task.dates.get_through_model()
        TaskCellAction = Task.actions.get_through_model()
        database.create_tables([Tool, Reference])

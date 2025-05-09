from neomodel import (
    StructuredNode, StringProperty, FloatProperty, IntegerProperty,
    RelationshipTo, UniqueIdProperty
)

class Party(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    type = StringProperty()  # e.g., "Client" or "Service Provider"
    address = StringProperty()
    context = StringProperty()

class Vendor(Party):
    pass  # Same as Party, but used semantically

class Division(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    description = StringProperty()

class Initiative(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    description = StringProperty()

class Project(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    description = StringProperty()
    start_date = StringProperty()
    end_date = StringProperty()
    status = StringProperty()

    division = RelationshipTo(Division, 'BELONGS_TO')
    initiative = RelationshipTo(Initiative, 'PART_OF')

class Contract(StructuredNode):
    uid = UniqueIdProperty()
    file_name = StringProperty(required=True, unique_index=True)
    type = StringProperty()
    summary_description = StringProperty()
    start_date = StringProperty()
    end_date = StringProperty()

    vendor = RelationshipTo(Party, 'SIGNED_BY_VENDOR')
    client = RelationshipTo(Party, 'SIGNED_BY_CLIENT')
    services = RelationshipTo('Service', 'COVERS')
    roles = RelationshipTo('Role', 'INCLUDES')
    project = RelationshipTo(Project, 'ASSOCIATED_WITH')

class Service(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    description = StringProperty()
    period = StringProperty()
    coverage = StringProperty()
    notes = StringProperty()

class ServiceLevelAgreement(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    description = StringProperty()
    target = StringProperty()
    metric = StringProperty()
    unit = StringProperty()
    frequency = StringProperty()
    enforcement_method = StringProperty()

    applies_to = RelationshipTo(Service, 'APPLIES_TO')

class Role(StructuredNode):
    uid = UniqueIdProperty()
    role_name = StringProperty()
    description = StringProperty()
    level = StringProperty()
    location = StringProperty()
    hours_committed = IntegerProperty()
    billing_type = StringProperty()
    schedule_reference = StringProperty()
    project = StringProperty()

    rate = RelationshipTo('Rate', 'HAS_RATE')
    resource = RelationshipTo('Resource', 'FILLED_BY')

class Rate(StructuredNode):
    uid = UniqueIdProperty()
    amount = FloatProperty()
    currency = StringProperty()
    unit = StringProperty()

class Resource(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

class Deliverable(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    delivery_date = StringProperty()
    invoice_amount_usd = FloatProperty()
    percentage = FloatProperty()

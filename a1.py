
from neomodel import (
    StructuredNode, StringProperty, FloatProperty, IntegerProperty, DateProperty,
    RelationshipTo, ArrayProperty
)

# --- Canonical Models ---

class CanonicalService(StructuredNode):
    name = StringProperty()
    description = StringProperty()

class CanonicalRole(StructuredNode):
    name = StringProperty()
    description = StringProperty()

class CanonicalPerson(StructuredNode):
    name = StringProperty()

class CanonicalVendor(StructuredNode):
    name = StringProperty()

class CanonicalLocation(StructuredNode):
    name = StringProperty()
    address = StringProperty()
    city = StringProperty()
    state = StringProperty()
    country = StringProperty()
    continent = StringProperty()

class CanonicalDivision(StructuredNode):
    name = StringProperty()

# --- Main Models ---

class FeeBreakdown(StructuredNode):
    event = StringProperty()
    fee = StringProperty()

class Signature(StructuredNode):
    type = StringProperty()
    name = StringProperty()
    title = StringProperty()
    date = DateProperty()
    # Relationships to canonical nodes
    is_canonical_person = RelationshipTo(CanonicalPerson, 'IS_CANONICAL_PERSON')

class Service(StructuredNode):
    name = StringProperty()
    description = StringProperty()
    period = StringProperty()
    coverage = StringProperty()
    locations = ArrayProperty(StringProperty())
    days = IntegerProperty()
    quantity = IntegerProperty()
    unit_price = StringProperty()
    total = StringProperty()
    notes = ArrayProperty(StringProperty())
    # Relationships to canonical nodes
    provided_at = RelationshipTo(CanonicalLocation, 'PROVIDED_AT')
    is_canonical_service = RelationshipTo(CanonicalService, 'IS_CANONICAL_SERVICE')

class Role(StructuredNode):
    name = StringProperty()
    resource_name = StringProperty() 
    description = StringProperty()
    level = StringProperty()
    location = StringProperty()
    hours_committed = IntegerProperty()
    rate_amount = FloatProperty()
    rate_currency = StringProperty()
    rate_unit = StringProperty()
    total_fees = FloatProperty()
    billing_type = StringProperty()
    schedule_reference = StringProperty()
    project = StringProperty()
    # Relationships to canonical nodes
    is_canonical_role = RelationshipTo(CanonicalRole, 'IS_CANONICAL_ROLE')
    assigned_to = RelationshipTo(CanonicalPerson, 'ASSIGNED_TO')
    located_at = RelationshipTo(CanonicalLocation, 'LOCATED_AT')

class ServiceLevelAgreement(StructuredNode):
    name = StringProperty()
    description = StringProperty()
    target = StringProperty()
    metric = StringProperty()
    unit = StringProperty()
    frequency = StringProperty()
    applies_to = ArrayProperty(StringProperty())
    penalty_clause = StringProperty()
    enforcement_method = StringProperty()

class EngagementScope(StructuredNode):
    core_applications = ArrayProperty(StringProperty())
    supporting_applications = ArrayProperty(StringProperty())
    key_activities = ArrayProperty(StringProperty())
    assumptions = ArrayProperty(StringProperty())
    expectations = ArrayProperty(StringProperty())
    conditions = ArrayProperty(StringProperty())

class Initiative(StructuredNode):
    name = StringProperty()
    description = StringProperty()

class Project(StructuredNode):
    name = StringProperty()
    description = StringProperty()
    start_date = DateProperty()
    end_date = DateProperty()
    status = StringProperty()

class DeliverableAndInvoice(StructuredNode):
    deliverable = StringProperty()
    delivery_date = DateProperty()
    invoice_amount_usd = FloatProperty()
    percentage = FloatProperty()

class Party(StructuredNode):
    name = StringProperty()
    type = StringProperty()
    address = StringProperty()
    context = StringProperty()
    # Relationships to canonical nodes
    is_canonical_person = RelationshipTo(CanonicalPerson, 'IS_CANONICAL_PERSON')
    located_at = RelationshipTo(CanonicalLocation, 'LOCATED_AT')

class Contract(StructuredNode):
    file_name = StringProperty()
    vendor_name = StringProperty()
    type = StringProperty()
    summary_description = StringProperty()
    start_date = DateProperty()
    end_date = DateProperty()
    base_fee = StringProperty()
    total_fee = StringProperty()
    exclusions = ArrayProperty(StringProperty())
    payment_terms = StringProperty()
    billing_instructions = StringProperty()
    exceptions_or_notes = ArrayProperty(StringProperty())
    funding_request_id = StringProperty()
    division = StringProperty()
    # Relationships to main nodes
    has_fee_breakdown = RelationshipTo(FeeBreakdown, 'HAS_FEE_BREAKDOWN')
    signed_by = RelationshipTo(Signature, 'SIGNED_BY')
    includes_service = RelationshipTo(Service, 'INCLUDES_SERVICE')
    includes_role = RelationshipTo(Role, 'INCLUDES_ROLE')
    governed_by_sla = RelationshipTo(ServiceLevelAgreement, 'GOVERNED_BY_SLA')
    has_engagement_scope = RelationshipTo(EngagementScope, 'HAS_ENGAGEMENT_SCOPE')
    associated_with_initiative = RelationshipTo(Initiative, 'ASSOCIATED_WITH_INITIATIVE')
    associated_with_project = RelationshipTo(Project, 'ASSOCIATED_WITH_PROJECT')
    has_deliverable_invoice = RelationshipTo(DeliverableAndInvoice, 'HAS_DELIVERABLE_INVOICE')
    involves_party = RelationshipTo(Party, 'INVOLVES_PARTY')
    # Relationships to canonical nodes
    is_with_vendor = RelationshipTo(CanonicalVendor, 'IS_WITH_VENDOR')
    is_for_division = RelationshipTo(CanonicalDivision, 'IS_FOR_DIVISION')

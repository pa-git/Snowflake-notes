
from neomodel import (
    StructuredNode, StringProperty, FloatProperty, IntegerProperty, DateProperty,
    RelationshipTo, ArrayProperty
)

# --- Related Models (Canonical, Rate, Location, etc.) ---

class CanonicalParty(StructuredNode):
    name = StringProperty()
    description = StringProperty()

class CanonicalService(StructuredNode):
    name = StringProperty()
    description = StringProperty()

class CanonicalVendor(StructuredNode):
    name = StringProperty()

class CanonicalLocation(StructuredNode):
    address = StringProperty()
    city = StringProperty()
    state = StringProperty()
    country = StringProperty()
    continent = StringProperty()

class Location(StructuredNode):
    name = StringProperty()
    located_in = RelationshipTo(CanonicalLocation, 'LOCATED_IN')

class Rate(StructuredNode):
    unit = StringProperty()
    amount = FloatProperty()
    currency = StringProperty()
    total_fees = FloatProperty()
    billing_type = StringProperty()
    days_committed = IntegerProperty()
    hours_committed = IntegerProperty()
    notes = ArrayProperty(StringProperty())

# --- Main Models ---

class FeeBreakdown(StructuredNode):
    event = StringProperty()
    fee = StringProperty()
    notes = StringProperty()

class Vendor(StructuredNode):
    name = StringProperty()
    is_canonical_vendor = RelationshipTo(CanonicalVendor, 'IS_CANONICAL_VENDOR')

class Party(StructuredNode):
    name = StringProperty()
    title = StringProperty()
    address = StringProperty()
    context = StringProperty()
    is_canonical_party = RelationshipTo(CanonicalParty, 'IS_CANONICAL_PARTY')
    located_in = RelationshipTo(CanonicalLocation, 'LOCATED_IN')

class CanonicalRole(StructuredNode):
    name = StringProperty()
    description = StringProperty()

class Role(StructuredNode):
    name = StringProperty()
    description = StringProperty()
    level = StringProperty()
    assigned_to = RelationshipTo(Party, 'ASSIGNED_TO')
    has_rate = RelationshipTo(Rate, 'HAS_RATE')
    based_at = RelationshipTo(Location, 'BASED_AT')
    is_canonical_role = RelationshipTo(CanonicalRole, 'IS_CANONICAL_ROLE')

class Service(StructuredNode):
    name = StringProperty()
    description = StringProperty()
    has_rate = RelationshipTo(Rate, 'HAS_RATE')
    provided_at = RelationshipTo(Location, 'PROVIDED_AT')
    is_canonical_service = RelationshipTo(CanonicalService, 'IS_CANONICAL_SERVICE')

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

class Division(StructuredNode):
    name = StringProperty()

class Initiative(StructuredNode):
    name = StringProperty()
    description = StringProperty()

class Project(StructuredNode):
    name = StringProperty()
    description = StringProperty()
    start_date = DateProperty()
    end_date = DateProperty()
    status = StringProperty()

class Contract(StructuredNode):
    file_name = StringProperty()
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

    has_vendor = RelationshipTo(Vendor, 'HAS_VENDOR')
    involves_party = RelationshipTo(Party, 'INVOLVES_PARTY')
    has_scope = RelationshipTo(EngagementScope, 'HAS_SCOPE')
    belongs_to_division = RelationshipTo(Division, 'BELONGS_TO_DIVISION')
    associated_with_initiative = RelationshipTo(Initiative, 'ASSOCIATED_WITH_INITIATIVE')
    includes_service = RelationshipTo(Service, 'INCLUDES_SERVICE')
    governed_by_sla = RelationshipTo(ServiceLevelAgreement, 'GOVERNED_BY_SLA')
    delivers_project = RelationshipTo(Project, 'DELIVERS_PROJECT')
    has_fee_breakdown = RelationshipTo(FeeBreakdown, 'HAS_FEE_BREAKDOWN')

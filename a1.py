NODES
CONTRACT
file_name

type

summary_description

start_date

end_date

base_fee

total_fee

exclusions (list)

payment_terms

billing_instructions

exceptions_or_notes (list)

funding_request_id (from CSV lookup)

PARTY
(from signatures, parties, roles.resource_name)

name

title

address

context

CANONICAL_PARTY
name

description

SERVICE
name

description

CANONICAL_SERVICE
name

description

VENDOR
name

CANONICAL_VENDOR
name

RATE
unit

amount

currency

total_fees

billing_type

days_committed

hours_committed

notes (list)

ROLE
name

description

level

SERVICE_LEVEL_AGREEMENT
name

description

target

metric

unit

frequency

applies_to (string or array)

penalty_clause

enforcement_method

ENGAGEMENT_SCOPE
core_applications (list)

supporting_applications (list)

key_activities (list)

assumptions (list)

expectations (list)

conditions (list)

DIVISION
name (from CSV lookup or JSON)

INITIATIVE
name

description

PROJECT
name

description

start_date

end_date

status

LOCATION
name

CANONICAL_LOCATION
address

city

state

country

continent

🔗 RELATIONSHIPS
Source → Target	Relationship Name	Notes
CONTRACT → VENDOR	HAS_VENDOR	
CONTRACT → PARTY	INVOLVES_PARTY	covers all types from signatures, roles.resource_name, parties
PARTY → CANONICAL_PARTY	IS_CANONICAL_PARTY	canonical name grouping
PARTY → CANONICAL_LOCATION	LOCATED_IN	
CONTRACT → ENGAGEMENT_SCOPE	HAS_SCOPE	
CONTRACT → DIVISION	BELONGS_TO_DIVISION	
CONTRACT → INITIATIVE	ASSOCIATED_WITH_INITIATIVE	
CONTRACT → SERVICE	INCLUDES_SERVICE	
SERVICE → RATE	HAS_RATE	
SERVICE → LOCATION	PROVIDED_AT	
SERVICE → CANONICAL_SERVICE	IS_CANONICAL_SERVICE	
CONTRACT → SERVICE_LEVEL_AGREEMENT	GOVERNED_BY_SLA	
CONTRACT → PROJECT	DELIVERS_PROJECT	
VENDOR → CANONICAL_VENDOR	IS_CANONICAL_VENDOR	
ROLE → PARTY	ASSIGNED_TO	resource_name → PARTY
ROLE → RATE	HAS_RATE	
ROLE → LOCATION	BASED_AT	
ROLE → CANONICAL_ROLE	IS_CANONICAL_ROLE	if such grouping exists

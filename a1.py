Node: Contract
- file_name
- vendor_name
- type
- summary_description
- start_date
- end_date
- base_fee
- total_fee
- exclusions[]
- payment_terms
- billing_instructions
- exceptions_or_notes[]
- funding_request_id
- division

Node: Service
- name
- description
- period
- coverage
- locations[]
- days
- quantity
- unit_price
- total
- notes[]

Node: Role
- name
- resource_name
- description
- level
- location
- hours_committed
- rate_amount
- rate_currency
- rate_unit
- total_fees
- billing_type
- schedule_reference
- project

Node: Party
- name
- type
- address
- context

Node: Signature
- type
- name
- title
- date

Node: ServiceLevelAgreement
- name
- description
- target
- metric
- unit
- frequency
- applies_to[]
- penalty_clause
- enforcement_method

Node: EngagementScope
- core_applications[]
- supporting_applications[]
- key_activities[]
- assumptions[]
- expectations[]
- conditions[]

Node: Initiative
- name
- description

Node: Project
- name
- description
- start_date
- end_date
- status

Node: DeliverableAndInvoice
- deliverable
- delivery_date
- invoice_amount_usd
- percentage

Node: FeeBreakdown
- event
- fee

Node: CanonicalPerson
- name

Node: CanonicalRole
- name
- description

Node: CanonicalService
- name
- description

Node: CanonicalVendor
- name

Node: CanonicalDivision
- name

Node: CanonicalLocation
- name
- address
- city
- state
- country
- continent

------------

(Contract)-[:HAS_FEE_BREAKDOWN]->(FeeBreakdown)
(Contract)-[:SIGNED_BY]->(Signature)
(Contract)-[:INCLUDES_SERVICE]->(Service)
(Contract)-[:INCLUDES_ROLE]->(Role)
(Contract)-[:GOVERNED_BY_SLA]->(ServiceLevelAgreement)
(Contract)-[:HAS_ENGAGEMENT_SCOPE]->(EngagementScope)
(Contract)-[:ASSOCIATED_WITH_INITIATIVE]->(Initiative)
(Contract)-[:ASSOCIATED_WITH_PROJECT]->(Project)
(Contract)-[:HAS_DELIVERABLE_INVOICE]->(DeliverableAndInvoice)
(Contract)-[:INVOLVES_PARTY]->(Party)
(Contract)-[:IS_WITH_VENDOR]->(CanonicalVendor)
(Contract)-[:IS_FOR_DIVISION]->(CanonicalDivision)

(Service)-[:IS_CANONICAL_SERVICE]->(CanonicalService)
(Service)-[:PROVIDED_AT]->(CanonicalLocation)

(Role)-[:IS_CANONICAL_ROLE]->(CanonicalRole)
(Role)-[:ASSIGNED_TO]->(CanonicalPerson)
(Role)-[:LOCATED_AT]->(CanonicalLocation)

(Signature)-[:IS_CANONICAL_PERSON]->(CanonicalPerson)

(Party)-[:IS_CANONICAL_PERSON]->(CanonicalPerson)
(Party)-[:LOCATED_AT]->(CanonicalLocation)

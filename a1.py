<SCHEMA>
  <NODES>
    <Contract>
      uid: ID
      file_name: String
      vendor_name: String
      type: String
      summary_description: String
      start_date: Date
      end_date: Date
      base_fee: String
      total_fee: String
      exclusions: [String]
      payment_terms: String
      billing_instructions: String
      exceptions_or_notes: [String]
      funding_request_id: String
      division: String
    </Contract>

    <Role>
      uid: ID
      name: String
      resource_name: String
      description: String
      level: String
      location: String
      hours_committed: Integer
      rate_amount: Float
      rate_currency: String
      rate_unit: String
      total_fees: Float
      billing_type: String
      schedule_reference: String
      project: String
    </Role>

    <Rate>  # This is modeled inside Role, no separate Rate node in your model.
    </Rate>

    <Resource>  # Not explicitly defined as a node in your model.
    </Resource>

    <Service>
      uid: ID
      name: String
      description: String
      period: String
      coverage: String
      locations: [String]
      days: Integer
      quantity: Integer
      unit_price: String
      total: String
      notes: [String]
    </Service>

    <FeeBreakdown>
      uid: ID
      event: String
      fee: String
    </FeeBreakdown>

    <Signature>
      uid: ID
      type: String
      name: String
      title: String
      date: Date
    </Signature>

    <ServiceLevelAgreement>
      uid: ID
      name: String
      description: String
      target: String
      metric: String
      unit: String
      frequency: String
      applies_to: [String]
      penalty_clause: String
      enforcement_method: String
    </ServiceLevelAgreement>

    <EngagementScope>
      uid: ID
      core_applications: [String]
      supporting_applications: [String]
      key_activities: [String]
      assumptions: [String]
      expectations: [String]
      conditions: [String]
    </EngagementScope>

    <Initiative>
      uid: ID
      name: String
      description: String
    </Initiative>

    <Project>
      uid: ID
      name: String
      description: String
      start_date: Date
      end_date: Date
      status: String
    </Project>

    <DeliverableAndInvoice>
      uid: ID
      deliverable: String
      delivery_date: Date
      invoice_amount_usd: Float
      percentage: Float
    </DeliverableAndInvoice>

    <Party>
      uid: ID
      name: String
      type: String
      address: String
      context: String
    </Party>

    <CanonicalService>
      uid: ID
      name: String
      description: String
    </CanonicalService>

    <CanonicalRole>
      uid: ID
      name: String
      description: String
    </CanonicalRole>

    <CanonicalPerson>
      uid: ID
      name: String
    </CanonicalPerson>

    <CanonicalVendor>
      uid: ID
      name: String
    </CanonicalVendor>

    <CanonicalLocation>
      uid: ID
      name: String
      address: String
      city: String
      state: String
      country: String
      continent: String
    </CanonicalLocation>

    <CanonicalDivision>
      uid: ID
      name: String
    </CanonicalDivision>
  </NODES>

  <RELATIONSHIPS>
    Contract HAS_FEE_BREAKDOWN → FeeBreakdown
    Contract SIGNED_BY → Signature
    Contract INCLUDES_SERVICE → Service
    Contract INCLUDES_ROLE → Role
    Contract GOVERNED_BY_SLA → ServiceLevelAgreement
    Contract HAS_ENGAGEMENT_SCOPE → EngagementScope
    Contract ASSOCIATED_WITH_INITIATIVE → Initiative
    Contract ASSOCIATED_WITH_PROJECT → Project
    Contract HAS_DELIVERABLE_INVOICE → DeliverableAndInvoice
    Contract INVOLVES_PARTY → Party
    Contract IS_WITH_VENDOR → CanonicalVendor
    Contract IS_FOR_DIVISION → CanonicalDivision

    Role IS_CANONICAL_ROLE → CanonicalRole
    Role ASSIGNED_TO → CanonicalPerson
    Role LOCATED_AT → CanonicalLocation

    Service IS_CANONICAL_SERVICE → CanonicalService
    Service PROVIDED_AT → CanonicalLocation

    Signature IS_CANONICAL_PERSON → CanonicalPerson

    Party IS_CANONICAL_PERSON → CanonicalPerson
    Party LOCATED_AT → CanonicalLocation
  </RELATIONSHIPS>
</SCHEMA>

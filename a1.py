Group the role names into the appropriate Role Groups.

You will receive a list of raw role names. Your task is to assign each role to a valid ROLE_GROUP from the provided list.

Return the result as a JSON array of objects.

Each object must contain:

"role_group": the name of the group (must match one of the ROLE_GROUPS exactly)

"matches": a list of role names assigned to that group

Guidelines:

You must use one of the provided ROLE_GROUP values — do not invent new groups.

Choose the closest match based on the meaning of the role title.

Only use "Other" if no suitable group exists.

Ensure all roles are placed in one of the categories — none should be left out.

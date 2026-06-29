---
name: naming-convention
description: Help the user choose, validate, or rename infrastructure resource names using a well known naming convention. Use when the user says "name this", "what should I call this", "rename this", asks for a hostname or DNS name, or wants to check whether a
proposed name follows the convention. Also use this skill whenever a task clearly involves naming consistency, even if the user does not explicitly mention "naming convention".
---

# Naming Convention

Use this skill to turn vague naming requests into convention-compliant names.

## When to use

Use this skill when the user:

- asks for a name for a server, host, DNS entry, or similar infrastructure resource
- asks whether an existing name follows the convention
- asks to rename something to match the standard
- asks what an environment code, purpose code, or pattern segment should be
- needs multiple candidate names that all stay consistent with the same convention

If the task is clearly about naming consistency, apply this skill even if the user does not explicitly say "naming convention".

## Source of truth

If the user's target resource is outside the documented scope, say so clearly and ask the user for their team's convention rather than guessing.

## Inputs to gather

Ask only for the missing inputs.

For the global naming pattern, gather:

- `project`
- `datacenter`
- `purpose`
- `number`

For the DNS naming pattern, gather:

- `project`
- `datacenter`
- `dns_domain`

Ask concise follow-up questions when required.

### Required clarifications for the global pattern

Ask the user for:

1. **Project**
   Short project identifier.

2. **Datacenter**
   The datacenter code to use.

3. **Purpose**
   Must map to one approved purpose code.

4. **Number**
   A unique number for this resource.

### Required clarifications for the DNS pattern

Ask the user for:

1. **Project**
2. **Datacenter**
3. **DNS domain**

## Patterns

Use these canonical patterns exactly.

### Global naming pattern

```text
[project]-[datacenter]-[purpose]-[number]
```

### DNS naming pattern

```text
[project].[datacenter].[dns_domain]
```

Approved purpose codes

Use only these approved purpose codes unless the user explicitly tells you their team has extended the list:

- app — application server
- bkt — storage bucket
- cfg — configuration management server
- dns — name server
- fwl — firewall
- ftp — SFTP server
- lb — load balancer server
- mon — monitoring server
- pdu — power distribution unit
- prx — proxy server
- rtr — router
- sql — database server
- ssh — SSH jump or bastion host
- sto — storage server
- swt — switch
- ups — uninterruptible power supply
- vcs — version control software server
- vpn — VPN server
- web — web server

If the user's purpose does not clearly map to one of these codes, ask before inventing a new code.

## Output format

When you have enough information, present the answer in this format.

### For a proposed name

Proposed name

```text
<final-name>
```

┌──────────────────────────┬─────────┬───────────┐
│ Segment │ Value │ Meaning │
├──────────────────────────┼─────────┼───────────┤
│ project │ <value> │ <meaning> │
├──────────────────────────┼─────────┼───────────┤
│ datacenter or dns_domain │ <value> │ <meaning> │
├──────────────────────────┼─────────┼───────────┤
│ purpose │ <value> │ <meaning> │
├──────────────────────────┼─────────┼───────────┤
│ number │ <value> │ <meaning> │
└──────────────────────────┴─────────┴───────────┘

Validation: <short statement saying whether it matches the convention and any remaining caveats>

If helpful, include up to 2 alternatives and explain why they differ.

### For validation of an existing name

Use this format:

Name checked

```text
<name-to-validate>
```

Result: valid or invalid

Reasoning:

- <reason 1>
- <reason 2>

Suggested correction
If invalid, provide the closest compliant version.

Validation checklist

Before finalizing a name, check all of the following:

- uses lowercase only unless the user explicitly says otherwise
- uses hyphen separators for the global pattern
- uses dot separators for the DNS pattern
- uses an approved purpose code
- includes all required segments in the correct order
- uses a number that is unique within the relevant group: (project, datacenter, purpose) for the global pattern
- does not invent missing values without asking

If any required field is missing, stop and ask for it instead of guessing.

## Examples

### Example 1 — Global naming pattern

Input:

- project: atlas
- datacenter: dc1
- purpose: web
- number: 01

Output:

Proposed name

```text
atlas-dc1-web-01
```

┌────────────┬─────────┬────────────────────────┐
│ Segment │ Value │ Meaning │
├────────────┼─────────┼────────────────────────┤
│ project │ atlas │ Project identifier │
├────────────┼─────────┼────────────────────────┤
│ datacenter │ dc1 │ Datacenter code │
├────────────┼─────────┼────────────────────────┤
│ purpose │ web │ Web server │
├────────────┼─────────┼────────────────────────┤
│ number │ 01 │ Unique instance number │
└────────────┴─────────┴────────────────────────┘

Validation: matches the canonical global naming pattern.

### Example 2 — DNS naming pattern

Input:

- project: atlas
- datacenter: dc1
- dns_domain: example.com

Output:

Proposed name

```text
atlas.dc1.example.com
```

┌────────────┬─────────────┬───────────────────────────────────────┐
│ Segment │ Value │ Meaning │
├────────────┼─────────────┼───────────────────────────────────────┤
│ project │ atlas │ Project identifier │
├────────────┼─────────────┼───────────────────────────────────────┤
│ env │ dc1 │ Production environment for DNS naming │
├────────────┼─────────────┼───────────────────────────────────────┤
│ dns_domain │ example.com │ DNS domain │
└────────────┴─────────────┴───────────────────────────────────────┘

Validation: matches the canonical DNS naming pattern.

## Out-of-scope resources

For resources not covered by the canonical patterns, such as cloud buckets, Kubernetes namespaces, or GitHub repositories, do not guess a convention.

Instead:

1. tell the user that the current canonical cheatsheet does not define a pattern for that resource type
2. ask whether their team has a specific convention
3. if they want, help them draft one explicitly instead of pretending one already exists

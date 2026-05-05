# Screenshots Guide — Evidence Document Mapping

Region: ap-south-1 (Mumbai)
Console Base URL: https://ap-south-1.console.aws.amazon.com

---

## REL-001 — Deployment Automation & IaC

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 1 | `REL001_01_cfn_root_stack.png` | Section 2 — CloudFormation Nested Stack Structure | CloudFormation → Stacks → `{client}-copilot` (shows root + 6 nested stacks) |
| 2 | `REL001_02_cfn_stack_resources.png` | Section 2 — CloudFormation Nested Stack Structure | CloudFormation → Stacks → `{client}-copilot` → Resources tab |
| 3 | `REL001_03_cfn_stack_outputs.png` | Section 2 — CloudFormation Nested Stack Structure | CloudFormation → Stacks → `{client}-copilot` → Outputs tab |
| 4 | `REL001_04_cfn_stack_parameters.png` | Section 2 — CloudFormation Nested Stack Structure | CloudFormation → Stacks → `{client}-copilot` → Parameters tab (shows ClientName) |
| 5 | `REL001_05_cfn_nested_list.png` | Section 2 — CloudFormation Nested Stack Structure | CloudFormation → Stacks → filter "NESTED" (shows all 6 child stacks) |

---

## NETSEC-001 — VPC & Network Security

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 6 | `NETSEC001_01_vpc_overview.png` | Section 3.1 — VPC Architecture | VPC → Your VPCs → `{client}-copilot-vpc` (shows CIDR 10.1.0.0/16) |
| 7 | `NETSEC001_02_subnets.png` | Section 3.1 — VPC Architecture | VPC → Subnets → filter by VPC (shows 4 subnets with CIDRs and AZs) |
| 8 | `NETSEC001_03_igw.png` | Section 3.1 — VPC Architecture | VPC → Internet Gateways → `{client}-copilot-igw` (shows attached to VPC) |
| 9 | `NETSEC001_04_route_tables.png` | Section 3.1 — VPC Architecture | VPC → Route Tables → filter by VPC (shows public-rt with 0.0.0.0/0 → IGW) |
| 10 | `NETSEC001_05_nacl_private.png` | Section 3.3 — Network ACLs Implemented | VPC → Network ACLs → `{client}-nacl-private` → Inbound Rules tab |
| 11 | `NETSEC001_06_nacl_outbound.png` | Section 3.3 — Network ACLs Implemented | VPC → Network ACLs → `{client}-nacl-private` → Outbound Rules tab |
| 12 | `NETSEC001_07_sg_list.png` | Section 3.2 — Security Groups Implemented | VPC → Security Groups → filter by VPC (shows all 8 SGs) |
| 13 | `NETSEC001_08_sg_alb_rules.png` | Section 3.2 — Security Groups Implemented | VPC → Security Groups → `{client}-sg-alb` → Inbound Rules tab |
| 14 | `NETSEC001_09_sg_copilot_rules.png` | Section 3.2 — Security Groups Implemented | VPC → Security Groups → `{client}-sg-copilot-svc` → Inbound Rules tab |
| 15 | `NETSEC001_10_sg_vpce_bedrock.png` | Section 3.2 — Security Groups Implemented | VPC → Security Groups → `{client}-sg-vpce-bedrock` → Inbound Rules tab |
| 16 | `NETSEC001_11_s3_endpoint.png` | Section 3.4 — Additional Network Security | VPC → Endpoints → S3 Gateway endpoint (shows route table association) |

---

## NETSEC-002 — Data Encryption & Key Management

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 17 | `NETSEC002_01_kms_key_list.png` | Section 3.4 — KMS Key Inventory | KMS → Customer managed keys (shows all 7 keys with aliases) |
| 18 | `NETSEC002_02_kms_s3_key.png` | Section 3.3 — Encryption at Rest | KMS → `{client}-s3-key` → Key details (shows rotation enabled) |
| 19 | `NETSEC002_03_kms_ddb_key.png` | Section 3.3 — Encryption at Rest | KMS → `{client}-ddb-key` → Key details |
| 20 | `NETSEC002_04_s3_encryption.png` | Section 3.3 — Encryption at Rest | S3 → `{client}-knowledge-base-{acct}` → Properties → Default encryption (shows SSE-KMS) |
| 21 | `NETSEC002_05_s3_versioning.png` | Section 3.3 — Encryption at Rest | S3 → `{client}-knowledge-base-{acct}` → Properties → Bucket Versioning (shows Enabled) |
| 22 | `NETSEC002_06_s3_public_access.png` | Section 3.3 — Encryption at Rest | S3 → `{client}-knowledge-base-{acct}` → Permissions → Block public access (shows all blocked) |
| 23 | `NETSEC002_07_ddb_encryption.png` | Section 3.3 — Encryption at Rest | DynamoDB → Tables → `{client}-tenant-config` → Additional settings → Encryption (shows KMS CMK) |

---

## ACCT-001 — Secure AWS Account Governance

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 24 | `ACCT001_01_root_mfa.png` | Section 4 — MFA on Root | IAM → Dashboard → Security recommendations (shows "Root user MFA" status) |
| 25 | `ACCT001_02_cloudtrail_enabled.png` | Section 4 — CloudTrail in All Regions | CloudTrail → Trails (shows existing trail with multi-region = Yes) |

---

## ACCT-002 — Identity Security / IAM

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 26 | `ACCT002_01_iam_roles_list.png` | Section 4.3 — Workload IAM | IAM → Roles → search `{client}` (shows all 4 roles) |
| 27 | `ACCT002_02_task_role_policy.png` | Section 4.3 — Workload IAM | IAM → Roles → `{client}-ecs-copilot-task-role` → Permissions (shows CopilotPolicy) |
| 28 | `ACCT002_03_task_role_trust.png` | Section 4.3 — Workload IAM | IAM → Roles → `{client}-ecs-copilot-task-role` → Trust relationships |
| 29 | `ACCT002_04_ingest_role_policy.png` | Section 4.3 — Workload IAM | IAM → Roles → `{client}-lambda-ingest-role` → Permissions |
| 30 | `ACCT002_05_deploy_role.png` | Section 4.3 — Workload IAM | IAM → Roles → `{client}-github-deploy-role` → Trust relationships |
| 31 | `ACCT002_06_cognito_pool.png` | Section 4.2 — Multi-Tenant Authentication | Cognito → User pools → `{client}-tenant-pool` → Overview |
| 32 | `ACCT002_07_cognito_mfa.png` | Section 4.2 — Multi-Tenant Authentication | Cognito → `{client}-tenant-pool` → Sign-in experience → MFA (shows Required) |
| 33 | `ACCT002_08_cognito_attributes.png` | Section 4.2 — Multi-Tenant Authentication | Cognito → `{client}-tenant-pool` → Sign-up experience → Custom attributes (shows tenant_id) |
| 34 | `ACCT002_09_cognito_app_client.png` | Section 4.2 — Multi-Tenant Authentication | Cognito → `{client}-tenant-pool` → App integration → App clients (shows copilot-client) |

---

## AGAIPS-001 — Agentic AI Practice Implementation

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 35 | `AGAIPS001_01_bedrock_models.png` | Section 3 — FM Selection Rationale | Bedrock → Model access (shows Claude Sonnet 4, Nova Pro, Titan Embeddings enabled) |
| 36 | `AGAIPS001_02_bedrock_playground.png` | Section 3 — FM Selection Rationale | Bedrock → Chat playground → select Claude Sonnet 4 (shows model available) |

---

## AGAIPS-002 — Security & Interoperability

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 37 | `AGAIPS002_01_cognito_tenant_id.png` | Section 3 — Authentication Design | Same as ACCT002_08 — Cognito custom attributes showing tenant_id |
| 38 | `AGAIPS002_02_sg_copilot_inbound.png` | Section 6 — Network Security | Same as NETSEC001_09 — sg-copilot-svc inbound rules |

> Note: Reuse ACCT-002 and NETSEC-001 screenshots — no new screenshots needed.

---

## AGAIPS-003 — Responsible AI Practice

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 39 | `AGAIPS003_01_guardrail_overview.png` | Section 3 — Safety Controls | Bedrock → Guardrails → `{client}-copilot-guardrail` → Overview |
| 40 | `AGAIPS003_02_guardrail_content.png` | Section 3 — Safety Controls | Bedrock → Guardrails → `{client}-copilot-guardrail` → Content filters tab |
| 41 | `AGAIPS003_03_guardrail_pii.png` | Section 3 — Safety Controls | Bedrock → Guardrails → `{client}-copilot-guardrail` → Sensitive information tab |
| 42 | `AGAIPS003_04_guardrail_topics.png` | Section 3 — Safety Controls | Bedrock → Guardrails → `{client}-copilot-guardrail` → Denied topics tab |
| 43 | `AGAIPS003_05_guardrail_words.png` | Section 3 — Safety Controls | Bedrock → Guardrails → `{client}-copilot-guardrail` → Word filters tab |

---

## AGAIPS-004 — Compute Practice Implementation

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 44 | `AGAIPS004_01_ecs_cluster.png` | Section 4 — Compute Architecture | ECS → Clusters → `{client}-copilot` → Overview |
| 45 | `AGAIPS004_02_task_def.png` | Section 4 — Compute Architecture | ECS → Task definitions → `{client}-copilot-svc` → Latest revision |
| 46 | `AGAIPS004_03_task_def_container.png` | Section 4 — Compute Architecture | ECS → Task definitions → `{client}-copilot-svc` → Container definitions (shows 1 vCPU, 2 GB, port 8080) |
| 47 | `AGAIPS004_04_task_def_env.png` | Section 4 — Compute Architecture | ECS → Task definitions → `{client}-copilot-svc` → Environment variables (shows model IDs) |
| 48 | `AGAIPS004_05_ecr_repo.png` | Section 6 — Deployment Guide | ECR → Repositories → `{client}-copilot` (shows repo with KMS encryption) |

---

## OPE-001 — Workload Health KPIs

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 49 | `OPE001_01_dashboard.png` | Section 3.1 — CloudWatch Dashboard | CloudWatch → Dashboards → `{client}-copilot-dashboard` |
| 50 | `OPE001_02_alarms_list.png` | Section 3.3 — Alerting Configuration | CloudWatch → Alarms → filter `{client}` (shows 3 alarms) |
| 51 | `OPE001_03_alarm_cpu.png` | Section 3.3 — Alerting Configuration | CloudWatch → Alarms → `{client}-ecs-cpu-high` → Details |
| 52 | `OPE001_04_log_groups.png` | Section 3.2 — Application Logs | CloudWatch → Log groups → filter `{client}` (shows 4 log groups) |

---

## DynamoDB Screenshots (used across multiple evidence docs)

| # | Screenshot Name | Evidence Section | Console Path |
|---|---|---|---|
| 53 | `DATA_01_ddb_tables.png` | NETSEC-002 Section 3.3, AGAIPS-002 Section 4 | DynamoDB → Tables (shows 3 tables: tenant-config, interaction-history, feedback-log) |
| 54 | `DATA_02_ddb_pitr.png` | REL-002 Section 3.3 | DynamoDB → `{client}-tenant-config` → Backups → Point-in-time recovery (shows Enabled) |
| 55 | `DATA_03_ddb_schema.png` | AGAIPS-002 Section 4 | DynamoDB → `{client}-interaction-history` → Overview (shows partition key: tenant_id) |

---

## Summary

| Evidence Doc | Screenshots Needed | New Screenshots | Reused From |
|---|---|---|---|
| REL-001 | 5 | 5 | — |
| NETSEC-001 | 11 | 11 | — |
| NETSEC-002 | 7 | 7 | — |
| ACCT-001 | 2 | 2 (from existing account) | — |
| ACCT-002 | 9 | 9 | — |
| AGAIPS-001 | 2 | 2 | — |
| AGAIPS-002 | 2 | 0 | ACCT-002, NETSEC-001 |
| AGAIPS-003 | 5 | 5 | — |
| AGAIPS-004 | 5 | 5 | — |
| OPE-001 | 4 | 4 | — |
| DynamoDB | 3 | 3 | — |
| **Total** | **55** | **53 unique** | |

> Replace `{client}` with your ClientName from config.yaml (e.g., `cust03`).
> Replace `{acct}` with your AWS account ID.

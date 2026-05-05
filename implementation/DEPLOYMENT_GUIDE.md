# Deployment Guide — GenAI Copilot (Evidence Screenshots)

---

## Prerequisites

### 1. AWS CLI installed and configured

```bash
# Check if installed
aws --version

# If not installed, download from:
# https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
```

### 2. AWS CLI configured with ap-south-1 credentials

```bash
aws configure
# AWS Access Key ID:     <your-access-key>
# AWS Secret Access Key: <your-secret-key>
# Default region name:   ap-south-1
# Default output format: json
```

### 3. Verify your identity

```bash
aws sts get-caller-identity
```
You should see your Account ID, ARN, and UserId.

### 4. Python 3.8+ with PyYAML

```bash
python --version
pip install pyyaml
```

### 5. IAM Permissions required

Your IAM user/role needs these permissions:
- `cloudformation:*` (create/delete stacks)
- `s3:*` (CFN artifact bucket + knowledge-base bucket)
- `ec2:*` (VPC, subnets, SGs, NACLs, endpoints)
- `kms:*` (create/delete CMKs)
- `dynamodb:*` (create/delete tables)
- `cognito-idp:*` (user pool)
- `ecs:*` (cluster, task definitions)
- `ecr:*` (repository)
- `bedrock:*` (guardrail)
- `logs:*` (log groups)
- `cloudwatch:*` (dashboard, alarms)
- `iam:*` (roles, policies)

> Simplest option: Use an IAM user with `AdministratorAccess` policy for the deployment session. Revoke after screenshots.

---

## Step 1 — Set your client name

Open `implementation/config.yaml` and set your client name:

```yaml
ClientName: cust03          # ← Change this to your client name
Region: ap-south-1
CfnBucket: cust03-cfn-artifacts  # ← Update prefix to match ClientName
```

**Examples:**
| If ClientName is | Resources will be named |
|---|---|
| `cust03` | `cust03-copilot-vpc`, `cust03-tenant-config`, `cust03-sg-alb` ... |
| `webner` | `webner-copilot-vpc`, `webner-tenant-config`, `webner-sg-alb` ... |
| `acme` | `acme-copilot-vpc`, `acme-tenant-config`, `acme-sg-alb` ... |

> **Important:** Also update `CfnBucket` to match. S3 bucket names must be globally unique. If `cust03-cfn-artifacts` is taken, use `cust03-cfn-artifacts-{your-account-id}`.

---

## Step 2 — Deploy

Run from the project root directory:

```bash
python implementation/deploy.py deploy
```

**What happens:**
1. Creates an S3 bucket (`{ClientName}-cfn-artifacts`) for nested template upload
2. Packages all 6 nested YAML templates and uploads them to S3
3. Deploys the root CloudFormation stack with all 6 nested stacks

**Expected output:**
```
============================================================
  DEPLOYING:  cust03-copilot
  Region:     ap-south-1
  Client:     cust03
  CFN Bucket: cust03-cfn-artifacts
============================================================

[1/3] Ensuring CFN artifacts bucket ...
[2/3] Packaging nested templates ...
[3/3] Deploying stack ...

============================================================
  DEPLOY COMPLETE: cust03-copilot
  Console: https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1
  Destroy: python implementation/deploy.py destroy
============================================================
```

**Deployment time:** ~5-8 minutes.

---

## Step 3 — Verify in AWS Console

Open the CloudFormation console link printed at the end of deploy.

You should see:

```
cust03-copilot                    CREATE_COMPLETE    (root stack)
├── cust03-copilot-VpcStack       CREATE_COMPLETE
├── cust03-copilot-DataStack      CREATE_COMPLETE
├── cust03-copilot-AuthStack      CREATE_COMPLETE
├── cust03-copilot-EcsStack       CREATE_COMPLETE
├── cust03-copilot-BedrockStack   CREATE_COMPLETE
└── cust03-copilot-MonitoringStack CREATE_COMPLETE
```

If any stack shows `CREATE_FAILED`, click on it → Events tab to see the error.

---

## Step 4 — Take screenshots

Follow `SCREENSHOTS_GUIDE.md` for the exact console paths.

**Quick console links (replace `cust03` with your ClientName):**

| Service | URL |
|---|---|
| CloudFormation | `https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1` |
| VPC | `https://ap-south-1.console.aws.amazon.com/vpcconsole/home?region=ap-south-1` |
| DynamoDB | `https://ap-south-1.console.aws.amazon.com/dynamodbv2/home?region=ap-south-1#tables` |
| S3 | `https://s3.console.aws.amazon.com/s3/home?region=ap-south-1` |
| KMS | `https://ap-south-1.console.aws.amazon.com/kms/home?region=ap-south-1#/kms/keys` |
| Cognito | `https://ap-south-1.console.aws.amazon.com/cognito/v2/home?region=ap-south-1` |
| ECS | `https://ap-south-1.console.aws.amazon.com/ecs/v2/clusters?region=ap-south-1` |
| ECR | `https://ap-south-1.console.aws.amazon.com/ecr/repositories?region=ap-south-1` |
| Bedrock Guardrails | `https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/guardrails` |
| CloudWatch Dashboards | `https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#dashboards` |
| CloudWatch Alarms | `https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#alarmsV2` |
| IAM Roles | `https://console.aws.amazon.com/iam/home#/roles` |

---

## Step 5 — Destroy (after screenshots)

```bash
python implementation/deploy.py destroy
```

**What happens:**
1. Empties the S3 knowledge-base bucket (CloudFormation can't delete non-empty buckets)
2. Deletes the root CloudFormation stack (cascades to all 6 nested stacks)
3. Removes the CFN artifacts S3 bucket
4. Deletes the local `packaged.yaml` file

**Expected output:**
```
============================================================
  DESTROYING: cust03-copilot
============================================================

[1/3] Emptying S3 bucket ...
[2/3] Deleting CloudFormation stack ...
  Waiting for deletion ...
[3/3] Cleaning up CFN artifacts bucket ...

============================================================
  DESTROY COMPLETE: cust03-copilot
  KMS keys scheduled for deletion (7-day AWS minimum)
============================================================
```

**Deletion time:** ~5-10 minutes.

---

## Troubleshooting

### "S3 bucket name already exists"
S3 bucket names are globally unique. Change `CfnBucket` in `config.yaml`:
```yaml
CfnBucket: cust03-cfn-artifacts-123456789012   # append your account ID
```

### "Stack creation failed — security group name already exists"
Security group names must be unique per VPC. If you had a previous failed deploy, delete the leftover stack first:
```bash
aws cloudformation delete-stack --stack-name cust03-copilot --region ap-south-1
aws cloudformation wait stack-delete-complete --stack-name cust03-copilot --region ap-south-1
```
Then deploy again.

### "Bedrock Guardrail creation failed"
Bedrock Guardrails may not be available in all regions. Verify ap-south-1 supports it:
```bash
aws bedrock list-guardrails --region ap-south-1
```
If not supported, you can comment out the BedrockStack in `main.yaml` and create the guardrail manually in a supported region for the screenshot.

### "Delete failed — bucket not empty"
If destroy fails on S3, manually empty and delete:
```bash
aws s3 rb s3://cust03-knowledge-base-123456789012 --force --region ap-south-1
```
Then re-run destroy.

### "KMS keys still visible after destroy"
KMS keys have a mandatory 7-day waiting period before deletion. They'll show as "Pending deletion" in the console. This is normal — they'll auto-delete after 7 days and cost nothing while pending.

---

## Cost Summary

| Resource | Cost | Notes |
|---|---|---|
| VPC, Subnets, IGW, SGs, NACLs | $0 | Free |
| S3 Gateway Endpoint | $0 | Free |
| DynamoDB (3 tables, on-demand) | $0 | Free tier / no reads or writes |
| S3 Buckets (empty) | $0 | No storage used |
| Cognito User Pool | $0 | Free tier (no users) |
| ECS Cluster + Task Def | $0 | No running tasks |
| ECR Repository (empty) | $0 | No images stored |
| Bedrock Guardrail | $0 | Free to create |
| CloudWatch Dashboard | $0 | First 3 dashboards free |
| CloudWatch Alarms | $0 | First 10 alarms free |
| CloudWatch Log Groups | $0 | No log data |
| IAM Roles | $0 | Free |
| **KMS Keys (7)** | **~$7/month** | **$1/key/month, prorated. Scheduled for deletion on destroy.** |
| **Total for a 1-hour screenshot session** | **< $0.25** | |

---

## Files Reference

```
implementation/
├── config.yaml          ← Change ClientName here
├── deploy.py            ← Deploy and destroy script
├── main.yaml            ← Root stack (orchestrates 6 nested stacks)
├── vpc.yaml             ← VpcStack: VPC, subnets, IGW, NACLs, 8 SGs, S3 endpoint
├── data.yaml            ← DataStack: 7 KMS CMKs, 3 DynamoDB tables, S3 bucket, ECR
├── auth.yaml            ← AuthStack: Cognito User Pool (tenant_id, MFA)
├── ecs.yaml             ← EcsStack: ECS cluster, task def, 4 IAM roles
├── bedrock.yaml         ← BedrockStack: Guardrail (PII, content, topics)
├── monitoring.yaml      ← MonitoringStack: 4 log groups, dashboard, 3 alarms
├── SCREENSHOTS_GUIDE.md ← Screenshot-to-evidence mapping
└── DEPLOYMENT_GUIDE.md  ← This file
```

"""
Deploy / Destroy the Copilot CloudFormation nested stacks.

Usage:
  python implementation/deploy.py deploy
  python implementation/deploy.py destroy

Reads ClientName from implementation/config.yaml.
Prereqs: AWS CLI configured, pip install pyyaml.
"""
import yaml
import subprocess
import sys
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
with open(CONFIG_FILE) as f:
    CFG = yaml.safe_load(f)

CLIENT = CFG["ClientName"]
REGION = CFG.get("Region", "ap-south-1")
STACK_NAME = f"{CLIENT}-copilot"
CFN_BUCKET = CFG.get("CfnBucket", f"{CLIENT}-cfn-artifacts")
IMPL_DIR = os.path.dirname(os.path.abspath(__file__))


def run(cmd, check=True):
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr.strip():
        print(result.stderr.strip())
    if result.returncode != 0 and check:
        sys.exit(1)
    return result.returncode


def deploy():
    print(f"\n{'='*60}")
    print(f"  DEPLOYING:  {STACK_NAME}")
    print(f"  Region:     {REGION}")
    print(f"  Client:     {CLIENT}")
    print(f"  CFN Bucket: {CFN_BUCKET}")
    print(f"{'='*60}\n")

    print("[1/3] Ensuring CFN artifacts bucket ...")
    run(f"aws s3 mb s3://{CFN_BUCKET} --region {REGION}", check=False)

    print("[2/3] Packaging nested templates ...")
    packaged = os.path.join(IMPL_DIR, "packaged.yaml")
    main_tpl = os.path.join(IMPL_DIR, "main.yaml")
    rc = run(
        f"aws cloudformation package"
        f" --template-file {main_tpl}"
        f" --s3-bucket {CFN_BUCKET}"
        f" --output-template-file {packaged}"
        f" --region {REGION}"
    )
    if rc != 0:
        return

    print("[3/3] Deploying stack ...")
    run(
        f"aws cloudformation deploy"
        f" --template-file {packaged}"
        f" --stack-name {STACK_NAME}"
        f" --capabilities CAPABILITY_NAMED_IAM"
        f" --region {REGION}"
        f" --parameter-overrides ClientName={CLIENT}"
        f" --tags Project={STACK_NAME} Client={CLIENT}"
        f" --no-fail-on-empty-changeset"
    )

    url = f"https://{REGION}.console.aws.amazon.com/cloudformation/home?region={REGION}"
    print(f"\n{'='*60}")
    print(f"  DEPLOY COMPLETE: {STACK_NAME}")
    print(f"  Console: {url}")
    print(f"  Destroy: python implementation/deploy.py destroy")
    print(f"{'='*60}\n")


def destroy():
    print(f"\n{'='*60}")
    print(f"  DESTROYING: {STACK_NAME}")
    print(f"{'='*60}\n")

    # Get account ID for bucket name
    acct = subprocess.run(
        "aws sts get-caller-identity --query Account --output text",
        shell=True, capture_output=True, text=True,
    ).stdout.strip()

    # Empty S3 bucket (CFN can't delete non-empty)
    print("[1/3] Emptying S3 bucket ...")
    bucket = f"{CLIENT}-knowledge-base-{acct}"
    run(f"aws s3 rm s3://{bucket} --recursive --region {REGION}", check=False)

    # Delete stack
    print("[2/3] Deleting CloudFormation stack ...")
    run(f"aws cloudformation delete-stack --stack-name {STACK_NAME} --region {REGION}")
    print("  Waiting for deletion ...")
    run(f"aws cloudformation wait stack-delete-complete --stack-name {STACK_NAME} --region {REGION}")

    # Cleanup CFN bucket
    print("[3/3] Cleaning up CFN artifacts bucket ...")
    run(f"aws s3 rb s3://{CFN_BUCKET} --force --region {REGION}", check=False)

    packaged = os.path.join(IMPL_DIR, "packaged.yaml")
    if os.path.exists(packaged):
        os.remove(packaged)

    print(f"\n{'='*60}")
    print(f"  DESTROY COMPLETE: {STACK_NAME}")
    print(f"  KMS keys scheduled for deletion (7-day AWS minimum)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("deploy", "destroy"):
        print("Usage: python implementation/deploy.py deploy|destroy")
        sys.exit(1)
    {"deploy": deploy, "destroy": destroy}[sys.argv[1]]()

# Project Updates (Fork Enhancements)

This fork contains several critical enhancements and modernizations over the original repository.

## Key Changes

### 1. Cloud Functions Gen 2 Upgrade
The Cloud Function has been upgraded from Gen 1 to **Gen 2 (Cloud Run Functions)**. 
- **Platform:** Now runs on Google Cloud Run for better scalability and performance.
- **Trigger:** Uses **Eventarc** to listen to Pub/Sub events, following Google's modern architectural standards.
- **Memory:** Increased default available memory to **256MB** for more robust execution.

### 2. Python Runtime Update
- **Version:** Upgraded to **Python 3.14**.
- **Security:** Ensures long-term support and addresses security vulnerabilities in older runtimes.

### 3. Remote Terraform Backend (GCS)
The project is now configured to store its infrastructure state safely. The `backend "gcs" {}` block was added to `main.tf`.
- **Benefits:**
    - **Persistence:** State is safely stored in GCP, not just on a local machine.
    - **Collaboration:** Multiple users or machines can now initialize the project and manage the infrastructure concurrently.

### 4. Terraform Variables for Project and Bucket
To make the deployment fully dynamic and reproducible across environments without hardcoding, the configuration now strictly relies on Terraform variables:
- **`project_id`**: The Google Cloud project to deploy resources to.
- **`bucket_name`**: A new variable added to customize the GCS bucket used for storing the Cloud Function's source code (replacing the old behavior that used a random ID).

### 5. Custom IAM Role & Permissions Fixes
- Added necessary IAM policy bindings to ensure that the **Cloud Build service account** has the correct permissions to deploy the function.
- Added permissions for **Eventarc** and **Pub/Sub Service Agent** to correctly handle event triggers in the Gen 2 architecture.

---

## How to Initialize and Deploy in a New Environment

If you clone this project to a new machine or a new Cloud Shell session, you need to provide your backend configuration and Terraform variables.

**1. Set your GCP project:**
```bash
gcloud config set project YOUR_PROJECT_ID
```

**2. Create a GCS bucket for the Terraform state:**
Before initializing Terraform with a remote state, you must create the bucket in your Google Cloud project using `gcloud`.

```bash
gcloud storage buckets create gs://YOUR_TERRAFORM_STATE_BUCKET_NAME \
  --location=us-central1 \
  --project=YOUR_PROJECT_ID

# (Optional but recommended) Enable versioning to keep history of your state
gcloud storage buckets update gs://YOUR_TERRAFORM_STATE_BUCKET_NAME --versioning
```

**3. Initialize Terraform (connecting it to your remote GCS state bucket):**
```bash
terraform init -backend-config="bucket=YOUR_TERRAFORM_STATE_BUCKET_NAME"
```

**4. Apply the changes with your variables:**
```bash
terraform apply \
  -var="project_id=YOUR_PROJECT_ID" \
  -var="bucket_name=YOUR_FUNCTION_SOURCE_BUCKET_NAME" \
  -var="target_amount=50"
```

> **Note:** Do not commit any local `.tfvars`, `.terraform.lock.hcl`, or tfenv variable files to the repository to keep your environment-specific data secure.

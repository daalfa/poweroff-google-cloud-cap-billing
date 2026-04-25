# Project Updates (Fork Enhancements)

This fork contains several critical enhancements and modernizations over the original repository, including the highly requested ability to monitor and cap billing for **multiple projects at once**.

## Key Changes

### 1. Multi-Project Monitoring & Capping
The original repository required you to deploy the "kill switch" function and budget alert separately into every single project you wanted to monitor. 

**Now, you can monitor a combined budget for multiple projects using a single deployment.**
- The budget alert watches the combined spending of a specified list of projects.
- When the budget is exceeded, the Cloud Function iterates through your provided list and safely disables billing for *each one* of the monitored projects.
- This allows you to group related projects under one shared budget cap while explicitly excluding others (like production environments).

### 2. Cloud Functions Gen 2 Upgrade
The Cloud Function has been upgraded from Gen 1 to **Gen 2 (Cloud Run Functions)**. 
- **Platform:** Now runs on Google Cloud Run for better scalability and performance.
- **Trigger:** Uses **Eventarc** to listen to Pub/Sub events, following Google's modern architectural standards.
- **Memory:** Increased default available memory to **256MB** for more robust execution.

### 3. Python Runtime Update
- **Version:** Upgraded to **Python 3.14**.
- **Security:** Ensures long-term support and addresses security vulnerabilities in older runtimes.

### 4. Remote Terraform Backend (GCS)
The project is now configured to store its infrastructure state safely. The `backend "gcs" {}` block was added to `main.tf`.
- **Benefits:**
    - **Persistence:** State is safely stored in GCP, not just on a local machine.
    - **Collaboration:** Multiple users or machines can now initialize the project and manage the infrastructure concurrently.

### 5. Custom IAM Role & Permissions Fixes
- Added necessary IAM policy bindings to ensure that the **Cloud Build service account** has the correct permissions to deploy the function.
- Added permissions for **Eventarc** and **Pub/Sub Service Agent** to correctly handle event triggers in the Gen 2 architecture.
- The Service Account automatically grants itself the custom role in **every monitored project** to ensure it can successfully remove the billing account when triggered.

---

## How to Initialize and Deploy in a New Environment

If you clone this project to a new machine or a new Cloud Shell session, you need to provide your backend configuration and Terraform variables.

### 1. Identify Your Projects
Decide which project will host the Cloud Function and Budget Alert (`deploy_project_id`), and which projects you actually want to monitor and cap (`monitored_project_ids`).

> **Tip:** If you need to find the IDs of all projects under your organization, you can use this `gcloud` command:
> ```bash
> gcloud projects list --filter="parent.id:YOUR_ORG_ID"
> ```

### 2. Set your Deployment GCP project:
```bash
gcloud config set project YOUR_DEPLOY_PROJECT_ID
```

### 3. Create a GCS bucket for the Terraform state:
Before initializing Terraform with a remote state, you must create the bucket in your deployment project using `gcloud`.

```bash
gcloud storage buckets create gs://YOUR_TERRAFORM_STATE_BUCKET_NAME \
  --location=us-central1 \
  --project=YOUR_DEPLOY_PROJECT_ID

# (Optional but recommended) Enable versioning to keep history of your state
gcloud storage buckets update gs://YOUR_TERRAFORM_STATE_BUCKET_NAME --versioning
```

### 4. Initialize Terraform (connecting it to your remote GCS state bucket):
```bash
terraform init -backend-config="bucket=YOUR_TERRAFORM_STATE_BUCKET_NAME"
```

### 5. Apply the changes with your variables:
When applying, you must provide the single deployment project and a list of the projects you want to monitor (formatted as a valid Terraform list of strings):

```bash
terraform apply \
  -var="deploy_project_id=YOUR_DEPLOY_PROJECT_ID" \
  -var='monitored_project_ids=["project-id-1", "project-id-2"]' \
  -var="bucket_name=YOUR_FUNCTION_SOURCE_BUCKET_NAME" \
  -var="target_amount=50"
```

> **Note:** Do not commit any local `.tfvars`, `.terraform.lock.hcl`, or tfenv variable files to the repository to keep your environment-specific data secure.

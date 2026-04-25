# Copyright 2021 Google LLC
# Copyright 2022 Nils Knieling
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

###############################################################################
# This function will remove the billing account associated
# with the projects if the cost amount is higher than the budget amount.
###############################################################################

import base64
import json
import os
import google.auth
from google.cloud import billing

# Fallback to default project if MONITORED_PROJECT_IDS is not set
DEFAULT_PROJECT_ID = google.auth.default()[1]
cloud_billing_client = billing.CloudBillingClient()


def stop_billing(event, context=None):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    # Handle CloudEvents (Gen 2) vs Background Events (Gen 1)
    if hasattr(event, 'data'):
        pubsub_data = base64.b64decode(event.data["message"]["data"]).decode("utf-8")
    elif "data" in event and "message" in event: # Gen 2 generic
        pubsub_data = base64.b64decode(event["message"]["data"]).decode("utf-8")
    else: # Gen 1 background event
        pubsub_data = base64.b64decode(event.get("data", "")).decode("utf-8")
        
    print(f"Data: {pubsub_data}")

    pubsub_json = json.loads(pubsub_data)
    cost_amount = pubsub_json["costAmount"]
    budget_amount = pubsub_json["budgetAmount"]

    if cost_amount <= budget_amount:
        print(f"No action necessary. (Current cost: {cost_amount})")
        return

    monitored_projects_env = os.getenv("MONITORED_PROJECT_IDS", "")
    if monitored_projects_env:
        project_ids = [pid.strip() for pid in monitored_projects_env.split(",") if pid.strip()]
    else:
        project_ids = [DEFAULT_PROJECT_ID]

    for project_id in project_ids:
        project_name = cloud_billing_client.common_project_path(project_id)
        try:
            request = billing.UpdateProjectBillingInfoRequest(
                name=project_name,
                project_billing_info=billing.ProjectBillingInfo(
                    billing_account_name=""  # Disable billing
                ),
            )
            project_billing_info = cloud_billing_client.update_project_billing_info(request)
            print(f"Billing disabled for project {project_id}: {project_billing_info}")
        except Exception as e:
            print(f"Failed to disable billing for project {project_id}: {e}")

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

###############################################################################
# VARIABLES
###############################################################################

variable "deploy_project_id" {
  type        = string
  nullable    = false
  description = "The project ID where the resources (function, bucket, pubsub) will be deployed"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.deploy_project_id))
    error_message = "Invalid project ID!"
  }
}

variable "monitored_project_ids" {
  type        = list(string)
  nullable    = false
  description = "A list of project IDs that will be monitored by the budget alert and unlinked from the billing account if the budget is exceeded"
  validation {
    condition     = length(var.monitored_project_ids) > 0
    error_message = "At least one project ID must be specified!"
  }
}

variable "pubsub_topic" {
  type        = string
  nullable    = false
  description = "Name of the Pub/Sub topic"
  default     = "cap-billing-alert"
}

variable "target_amount" {
  type        = number
  nullable    = false
  description = "Set maximum monthly budget amount (currency as in billing account)"
  default     = 1000
  validation {
    condition     = can(regex("^[0-9]+$", var.target_amount))
    error_message = "Specify amount as 64-bit signed integer (1 - 10000000..)!"
  }
}

variable "region" {
  type        = string
  nullable    = false
  description = "Region for the resources"
  default     = "us-central1"
}

variable "bucket_name" {
  type        = string
  nullable    = false
  description = "The GCS bucket name to store the Cloud Function source code"
}

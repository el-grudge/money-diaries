variable "project" {
  description = "Project"
  # default   = [project-name]
}

variable "app_name" {
  type        = string
  description = "Application Name"
  default     = "mage-data-prep"
}

variable "container_cpu" {
  description = "Container cpu"
  default     = "2000m"
}

variable "container_memory" {
  description = "Container memory"
  default     = "2G"
}

variable "project_id" {
  type        = string
  description = "The name of the project"
  # default = [project-id]
}

variable "region" {
  type        = string
  description = "The default compute region"
  # default   = [region]
}

variable "zone" {
  type        = string
  description = "The default compute zone"
  # default   = [zone]
}

variable "location" {
  description = "Project Location"
  # default = [location] 
}

variable "repository" {
  type        = string
  description = "The name of the Artifact Registry repository to be created"
  default     = "mage-data-prep"
}

variable "database_user" {
  type        = string
  description = "The username of the Postgres database."
  default     = "mageuser"
}

variable "database_password" {
  type        = string
  description = "The password of the Postgres database."
  sensitive   = true
  # default   = [database_password]
}

variable "docker_image" {
  type        = string
  description = "The docker image to deploy to Cloud Run."
  default     = "minasonbol/moneydiaries:moneydiaries"
}

variable "domain" {
  description = "Domain name to run the load balancer on. Used if `ssl` is `true`."
  type        = string
  default     = ""
}

variable "ssl" {
  description = "Run load balancer on HTTPS and provision managed certificate with provided `domain`."
  type        = bool
  default     = false
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "money_diaries"
}

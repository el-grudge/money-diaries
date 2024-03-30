Terraform will provision the following resources:

```bash
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "money_diaries"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = true
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = (known after apply)
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
    }

  # google_cloud_run_service.run_service will be created
  + resource "google_cloud_run_service" "run_service" {
      + autogenerate_revision_name = true
      + id                         = (known after apply)
      + location                   = "us-central1"
      + name                       = "mage-data-prep"
      + project                    = (known after apply)
      + status                     = (known after apply)

      + metadata {
          + annotations      = {
              + "run.googleapis.com/ingress"      = "all"
              + "run.googleapis.com/launch-stage" = "BETA"
            }
          + generation       = (known after apply)
          + labels           = (known after apply)
          + namespace        = (known after apply)
          + resource_version = (known after apply)
          + self_link        = (known after apply)
          + uid              = (known after apply)
        }

      + template {
          + metadata {
              + annotations      = (known after apply)
              + generation       = (known after apply)
              + labels           = (known after apply)
              + name             = (known after apply)
              + namespace        = (known after apply)
              + resource_version = (known after apply)
              + self_link        = (known after apply)
              + uid              = (known after apply)
            }
          + spec {
              + container_concurrency = (known after apply)
              + service_account_name  = (known after apply)
              + serving_state         = (known after apply)
              + timeout_seconds       = (known after apply)

              + containers {
                  + image = "minasonbol/moneydiaries:moneydiaries"
                  + name  = (known after apply)

                  + env {
                      # At least one attribute in this block is (or was) sensitive,
                      # so its contents will not be displayed.
                    }
                  + env {
                      # At least one attribute in this block is (or was) sensitive,
                      # so its contents will not be displayed.
                    }
                  + env {
                      # At least one attribute in this block is (or was) sensitive,
                      # so its contents will not be displayed.
                    }
                  + env {
                      # At least one attribute in this block is (or was) sensitive,
                      # so its contents will not be displayed.
                    }
                  + env {
                      # At least one attribute in this block is (or was) sensitive,
                      # so its contents will not be displayed.
                    }
                  + env {
                      # At least one attribute in this block is (or was) sensitive,
                      # so its contents will not be displayed.
                    }
                  + env {
                      # At least one attribute in this block is (or was) sensitive,
                      # so its contents will not be displayed.
                    }
                  + env {
                      # At least one attribute in this block is (or was) sensitive,
                      # so its contents will not be displayed.
                    }
                  + env {
                      # At least one attribute in this block is (or was) sensitive,
                      # so its contents will not be displayed.
                    }

                  + ports {
                      + container_port = 6789
                      + name           = (known after apply)
                    }

                  + resources {
                      + limits = {
                          + "cpu"    = "2000m"
                          + "memory" = "2G"
                        }
                    }

                  + volume_mounts {
                      + mount_path = "/secrets/bigquery"
                      + name       = "secret-bigquery-key"
                    }
                }

              + volumes {
                  + name = "secret-bigquery-key"

                  + secret {
                      + secret_name = "bigquery_credentials"

                      + items {
                          + key  = "latest"
                          + path = "bigquery_credentials"
                        }
                    }
                }
            }
        }

      + traffic {
          + latest_revision = true
          + percent         = 100
          + url             = (known after apply)
        }
    }

  # google_cloud_run_service_iam_member.run_all_users will be created
  + resource "google_cloud_run_service_iam_member" "run_all_users" {
      + etag     = (known after apply)
      + id       = (known after apply)
      + location = "us-central1"
      + member   = "allUsers"
      + project  = (known after apply)
      + role     = "roles/run.invoker"
      + service  = "mage-data-prep"
    }

  # google_compute_region_network_endpoint_group.cloudrun_neg will be created
  + resource "google_compute_region_network_endpoint_group" "cloudrun_neg" {
      + id                    = (known after apply)
      + name                  = "mage-data-prep-neg"
      + network_endpoint_type = "SERVERLESS"
      + project               = (known after apply)
      + region                = "us-central1"
      + self_link             = (known after apply)

      + cloud_run {
          + service = "mage-data-prep"
        }
    }

  # google_compute_security_policy.policy will be created
  + resource "google_compute_security_policy" "policy" {
      + fingerprint = (known after apply)
      + id          = (known after apply)
      + name        = "mage-data-prep-security-policy"
      + project     = (known after apply)
      + self_link   = (known after apply)
      + type        = (known after apply)

      + rule {
          + action      = "allow"
          + description = "Whitelist IP"
          + preview     = (known after apply)
          + priority    = 100

          + match {
              + versioned_expr = "SRC_IPS_V1"

              + config {
                  + src_ip_ranges = [
                      + "34.16.79.15/32",
                    ]
                }
            }
        }
      + rule {
          + action      = "deny(403)"
          + description = "default rule"
          + preview     = (known after apply)
          + priority    = 2147483647

          + match {
              + versioned_expr = "SRC_IPS_V1"

              + config {
                  + src_ip_ranges = [
                      + "*",
                    ]
                }
            }
        }
    }

  # google_filestore_instance.instance will be created
  + resource "google_filestore_instance" "instance" {
      + create_time = (known after apply)
      + etag        = (known after apply)
      + id          = (known after apply)
      + location    = "us-central1-c"
      + name        = "mage-data-prep"
      + project     = (known after apply)
      + tier        = "BASIC_HDD"
      + zone        = (known after apply)

      + file_shares {
          + capacity_gb   = 1024
          + name          = "share1"
          + source_backup = (known after apply)
        }

      + networks {
          + connect_mode      = "DIRECT_PEERING"
          + ip_addresses      = (known after apply)
          + modes             = [
              + "MODE_IPV4",
            ]
          + network           = "default"
          + reserved_ip_range = (known after apply)
        }
    }

  # google_project_service.artifactregistry will be created
  + resource "google_project_service" "artifactregistry" {
      + disable_on_destroy = false
      + id                 = (known after apply)
      + project            = (known after apply)
      + service            = "artifactregistry.googleapis.com"
    }

  # google_project_service.cloudrun will be created
  + resource "google_project_service" "cloudrun" {
      + disable_on_destroy = false
      + id                 = (known after apply)
      + project            = (known after apply)
      + service            = "run.googleapis.com"
    }

  # google_project_service.iam will be created
  + resource "google_project_service" "iam" {
      + disable_on_destroy = false
      + id                 = (known after apply)
      + project            = (known after apply)
      + service            = "iam.googleapis.com"
    }

  # google_project_service.resourcemanager will be created
  + resource "google_project_service" "resourcemanager" {
      + disable_on_destroy = false
      + id                 = (known after apply)
      + project            = (known after apply)
      + service            = "cloudresourcemanager.googleapis.com"
    }

  # google_project_service.secretmanager will be created
  + resource "google_project_service" "secretmanager" {
      + disable_on_destroy = false
      + id                 = (known after apply)
      + project            = (known after apply)
      + service            = "secretmanager.googleapis.com"
    }

  # google_project_service.sqladmin will be created
  + resource "google_project_service" "sqladmin" {
      + disable_on_destroy = false
      + id                 = (known after apply)
      + project            = (known after apply)
      + service            = "sqladmin.googleapis.com"
    }

  # google_project_service.vpcaccess will be created
  + resource "google_project_service" "vpcaccess" {
      + disable_on_destroy = false
      + id                 = (known after apply)
      + project            = (known after apply)
      + service            = "vpcaccess.googleapis.com"
    }

  # google_sql_database.database will be created
  + resource "google_sql_database" "database" {
      + charset         = (known after apply)
      + collation       = (known after apply)
      + deletion_policy = "DELETE"
      + id              = (known after apply)
      + instance        = "mage-data-prep-db-instance"
      + name            = "mage-data-prep-db"
      + project         = (known after apply)
      + self_link       = (known after apply)
    }

  # google_sql_database_instance.instance will be created
  + resource "google_sql_database_instance" "instance" {
      + available_maintenance_versions = (known after apply)
      + connection_name                = (known after apply)
      + database_version               = "POSTGRES_14"
      + deletion_protection            = false
      + dns_name                       = (known after apply)
      + encryption_key_name            = (known after apply)
      + first_ip_address               = (known after apply)
      + id                             = (known after apply)
      + instance_type                  = (known after apply)
      + ip_address                     = (known after apply)
      + maintenance_version            = (known after apply)
      + master_instance_name           = (known after apply)
      + name                           = "mage-data-prep-db-instance"
      + private_ip_address             = (known after apply)
      + project                        = (known after apply)
      + psc_service_attachment_link    = (known after apply)
      + public_ip_address              = (known after apply)
      + region                         = "us-central1"
      + self_link                      = (known after apply)
      + server_ca_cert                 = (known after apply)
      + service_account_email_address  = (known after apply)

      + settings {
          + activation_policy     = "ALWAYS"
          + availability_type     = "ZONAL"
          + connector_enforcement = (known after apply)
          + disk_autoresize       = true
          + disk_autoresize_limit = 0
          + disk_size             = (known after apply)
          + disk_type             = "PD_SSD"
          + pricing_plan          = "PER_USE"
          + tier                  = "db-f1-micro"
          + user_labels           = (known after apply)
          + version               = (known after apply)

          + database_flags {
              + name  = "max_connections"
              + value = "50"
            }
        }
    }

  # google_sql_user.database-user will be created
  + resource "google_sql_user" "database-user" {
      + host                    = (known after apply)
      + id                      = (known after apply)
      + instance                = "mage-data-prep-db-instance"
      + name                    = "mageuser"
      + password                = (sensitive value)
      + project                 = (known after apply)
      + sql_server_user_details = (known after apply)
    }

  # google_vpc_access_connector.connector will be created
  + resource "google_vpc_access_connector" "connector" {
      + connected_projects = (known after apply)
      + id                 = (known after apply)
      + ip_cidr_range      = "10.8.0.0/28"
      + machine_type       = "e2-micro"
      + max_instances      = (known after apply)
      + max_throughput     = 300
      + min_instances      = (known after apply)
      + min_throughput     = 200
      + name               = "mage-data-prep-connector"
      + network            = "default"
      + project            = (known after apply)
      + region             = "us-central1"
      + self_link          = (known after apply)
      + state              = (known after apply)
    }

  # module.lb-http.google_compute_backend_service.default["default"] will be created
  + resource "google_compute_backend_service" "default" {
      + connection_draining_timeout_sec = 300
      + creation_timestamp              = (known after apply)
      + enable_cdn                      = false
      + fingerprint                     = (known after apply)
      + generated_id                    = (known after apply)
      + id                              = (known after apply)
      + load_balancing_scheme           = "EXTERNAL"
      + name                            = "mage-data-prep-urlmap-backend-default"
      + port_name                       = (known after apply)
      + project                         = (known after apply)
      + protocol                        = (known after apply)
      + security_policy                 = "mage-data-prep-security-policy"
      + self_link                       = (known after apply)
      + session_affinity                = (known after apply)
      + timeout_sec                     = (known after apply)

      + backend {
          + balancing_mode               = "UTILIZATION"
          + capacity_scaler              = 1
          + group                        = (known after apply)
          + max_connections              = (known after apply)
          + max_connections_per_endpoint = (known after apply)
          + max_connections_per_instance = (known after apply)
          + max_rate                     = (known after apply)
          + max_rate_per_endpoint        = (known after apply)
          + max_rate_per_instance        = (known after apply)
          + max_utilization              = (known after apply)
        }
    }

  # module.lb-http.google_compute_global_address.default[0] will be created
  + resource "google_compute_global_address" "default" {
      + address            = (known after apply)
      + creation_timestamp = (known after apply)
      + id                 = (known after apply)
      + label_fingerprint  = (known after apply)
      + labels             = {
          + "example-label" = "cloud-run-example"
        }
      + name               = "mage-data-prep-urlmap-address"
      + prefix_length      = (known after apply)
      + project            = (known after apply)
      + self_link          = (known after apply)
    }

  # module.lb-http.google_compute_global_forwarding_rule.http[0] will be created
  + resource "google_compute_global_forwarding_rule" "http" {
      + base_forwarding_rule  = (known after apply)
      + id                    = (known after apply)
      + ip_address            = (known after apply)
      + ip_protocol           = (known after apply)
      + label_fingerprint     = (known after apply)
      + labels                = {
          + "example-label" = "cloud-run-example"
        }
      + load_balancing_scheme = "EXTERNAL"
      + name                  = "mage-data-prep-urlmap"
      + network               = (known after apply)
      + port_range            = "80"
      + project               = (known after apply)
      + psc_connection_id     = (known after apply)
      + psc_connection_status = (known after apply)
      + self_link             = (known after apply)
      + subnetwork            = (known after apply)
      + target                = (known after apply)
    }

  # module.lb-http.google_compute_target_http_proxy.default[0] will be created
  + resource "google_compute_target_http_proxy" "default" {
      + creation_timestamp = (known after apply)
      + id                 = (known after apply)
      + name               = "mage-data-prep-urlmap-http-proxy"
      + project            = (known after apply)
      + proxy_bind         = (known after apply)
      + proxy_id           = (known after apply)
      + self_link          = (known after apply)
      + url_map            = (known after apply)
    }

  # module.lb-http.google_compute_url_map.default[0] will be created
  + resource "google_compute_url_map" "default" {
      + creation_timestamp = (known after apply)
      + default_service    = (known after apply)
      + fingerprint        = (known after apply)
      + id                 = (known after apply)
      + map_id             = (known after apply)
      + name               = "mage-data-prep-urlmap-url-map"
      + project            = (known after apply)
      + self_link          = (known after apply)
    }
```
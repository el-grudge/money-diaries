# Money Diaries

## Problem Description 
[Money Diaries](https://www.refinery29.com/en-us/money-diary) is a blog created in 2016 and hosted by the Refinery29 website. It comes out 3 times a week, where in each post an anonymous contributor writes about their money spending habits. All posts share a similar structure:
* The first section has information on the contributor's occupation, the industry they work in, their age, location, salary, net worth, debt, paycheck amount and cadence, and pronouns
* The second section covers their monthly expenses
* The third section is a list of background questions
* The fourth section is the diary, where the contributor tracks and shares their money spending for a week
* The fifth and final section is the breadkown, in which all their spending is aggregated into six cateogries: Food+Drink, Home+Health, Clothes+Beauty, Entertainment, Transport, Other

The blog is a rich source of data for anyone who wants to learn about how money shapes our lives. My goal is to create an interactive dashboard that summarizes some of the information in the blog such as salary distribution, prices over time, and debt vs. net worth. 

### Pipeline

[pipeline image here]

...

## Cloud
The following cloud resources are provisioned using Terraform:
- Mage.ai 
- BigQuery dataset

See instructions in the Reproducibility section for details on how to deploy and run these resources.

## Data ingestion
Data is ingested using a pipelines are created in Mage.ai. 

The DAG steps are:
1. Scrap the blog home page and load it's json objects in BigQuery using `dlt`*
2. Extract the blog urls from "diary_links__rows__entities" table
3. Scrap the blog posts and load their json contents in BigQuery using `dlt`

[dag image here]

\* Note: Refinery29 webstie's robot.txt file has no explicit restrictions on scrapping the Money Diaries blog posts. You can check it [here](https://www.refinery29.com/robots.txt)

## Data warehouse

BigQuery dataware

...

## Transformations

...

## Dashboard

[image](...)

The dashboard can be accessed [here](...)

The dashboard has the following charts:
* Number overlays showing ...
* Salary distribution histogram
* Debt-Net worth divergent bar chart
* Category prices over time line chart
* Inflation calculator

...

## Reproducibility

### Prerequisite

1. [Docker](https://docs.docker.com/engine/install/)
2. [terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
3. [dbt](https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup)
4. GCP account

### Permissions

- Artifact Registry Read (mage)
- Artifact Registry Writer (mage)
- Cloud Run Developer (mage in the cloud) (try Cloud Run Admin instead) 
- Cloud SQL Admin (mage in the cloud)
- Service Account Token Creator (mage in the cloud)
- BigQuery Admin (BigQuery) # if needed 
- Cloud Vision AI Service Agent (Vision) # if needed
- Secret Manager Secret Accessor (mage) # if needed
- Vision AI Analysis Editor (Vision) # if needed
- Vision AI Application Editor (Vision) # if needed
- Service Usage Admin () # if needed
- Service Object Viewer () # if needed

...

### Run 

1. Clone the repo 


```bash
git clone https://github.com/el-grudge/money-diaries.git 
```

2. Export the following environment variables 

Change the values of the following environment variables or set them in the `variables.tf` file

```bash
export GOOGLE_PROJECT=[project-name]
export GOOGLE_PROJECT_ID=[project-id]
export GCP_REGION=[region]
export GCP_ZONE=[us-central1-c]
export GCP_LOCATION=[location]
export DB_PASSWORD=[database_password]
```

Note: The DB_PASSWORD parameter is for the Postgres database that will be used by Mage.ai's internal operations. The dashboard's data will be stored in a BigQuery dataset. 

1. Provision cloud resources with terraform

*terraform init* 
```bash
cd terraform \
terraform init
```

*terraform plan*
```bash
terraform plan \
  -var="project=${GOOGLE_PROJECT}" \
  -var="project_id=${GOOGLE_PROJECT_ID}" \
  -var="region=${GCP_REGION}" \
  -var="zone=${GCP_ZONE}" \
  -var="location=${GCP_LOCATION}"
```

*terraform apply*
```bash
terraform apply \
  -var="project=${GOOGLE_PROJECT}" \
  -var="project_id=${GOOGLE_PROJECT_ID}" \
  -var="region=${GCP_REGION}" \
  -var="zone=${GCP_ZONE}" \
  -var="location=${GCP_LOCATION}"
```

Terraform will deploy Mage.ai as a Google Clound Run service, which you can access by navigating to the Cloud Run option on the left navigation menu. On the service details page, you'll find the URL of the running service listed under the "Service URL" section. Copy & go to this URL to find the Mage.ai service

<img src="./images/cloud_run.gif" alt="cloud run" width="750"/>

Once inside Mage.ai service, you'll find the money_diaries pipeline already created. To run the pipeline, click on it to go the triggers page then press the Run@Once button, then the Run Now button in the Run Pipeline Now pop-up window. You can view the run's log by going to Run on the left navigation menu and clicking on the logs logo next to the Running pipeline

<img src="./images/pipeline_run.gif" alt="pipeline" width="750"/>

The pipeline will extract the blog posts from Money Diaries and load them into the BigQuery dataset called money_diaries, also provisioned by Terraform. You can view the dataset by navigating to BigQuery on the left navigation menu, then click on BigQuery Studio. Once the Explorer loads, expand the project containing your dataset to list all datasets

<img src="./images/dataset.gif" alt="dataset" width="750"/>

To delete these resources, run the `terraform destroy` command:

*terraform destroy*
```bash
terraform destroy \
  -var="project=${GOOGLE_PROJECT}" \
  -var="project_id=${GOOGLE_PROJECT_ID}" \
  -var="region=${GCP_REGION}" \
  -var="zone=${GCP_ZONE}" \
  -var="location=${GCP_LOCATION}"
```

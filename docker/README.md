The Dockerfile [`moneydiaries.dockerfile`](moneydiaries.dockerfile) creates an image based on Mage.ai. Two more things are added to it:

1. The [`dlt`](https://dlthub.com/) package
2. The data ingestion pipeline that will be deployed in Mage.ai

The image is uploaded to docker hub and Google artifact registry, and is deployed by terraform as Google Cloud Run service.

Follow these instructions to build the image locally 

**Note:** 
- Run these commands from the project home directory to ensure that the build context includes the mage_data directory
- Replace the values of the variables in squared brackets

```bash
# build the image
docker build -t [imagename]:[tag] -f docker/moneydiaries.dockerfile .
# upload to dockerhub
docker tag [imagename]:[tag] [dockerhub_username]/[dockerhub_repository]:[dockerhub_tag]
docker login
# enter your credentials
docker push [dockerhub_username]/[dockerhub_repository]:[dockerhub_tag]
# upload to Google artifact registry
gcloud init
gcloud auth configure-docker [gcp_region]-docker.pkg.dev
docker tag [imagename]:[tag] [gcp_region]-docker.pkg.dev/[project_id]/[repository_name]/[property_name]:[property_tag]
docker push [gcp_region]-docker.pkg.dev/[project_id]/[repository_name]/[property_name]:[property_tag]
```




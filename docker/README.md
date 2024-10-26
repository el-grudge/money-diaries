#### BigQuery
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


#### Postgres on NEON
To use Postgres on NEON instead of BigQuery, follow these steps:

1. Create an account on NEON ([here](https://console.neon.tech/realms/prod-realm/protocol/openid-connect/registrations?client_id=neon-console&redirect_uri=https%3A%2F%2Fconsole.neon.tech%2Fauth%2Fkeycloak%2Fcallback&response_type=code&scope=openid+profile+email&state=NR-FzJYd9UBjtZhRVjq-uA%3D%3D%2C%2C%2C))
2. Create a project called money-diaries
3. The schema name should be money_diaries

Next, go to the Dashboard tab and copy the connection parameters, which can be found under "Connection Details".

To run a docker container that connects Mage with Postgres on NEON use the following command:

```bash
docker run \
    -d \
    -p 6789:6789 \
    -e NEON_HOST=<hostname> \
    -e NEON_DB='money_diaries' \
    -e NEON_USER=<username> \
    -e NEON_PASSWORD=<password> \
    --name mage_container \
    -v $(pwd)/mage_data:/home/mage_code/money_diaries \
    moneydiaries:mage
```

To delete a docker container with the same name use this command:

```bash
docker rm mage_container
```
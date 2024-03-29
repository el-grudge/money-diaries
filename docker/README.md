docker build -t money-diaries:002 -f docker/moneydiaries.dockerfile .
docker run -it --rm money-diaries:002 /bin/bash
docker tag money-diaries:002 minasonbol/moneydiaries:moneydiaries
docker login
docker push minasonbol/moneydiaries:moneydiaries
gcloud init
gcloud auth configure-docker us-central1-docker.pkg.dev
docker tag money-diaries:002 us-central1-docker.pkg.dev/linen-source-411501/mage-with-dlt/magedlt:moneydiaries
docker push us-central1-docker.pkg.dev/linen-source-411501/mage-with-dlt/magedlt:moneydiaries

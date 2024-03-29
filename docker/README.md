docker build -t money-diaries:001 -f docker/moneydiaries.dockerfile .
docker run -it --rm money-diaries:001 /bin/bash
docker tag money-diaries:001 minasonbol/moneydiaries:moneydiaries
docker login
docker push minasonbol/moneydiaries:moneydiaries
gcloud init
gcloud auth configure-docker us-central1-docker.pkg.dev
docker tag money-diaries:001 us-central1-docker.pkg.dev/linen-source-411501/mage-with-dlt/magedlt:moneydiaries
docker push us-central1-docker.pkg.dev/linen-source-411501/mage-with-dlt/magedlt:moneydiaries

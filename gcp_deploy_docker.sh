# I think this step is not needed for app engine deployment as we only need the image locally i thnk??
# and putting it in the container registry is only for training and make endpoint [Search that!]

docker build -t gcr.io/landmark-classifier/my-docker-api .
docker push gcr.io/landmark-classifier/my-docker-api
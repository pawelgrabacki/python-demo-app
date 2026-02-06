pipeline {
  agent any

  environment {
    CLOUDSDK_CORE_PROJECT = 'jenkins-gcloud-486320'
    REPO_URL       = 'https://github.com/pawelgrabacki/python-demo-app.git'
    BRANCH         = 'main'
    DOCKERHUB_REPO = 'pawelgrabacki/python-demo-app'
    IMAGE_TAG      = "${BUILD_NUMBER}"

    // GCE settings
    GCE_ZONE     = 'europe-central2-a'
    GCE_INSTANCE = 'python-demo-app-vm'
    GCE_TAG      = 'python-demo-app'
    GCE_FW_RULE  = 'allow-flask-80'
  }

  stages {

    stage('Checkout') {
      steps {
        git branch: "${BRANCH}", url: "${REPO_URL}"
      }
    }

    // Creating Docker image with python/flask app
    stage('Build Docker image') {
      steps {
        sh """
          docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} .
          docker tag ${DOCKERHUB_REPO}:${IMAGE_TAG} ${DOCKERHUB_REPO}:latest
        """
      }
    }

    stage('List images') {
      steps {
        sh "docker images | grep ${DOCKERHUB_REPO} || true"
      }
    }

    // Uploading created image to Docker Hub
    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'pawelgrabacki-dockerhub',
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS'
        )]) {
          sh """
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}
            docker push ${DOCKERHUB_REPO}:latest
          """
        }
      }
    }

    // GCP deployment
    stage('Deploy to GCE (create or update container VM)') {
      when { expression { env.BRANCH == 'main' } }

      steps {
        withCredentials([file(credentialsId: 'gcloud-creds', variable: 'GCLOUD_CREDS')]) {
          sh '''
            set -eu

            gcloud auth activate-service-account --key-file="$GCLOUD_CREDS"
<<<<<<< HEAD
            gcloud config set project "$CLOUDSDK_CORE_PROJECT"
            gcloud config set compute/zone "$GCE_ZONE"

            # Firewall rule: allow HTTP (port 80)
            if ! gcloud compute firewall-rules describe "$GCE_FW_RULE" >/dev/null 2>&1; then
              gcloud compute firewall-rules create "$GCE_FW_RULE" \
                --allow tcp:80 \
                --direction INGRESS \
                --source-ranges 0.0.0.0/0 \
                --target-tags "$GCE_TAG"
            fi

            # Create VM if missing, otherwise update container
            if ! gcloud compute instances describe "$GCE_INSTANCE" >/dev/null 2>&1; then
              gcloud beta compute instances create-with-container "$GCE_INSTANCE" \
                --machine-type=e2-micro \
                --tags="$GCE_TAG" \
                --container-image="$DOCKERHUB_REPO:latest" \
                --container-env=BUILD_NUMBER=$BUILD_NUMBER \
                --container-restart-policy=always
            else
              gcloud compute instances add-tags "$GCE_INSTANCE" --tags="$GCE_TAG" || true

              gcloud beta compute instances update-container "$GCE_INSTANCE" \
                --container-image="$DOCKERHUB_REPO:latest" \
                --container-env=BUILD_NUMBER=$BUILD_NUMBER
            fi

            echo "VM external IP:"
            gcloud compute instances describe "$GCE_INSTANCE" \
=======
            gcloud config set project "'"${CLOUDSDK_CORE_PROJECT}"'"
            gcloud config set compute/zone "'"${GCE_ZONE}"'"

            # Open port 80 to the VM (tag: python-demo-app)
            if ! gcloud compute firewall-rules describe "'"${GCE_FW_RULE}"'" >/dev/null 2>&1; then
              gcloud compute firewall-rules create "'"${GCE_FW_RULE}"'" \
                --allow tcp:80 \
                --direction INGRESS \
                --source-ranges 0.0.0.0/0 \
                --target-tags "'"${GCE_TAG}"'"
            fi

            # Create VM if missing, otherwise update container
            if ! gcloud compute instances describe "'"${GCE_INSTANCE}"'" >/dev/null 2>&1; then
              gcloud beta compute instances create-with-container "'"${GCE_INSTANCE}"'" \
                --machine-type=e2-micro \
                --tags="'"${GCE_TAG}"'" \
                --container-image="'"${DOCKERHUB_REPO}"':latest" \
                --container-restart-policy=always
            else
              gcloud compute instances add-tags "'"${GCE_INSTANCE}"'" --tags="'"${GCE_TAG}"'" || true

              gcloud beta compute instances update-container "'"${GCE_INSTANCE}"'" \
                --container-image="'"${DOCKERHUB_REPO}"':latest"
            fi

            echo "VM external IP:"
            gcloud compute instances describe "'"${GCE_INSTANCE}"'" \
>>>>>>> 54c2082 (update)
              --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
          '''
        }
      }
    }
  }
}

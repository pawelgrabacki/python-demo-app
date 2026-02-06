pipeline {
  agent any

  environment {
    CLOUDSDK_CORE_PROJECT = 'jenkins-gcloud-486320'
    REPO_URL       = 'https://github.com/pawelgrabacki/python-demo-app.git'
    BRANCH         = 'main'
    DOCKERHUB_REPO = 'pawelgrabacki/python-demo-app'
    IMAGE_TAG      = "${BUILD_NUMBER}"
  }

  stages {

    stage('Checkout') {
      steps {
        git branch: "${BRANCH}", url: "${REPO_URL}"
      }
    }

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

    stage('Deploy to GCE (create or update container VM)') {
      when {
        expression { env.BRANCH == 'main' }
      }
      steps {
        withCredentials([file(credentialsId: 'gcloud-creds', variable: 'GCLOUD_CREDS')]) {
          sh """
            set -euo pipefail

            PROJECT="${CLOUDSDK_CORE_PROJECT}"
            ZONE="europe-central2-a"
            INSTANCE="flask-app-vm"
            TAG="flask-app"
            FIREWALL_RULE="allow-flask-5000"
            IMAGE="${DOCKERHUB_REPO}:latest"

            gcloud auth activate-service-account --key-file="$GCLOUD_CREDS"
            gcloud config set project "\$PROJECT"
            gcloud config set compute/zone "\$ZONE"

            # Create firewall rule once (opens port 5000 to VMs with tag flask-app)
            if ! gcloud compute firewall-rules describe "$FIREWALL_RULE" >/dev/null 2>&1; then
              gcloud compute firewall-rules create "$FIREWALL_RULE" \\
                --allow tcp:5000 \\
                --direction INGRESS \\
                --target-tags "$TAG"
            fi

            # Create VM if missing, otherwise update its container image
            if ! gcloud compute instances describe "$INSTANCE" >/dev/null 2>&1; then
              gcloud beta compute instances create-with-container "$INSTANCE" \\
                --machine-type=e2-micro \\
                --tags="$TAG" \\
                --container-image="$IMAGE" \\
                --container-restart-policy=always
            else
              # Ensure it has the right tag (safe even if already present)
              gcloud compute instances add-tags "$INSTANCE" --tags="$TAG" || true

              gcloud beta compute instances update-container "$INSTANCE" \\
                --container-image="$IMAGE"
            fi

            # Print the external IP so you can open it in browser
            gcloud compute instances describe "$INSTANCE" \\
              --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
          """
        }
      }
    }

    /*
    stage('cloud') {
      steps {
        withCredentials([file(credentialsId: 'gcloud-creds', variable: 'GCLOUD_CREDS')]) {
          sh '''
            gcloud version
            gcloud auth activate-service-account --key-file="$GCLOUD_CREDS"
            gcloud compute zones list
          '''
        }
      }
    }
    */
  }
}

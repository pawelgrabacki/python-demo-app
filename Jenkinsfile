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
/*
    stage('Build Docker image') {
      steps {
        sh """
          docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} .
          docker tag ${DOCKERHUB_REPO}:${IMAGE_TAG} ${DOCKERHUB_REPO}:latest
        """
      }
      


    }
    */
       stage('Build Docker (main only)') {
      when { branch 'main' }
      steps {
        sh """
          docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} .
          docker tag ${DOCKERHUB_REPO}:${IMAGE_TAG} ${DOCKERHUB_REPO}:latest
        """
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

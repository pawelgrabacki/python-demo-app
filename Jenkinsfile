pipeline {
  agent any

  environment {
    CLOUDSDK_CORE_PROJECT = 'jenkins-gcloud-486320'
  }

  stages {

    // checking SCM
    stage('Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/pawelgrabacki/python-demo-app.git'
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

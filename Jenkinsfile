pipeline {
  agent any
  environment{
      CLOUDSDK_CORE_PROJECT='jenkins-gcloud-486320'
  }
  stages {
    stage('test') {
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
  }
}
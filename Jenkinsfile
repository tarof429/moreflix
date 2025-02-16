pipeline {
    agent {
        label 'jenkins-node'
    }


    stages {
        stage('Hello') {
            steps {
                sh 'docker run hello-world'
            }
        }
    }
}

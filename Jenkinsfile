pipeline {
    agent {
        label 'jenkins-node'
    }


    stages {
        stage('Init libraries') {
            steps {
                script {
                    gv = load "build.groovy"
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    gv.buildImage()
            }
        }

        stage('Push docker image') {
            steps {
                echo "Deploy..."
            }
        }
    }
}

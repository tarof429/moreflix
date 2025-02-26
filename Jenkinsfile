#/usr/bin/env groovy

@Library('moreflix-shared-library')_

pipeline {
    agent {
        label 'jenkins-node'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '30'))
    }

    stages {
        stage('Init') {
            steps {
                script {
                    removeDockerCompose('db,app')
                }
            }
        }

        stage('Get version') {
            steps {
                script {
                    def version = getVersion('setup.py')
                    echo("Version ${version}")
                }
            }
        }
        stage('Build docker image') {
            steps {
                script {
                    buildDockerImage('tarof429/moreflix:${version}')
                    tagDockerImage('tarof429/moreflix:${version}', 'latest')
                }
            }
        }

        stage('Build test docker image') {
            steps {
                script {
                    buildDockerImage('moreflix-test', 'Dockerfile-test')
                }
            }
        }

        stage('Run tests') {
            steps {
                script {
                    startDockerCompose('db,app')
                   
                    testFailed = runDockerCompose('test')
                    
                    stopDockerCompose('db,app')

                    echo "${testFailed}"

                    if (testFailed != 0) {
                        error('Tests failed')
                    }

                }
            }
        }
    }
}
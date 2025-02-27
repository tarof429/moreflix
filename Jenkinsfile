#!/usr/bin/env groovy

@Library('moreflix-shared-library')_

def version

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
                    version = getVersion('setup.py')
                    echo("Version ${version}")
                }
            }
        }
        stage('Build docker image') {
            steps {
                script {
                    buildDockerImage("tarof429/moreflix:${version}")
                    tagDockerImage("tarof429/moreflix:${version}", 'tarof429/moreflix:latest')
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

        stage('Deploy to dockerhub') {
            when {
                expression {
                    env.BRANCH_NAME == 'main' && testFailed == 0
                }
            }
            steps {
                script {
                    pushDockerTag('dockerhub', "tarof429/moreflix:latest")
                    pushDockerTag('dockerhub', "tarof429/moreflix:${version}")
                }
            }
        }

        stage('Set next version') {
            when {
                expression {
                    env.BRANCH_NAME == 'main' && testFailed == 0
                }
            }
            steps {
                script {
                    updateVersion('setup.py')
                }
            }
        }

        stage('Commit version update') {
            when {
                expression {
                    env.BRANCH_NAME == 'main' && testFailed == 0
                }
            }
            steps {
                script {
                    githubCommit('moreflix-token3', "https://github.com/tarof429/moreflix.git")
                }
            }
        }
    }
}
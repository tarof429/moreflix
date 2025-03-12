#!/usr/bin/env groovy

@Library('moreflix-shared-library@main') _
import com.github.moreflix.Helper

def helper

pipeline {
    agent any

    environment {
        IMAGE_PREFIX = 'tarof429/moreflix'
        LATEST_IMAGE_NAME = "${env.IMAGE_PREFIX}:latest"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '30'))
    }

    stages {
        stage('Init') {
            steps {
                script {
                    helper = new Helper(this)

                    helper.setSimulator(false)
                    helper.setServerIP('44.245.216.73')

                    helper.stopAndRemoveOrphans()
                }
            }
        }

        stage('Get version') {
            steps {
                script {
                    env.VERSION = helper.getVersion('setup.py')
                    echo("Version: ${env.VERSION}")
                }
            }
        }
        stage('Build docker image') {
            steps {
                script {
                    helper.buildDockerImage("${env.LATEST_IMAGE_NAME}")
                }
            }
        }

        stage('Build test docker image') {
            steps {
                script {
                    helper.buildDockerImage('moreflix-test', 'Dockerfile-test')
                }
            }
        }

        stage('Run tests') {
            steps {
                script {
                    def testFailed = 0

                    helper.startDockerCompose("${env.LATEST_IMAGE_NAME}", "db,app")
                   
                    testFailed = helper.runDockerCompose("dummy", "test")
                    
                    helper.stopDockerCompose("dummy", "db,app")

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
                    env.IMAGE_NAME = "${env.IMAGE_PREFIX}:${env.VERSION}-${env.BUILD_NUMBER}"

                    helper.tagDockerImage("${env.LATEST_IMAGE_NAME}", "${env.IMAGE_NAME}")

                    helper.pushDockerTag('dockerhub', "${env.LATEST_IMAGE_NAME}")
                    helper.pushDockerTag('dockerhub', "${env.IMAGE_NAME}")
                }
            }
        }

        stage('Deploy image to AWS') {
            when {
                expression {
                    env.BRANCH_NAME == 'main' && testFailed == 0
                }
            }
            steps {
                script {
                    helper.deployToAWS("${env.IMAGE_NAME}")
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
                    helper.updateVersion('setup.py')
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
                    helper.githubCommit('moreflix-token', "https://github.com/tarof429/moreflix.git")
                }
            }
        }
    }
}
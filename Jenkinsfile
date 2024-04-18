pipeline {
    agent any

    environment {
        CAR_INVENTORY_DOCKER_IMAGE = 'pax7898/car_inventory'
        VIN_DECODER_DOCKER_IMAGE = 'pax7898/vin_decoder'
    }

    stages {
        stage("Dockerize") {
            steps {
                script {
                    sh "docker build --platform linux/amd64 -t ${CAR_INVENTORY_DOCKER_IMAGE} car_inventory/."
                    sh "docker build --platform linux/amd64 -t ${VIN_DECODER_DOCKER_IMAGE} vin_decoder/."
                }
            }
        }

        stage("Login") {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: '21fdcb7b-93e6-4fb1-a5c0-0147b75284c4', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                        sh "echo \$DOCKERHUB_PASSWORD | docker login -u \$DOCKERHUB_USERNAME --password-stdin"
                    }
                }
            }
        }

        stage("Push to DockerHub") {
            steps {
                sh "docker push ${CAR_INVENTORY_DOCKER_IMAGE}"
                sh "docker push ${VIN_DECODER_DOCKER_IMAGE}"
            }
        }
    }
}



pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        CAR_INVENTORY_DOCKER_IMAGE = 'pax7898/car_inventory'
        VIN_DECODER_DOCKER_IMAGE = 'pax7898/vin_decoder'
    }
    
    stages{
        stage("Dockerize"){
            steps{
                sh 'docker build --platform linux/amd64 -t $CAR_INVENTORY_DOCKER_IMAGE car_inventory/.'
                sh 'docker build --platform linux/amd64 -t $VIN_DECODER_DOCKER_IMAGE vin_decoder/.'
            }
        }

        stage("Login"){
            steps{
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }

        stage("Push to DockerHub"){
            steps{
                sh 'docker push $CAR_INVENTORY_DOCKER_IMAGE'
                sh 'docker push $VIN_DECODER_DOCKER_IMAGE'
            }
        }
    }
}
pipeline {
    agent any

    tools {
        nodejs "nodejs_21_7_3"
    }

    environment {
        CAR_INVENTORY_DOCKERFILE_PATH = 'car_inventory/.'
        VIN_DECODER_DOCKERFILE_PATH = 'vin_decoder/.'

        CAR_INVENTORY_DOCKER_IMAGE = 'pax7898/car_inventory'
        VIN_DECODER_DOCKER_IMAGE = 'pax7898/vin_decoder'

        CAR_INVENTORY_YAML = 'car_inventory/car_inventory.yaml'
        VIN_DECODER_YAML = 'vin_decoder/vin_decoder.yaml'

        POSTMAN_API_KEY = 'PMAK-6620f2f8229990000138ca73-d962f419f0d6eaa784aad2c94127114727'
    }   

    stages {
        stage ("Cleaning"){
            steps {
                sh "kubectl delete service vin-decoder-service"
                sh "kubectl delete service car-inventory-service"
                sh "kubectl delete deployment vin-decoder-deployment"
                sh "kubectl delete deployment car-inventory-deployment"
            }
        }
        stage("Dockerize") {
            steps {
                script {
                    sh "docker build --platform linux/amd64 -t ${CAR_INVENTORY_DOCKER_IMAGE} ${CAR_INVENTORY_DOCKERFILE_PATH}"
                    sh "docker build --platform linux/amd64 -t ${VIN_DECODER_DOCKER_IMAGE} ${VIN_DECODER_DOCKERFILE_PATH}"
                }
            }
        }

        stage("Login") {
            steps {
                script {
                    sh 'docker login'
                }
            }
        }

        stage("Push to DockerHub") {
            steps {
                sh "docker push ${CAR_INVENTORY_DOCKER_IMAGE}"
                sh "docker push ${VIN_DECODER_DOCKER_IMAGE}"
            }
        }

        stage("Kubernets Deployment"){
            steps{
                sh "kubectl apply -f ${CAR_INVENTORY_YAML} -f ${VIN_DECODER_YAML}"
            }
        }

        stage('Install Postman CLI') {
            steps {
                sh 'curl -o- "https://dl-cli.pstmn.io/install/osx_arm64.sh" | sh'
            }
        }

        stage('Postman CLI Login') {
            steps {
                sh "postman login --with-api-key ${POSTMAN_API_KEY}"
            }
        }

        stage('Running collection') {
            steps {
                sh 'postman collection run "34340469-3bbe4d66-0367-45bc-a674-e6f9aac25bf9"'
            }
        }
            
    }
}



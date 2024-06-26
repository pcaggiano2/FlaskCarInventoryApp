// Check if service exists before attempting to delete
def deleteServiceIfExists(serviceName) {
    def serviceExists = sh(script: "kubectl get service $serviceName", returnStatus: true) == 0
    if (serviceExists) {
        sh "kubectl delete service $serviceName"
    } else {
        println "Service $serviceName does not exist, skipping deletion."
    }
}

// Check if deployment exists before attempting to delete
def deleteDeploymentIfExists(deploymentName) {
    def deploymentExists = sh(script: "kubectl get deployment $deploymentName", returnStatus: true) == 0
    if (deploymentExists) {
        sh "kubectl delete deployment $deploymentName"
    } else {
        println "Deployment $deploymentName does not exist, skipping deletion."
    }
}

pipeline {
    agent any

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
                script{
                    // Delete services
                    deleteServiceIfExists("vin-decoder-service")
                    deleteServiceIfExists("car-inventory-service")

                    // Delete deployments
                    deleteDeploymentIfExists("vin-decoder-deployment")
                    deleteDeploymentIfExists("car-inventory-deployment")
                }
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

        stage('Postman CLI Login') {
            steps {
                sh "/usr/local/bin/postman login --with-api-key ${POSTMAN_API_KEY}"
            }
        }

        stage('Running collection') {
            tools {
                nodejs "nodejs_21_7_3"
            }
            steps {
                sh '/usr/local/bin/postman collection run "34340469-3bbe4d66-0367-45bc-a674-e6f9aac25bf9"'
            }
        }
            
    }
}



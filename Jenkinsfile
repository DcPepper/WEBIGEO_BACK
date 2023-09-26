pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "sqlite"
        DOCKER_TAG = "back_test"
        DOCKER_BACK = "Back_Container"
    }
    stages {
        
        stage("Clean the containers"){
            steps{
                script{
                    def container = sh(script: 'docker ps',returnStdout: true).trim()

                    echo "This is the output : ${container}"

                    if (container.contains(env.DOCKER_BACK)){
                        sh "docker stop $DOCKER_BACK"
                        sh "docker rm $DOCKER_BACK"
                        sh "docker rmi $DOCKER_IMAGE:$DOCKER_TAG"
                    }
                    else{
                        echo "The container is clean"
                    }
                }
            }
        }



        stage("Building Back End image") {
            steps {
                script {
                    //sh "docker stop $DOCKER_BACK"
                    //sh "docker rm $DOCKER_BACK"
                    echo "Building Docker image: $DOCKER_IMAGE:$DOCKER_TAG"
                    sh "docker build -t $DOCKER_IMAGE:$DOCKER_TAG -f Dockerfile . --no-cache"
                }
            }
        }

        stage("Docker run the image") {
            steps {
                script {
                    echo "Running Docker container: $DOCKER_BACK"
                    sh "docker run -d -p 3021:8000 --name $DOCKER_BACK -v /mnt/data:/mnt/data $DOCKER_IMAGE:$DOCKER_TAG"
                    sh "docker ps"
                }
            }
        }

        
        stage("Testing the containers") {
            steps {
                script {
                    def serveripaddress = "4.236.153.248"
                    def containerId = sh(script: "docker ps -qf name=$DOCKER_BACK", returnStdout: true).trim()
                


                    def url = "http://${serveripaddress}:3021"

                    echo "Testing application at $url"
                    
                    // Use 'timeout' to prevent 'curl' from running indefinitely
                    def response = sh(script: "curl -i $url, returnStatus: true)
                    echo "The response of the url : ${response}"
                    if (response != 0) {
                        error "HTTP request to $url failed, check the URL and try again."
                    } else {
                        echo "HTTP request to $url was sucessfull :: status code $response"
                    }
                }
            }
        }
        

        stage("Removing the container and Image") {
            steps {
                script {
                    echo "Stopping and removing Docker container: $DOCKER_BACK"
                    sh "docker stop $DOCKER_BACK"
                    sh "docker rm $DOCKER_BACK"
                    echo "Removing Docker image: $DOCKER_IMAGE:$DOCKER_TAG"
                    sh "docker rmi $DOCKER_IMAGE:$DOCKER_TAG"
                }
            }
        }

       stage("Invoking another pipeline") {
            steps {
                script {
                    def main_pipeline = build job: 'WEBIGEO', parameters: [
                        booleanParam(name: 'Docker_Build_Back_End_Image', value: true),
                        booleanParam(name: 'Pushing_the_Back_End_image_to_DockerHub', value: true),
                        booleanParam(name: 'Deployment_in_webigeo', value: true)
                    ]
                    main_pipeline.waitForCompletion("Waiting for the WEBIGEO pipeline to complete")
                }
            }
        }

        stage("End") {
            steps {
                echo "Bye"
            }
        }
    }
}

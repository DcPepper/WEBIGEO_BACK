pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "sqlite"
        DOCKER_TAG = "back_test"
        DOCKER_BACK = "Back_Container"
    }
    stages {
        stage("Back End image") {
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
                    def response = sh(script: "timeout 30 curl -i $url", returnStatus: true)
                    echo "${response}"
                    if (response != 0) {
                        error "HTTP request to $url failed, check the URL and try again."
                    } else {
                        def statusCode = sh(script: "curl -s -o /dev/null -w '%{http_code}' $url", returnStatus: true)
                        echo"This is the test case : ${statusCode}"    
                        if (statusCode == 0) {
                            echo "HTTP request to $url was successful. Status code: $statusCode"
                        } else {
                            error "HTTP request to $url failed with status code $statusCode"
                        }
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
                echo "Triggering another pipeline job"
                build job: 'WEBIGEO', parameters: [string(name: 'param1', value: "value1")], wait: true
            }
        }

        stage("End") {
            steps {
                echo "Bye"
            }
        }
    }
}

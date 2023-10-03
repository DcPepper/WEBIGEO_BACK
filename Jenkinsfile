pipeline {
    agent {
        label 'Back_End'
    }
    environment {
        DOCKER_IMAGE = "my-django"
        DOCKER_TAG = "pre"
        DOCKER_BACK = "Back_Container"
        DOCKER_ID = "webigeo"
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
                        sh "docker rmi $DOCKER_IMAGE:$DOCKER_TAG || true"
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
                    sh "docker build -t $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG -f Dockerfile . --no-cache"
                }
            }
        }

        stage("Docker run the image") {
            steps {
                script {
                    echo "Running Docker container: $DOCKER_BACK"
                    sh "docker run -d -p 3021:8000 --name $DOCKER_BACK -v /mnt/data:/mnt/data $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG"
                    sh "docker ps"
                }
            }
        }

        
        stage("Testing the containers") {
            steps {
                script {
                    def serveripaddress = "4.180.124.152"
                    def containerId = sh(script: "docker ps -qf name=$DOCKER_BACK", returnStdout: true).trim()
                    sleep(30)


                    def url = "http://${serveripaddress}:3021"

                    echo "Testing application at $url"
                    
                    // Use 'timeout' to prevent 'curl' from running indefinitely
                    def response = sh(script: "curl -i $url", returnStatus: true)
                    echo "The response of the url : ${response}"
                    if (response != 0) {
                        error "HTTP request to $url failed, check the URL and try again."
                    } else {
                        echo "HTTP request to $url was sucessfull :: status code $response"
                    }
                }
            }
        }
        
        stage('Pushing Back End image to DockerHub') {
            environment
            {
                DOCKER_HUB_TOKEN = credentials("DOCKER_HUB_TOKEN") 
            }

            steps {

                script {
                    //env.DOCKER_HUB_TOKEN = DOCKER_HUB_TOKEN
                    sh '''
                    echo "docker login -u $DOCKER_ID -p $DOCKER_HUB_TOKEN"
                    docker login -u "webigeo" -p "yP?5Q>Ktp+YA%#_"
                    sleep 10
                    docker push "webigeo"/$DOCKER_IMAGE:$DOCKER_TAG
                '''
                }
            }
        }

        stage("Removing the container and Image") {
            steps {
                script {
                    echo "Stopping and removing Docker container: $DOCKER_BACK"
                    sh "docker stop $DOCKER_BACK"
                    sh "docker rm $DOCKER_BACK"
                    echo "Removing Docker image: $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG"
                    sh "docker rmi $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG"
                }
            }
        }

       stage("Invoking another pipeline") {
            steps {
                echo "Triggering another pipeline job"
                build job: 'WEBIGEO_CI_CD', parameters: [string(name: 'param1', value: "value1")], wait: true
            }
        }

        stage("End") {
            steps {
                echo "Bye"
            }
        }
    }
}

pipeline {
    agent any

    stages {



        stage('8. Run docker with secret variables') { 
            steps {
                withCredentials([
                    string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID'),
                    string(credentialsId: 'access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'mongodb_url', variable: 'MONGODB_URL'),
                    string(credentialsId: 'mlflow_tracking_uri', variable: 'MLFLOW_TRACKING_URI'),
                    string(credentialsId: 'mlflow_tracking_username', variable: 'MLFLOW_TRACKING_USERNAME'),
                    string(credentialsId: 'mlflow_tracking_password', variable: 'MLFLOW_TRACKING_PASSWORD')
                ]) {
                    sh """
                        # Docker login to ECR
                        aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com
                        
                        # Run the Docker container with secret environment variables
                        docker run -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
                                   -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
                                   -e MONGODB_URL=${MONGODB_URL} \
                                   -e MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI} \
                                   -e MLFLOW_TRACKING_USERNAME=${MLFLOW_TRACKING_USERNAME} \
                                   -e MLFLOW_TRACKING_PASSWORD=${MLFLOW_TRACKING_PASSWORD} \
                                   ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/your-image:latest
                    """
                }
            }
        }


    //     stage('2. Trivy Scan') {
    //         steps {
    //             sh "trivy fs . > trivy.txt"
    //         }
    //     }

    //     stage('3. Build Docker Image') {
    //         steps {
    //             sh 'docker build -ttt my-flask-app .'
    //         }
    //     }

    //     stage('4. Create ECR repo') {
    //         steps {
    //             withCredentials([string(credentialsId: 'access-key', variable: 'AWS_ACCESS_KEY'), 
    //                              string(credentialsId: 'secret-key', variable: 'AWS_SECRET_KEY')]) {
    //                 sh """
    //                 aws configure set aws_access_key_id $AWS_ACCESS_KEY
    //                 aws configure set aws_secret_access_key $AWS_SECRET_KEY
    //                 aws ecr describe-repositories --repository-names mlops-project-repo --region ap-south-1 || \
    //                 aws ecr create-repository --repository-name mlops-project-repo --region ap-south-1
    //                 """
    //             }
    //         }
    //     }

    //     stage('5. Login to ECR & tag image') {
    //         steps {
    //             withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
    //                 sh """
    //                 aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com
    //                 docker tag my-flask-app ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:${BUILD_NUMBER}
    //                 docker tag my-flask-app ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:latest
    //                 """
    //             }
    //         }
    //     }

    //     stage('6. Push image to ECR') {
    //         steps {
    //             withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
    //                 sh """
    //                 docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:${BUILD_NUMBER}
    //                 docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:latest
    //                 """
    //             }
    //         }
    //     }

    //     stage('7. Cleanup Images') {
    //         steps {
    //             withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
    //                 sh """
    //                 docker rmi ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:${BUILD_NUMBER}
    //                 docker rmi ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:latest
    //                 docker rmi my-flask-app
    //                 docker images
    //                 """
    //             }
    //         }
    //     }

    //     stage('8. Deploy to Kubernetes') {
    //         steps {
    //             withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID'),
    //                              string(credentialsId: 'access-key', variable: 'AWS_ACCESS_KEY_ID'),
    //                              string(credentialsId: 'secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
    //                              string(credentialsId: 'mongodb_url', variable: 'MONGODB_URL'),
    //                              string(credentialsId: 'mlflow_tracking_uri', variable: 'MLFLOW_TRACKING_URI'),
    //                              string(credentialsId: 'mlflow_tracking_username', variable: 'MLFLOW_TRACKING_USERNAME'),
    //                              string(credentialsId: 'mlflow_tracking_password', variable: 'MLFLOW_TRACKING_PASSWORD')]) {
    //                 sh """
    //                 aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com

    //                 kubectl create secret generic my-secret \
    //                   --from-literal=AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    //                   --from-literal=AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    //                   --from-literal=MONGODB_URL="${MONGODB_URL}" \
    //                   --from-literal=MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI}" \
    //                   --from-literal=MLFLOW_TRACKING_USERNAME="${MLFLOW_TRACKING_USERNAME}" \
    //                   --from-literal=MLFLOW_TRACKING_PASSWORD="${MLFLOW_TRACKING_PASSWORD}" \
    //                   --dry-run=client -o yaml | kubectl apply -f -

    //                 sed -i 's|\${AWS_ACCOUNT_ID}|'"${AWS_ACCOUNT_ID}"'|g' Kubernetes/deployment.yml
    //                 kubectl apply -f Kubernetes/deployment.yml
    //                 """
    //             }
    //         }
    //     }

    //     stage('9. Restart Deployment to Apply Changes') {
    //         steps {
    //             script {
    //                 sh "kubectl rollout restart deployment mlops-deployment"
    //             }
    //         }
    //     }

    //     stage('10. Expose Service in Kubernetes') {
    //         steps {
    //             sh "kubectl apply -f Kubernetes/service.yml"
    //         }
    //     }
    // }

    // post {
    //     success {
    //         withCredentials([string(credentialsId: 'RECIPIENTP', variable: 'RECIPIENTP')]) {
    //             emailext(
    //                 to: "${RECIPIENTP}",
    //                 from: "${RECIPIENTP}",
    //                 subject: "Build Success: ${BUILD_NUMBER}",
    //                 body: """
    //                     Dear user,
    //                     The Jenkins build has succeeded.
    //                 """,
    //                 mimeType: 'text/html'
    //             )
    //         }
    //     }

    //     failure {
    //         withCredentials([string(credentialsId: 'RECIPIENTF', variable: 'RECIPIENTF'),
    //                          string(credentialsId: 'RECIPIENTP', variable: 'RECIPIENTP')]) {
    //             emailext(
    //                 to: "${RECIPIENTF}",
    //                 from: "${RECIPIENTP}",
    //                 subject: "Build Failed: ${BUILD_NUMBER}",
    //                 body: """
    //                     Dear user,
    //                     The Jenkins build has failed. Please check the console output for more details:
    //                     ${env.BUILD_URL}console
    //                 """,
    //                 mimeType: 'text/html'
    //             )
    //         }
    //     }
    }
}

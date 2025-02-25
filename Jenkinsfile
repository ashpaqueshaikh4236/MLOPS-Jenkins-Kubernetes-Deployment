pipeline {
    agent any

    stages {
        // stage('1. Clone') {
        //     steps {
        //         echo 'Cloning the repository...'
        //         git branch: 'main', 
        //         url: 'https://github.com/ashpaqueshaikh4236/MLOPS-Jenkins-Kubernetes-Deployment.git'
        //         echo 'Repository cloned successfully.'
        //     }
        // }

        stage('2. Trivy Scan') {
            steps {
                echo 'Running Trivy Scan...'
                sh """
                trivy fs . > trivy.txt
                """
                echo 'Trivy Scan completed. Results stored in trivy.txt.'
            }
        }

       stage('3. Build Airflow Docker Image') {
            when {
            changeset pattern: '**/airflow/**, **/config/**, **/usvisa/**, setup.py, requirements-Airflow.txt, Dockerfile.Airflow'
        }
                    
            steps {
                script {
                    echo 'Checking if Docker image "airflow-image" exists...'
                    def imageExists = sh(
                        script: "docker images -q airflow-image",
                        returnStdout: true
                    ).trim()
        
                    if (imageExists) {
                        echo "Docker image 'airflow-image' already exists. Deleting and rebuilding..."
                        sh """
                        docker stop airflow-container || true
                        docker rm -fv airflow-container || true
                        docker rmi airflow-image:latest
                        docker images
                        docker build -f Dockerfile.Airflow -t airflow-image .
                        docker images
                        """
                    } else {
                        echo "Docker image 'airflow-image' does not exist. Building a new one..."
                        sh """
                        docker build -f Dockerfile.Airflow -t airflow-image .
                        docker images
                        """
                    }
                }
            }
        }



        // stage('4. Run Docker container using Airflow Docker Image') {
        //     steps {
        //         echo 'Running Docker container using Airflow image...'
        //         withCredentials([string(credentialsId: 'access-key', variable: 'AWS_ACCESS_KEY_ID'),
        //                         string(credentialsId: 'secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
        //                         string(credentialsId: 'mongodb_url', variable: 'MONGODB_URL'),
        //                         string(credentialsId: 'mlflow_tracking_uri', variable: 'MLFLOW_TRACKING_URI'),
        //                         string(credentialsId: 'mlflow_tracking_username', variable: 'MLFLOW_TRACKING_USERNAME'),
        //                         string(credentialsId: 'mlflow_tracking_password', variable: 'MLFLOW_TRACKING_PASSWORD')]) {

        //             sh """
        //             docker run -d -p 8080:8080 --name airflow-container \
        //                 -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
        //                 -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
        //                 -e MONGODB_URL="$MONGODB_URL" \
        //                 -e MLFLOW_TRACKING_URI="$MLFLOW_TRACKING_URI" \
        //                 -e MLFLOW_TRACKING_USERNAME="$MLFLOW_TRACKING_USERNAME" \
        //                 -e MLFLOW_TRACKING_PASSWORD="$MLFLOW_TRACKING_PASSWORD" \
        //                 airflow-image
        //             docker ps 
        //             """
        //             echo 'Docker container for Airflow is running.'
        //         }
        //     }
        // }

        // stage('5. Build Flask Docker Image') {
        //     steps {
        //         echo 'Building Flask Docker Image...'
        //         sh """
        //         docker build -f Dockerfile.Flask -t flask-image .
        //         """
        //         echo 'Flask Docker image built successfully.'
        //     }
        // }

        // stage('6. Create ECR repo for Flask Docker Images') {
        //     steps {
        //         echo 'Creating ECR repository for Flask Docker images...'
        //         withCredentials([string(credentialsId: 'access-key', variable: 'AWS_ACCESS_KEY'), 
        //                          string(credentialsId: 'secret-key', variable: 'AWS_SECRET_KEY')]) {
        //             sh """
        //             aws configure set aws_access_key_id $AWS_ACCESS_KEY
        //             aws configure set aws_secret_access_key $AWS_SECRET_KEY
        //             aws ecr describe-repositories --repository-names flask-docker-repo --region ap-south-1 || \
        //             aws ecr create-repository --repository-name flask-docker-repo --region ap-south-1
        //             """
        //         }
        //         echo 'ECR repository created or already exists.'
        //     }
        // }

        // stage('7. Login to flask-docker-repo ECR & tag image') {
        //     steps {
        //         echo 'Logging into ECR and tagging Flask Docker image...'
        //         withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
        //             sh """
        //             aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com
        //             docker tag flask-image ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/flask-docker-repo:${BUILD_NUMBER}
        //             docker tag flask-image ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/flask-docker-repo:latest
        //             """
        //         }
        //         echo 'Flask Docker image tagged successfully.'
        //     }
        // }

        // stage('8. Push image to ECR') {
        //     steps {
        //         echo 'Pushing Flask Docker image to ECR...'
        //         withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
        //             sh """
        //             docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/flask-docker-repo:${BUILD_NUMBER}
        //             docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/flask-docker-repo:latest
        //             """
        //         }
        //         echo 'Flask Docker image pushed to ECR successfully.'
        //     }
        // }

        // stage('9. Push image to flask-docker-repo ECR') {
        //     steps {
        //         echo 'Pushing Flask Docker image to flask-docker-repo ECR...'
        //         withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
        //             sh """
        //             docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/flask-docker-repo:${BUILD_NUMBER}
        //             docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/flask-docker-repo:latest
        //             """
        //         }
        //         echo 'Flask Docker image pushed to flask-docker-repo ECR successfully.'
        //     }
        // }

        // stage('10. Cleanup Flask Docker Image') {
        //     steps {
        //         echo 'Cleaning Flask up Docker images...'
        //         withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
        //             sh """
        //             docker rmi ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/flask-docker-repo:${BUILD_NUMBER}
        //             docker rmi ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/flask-docker-repo:latest
        //             docker rmi flask-image:latest
        //             docker images
        //             """
        //         }
        //         echo 'Cleaned up Flask Docker image.'
        //     }
        // }

        // stage('11. Flask web app deploy to Kubernetes') {
        //     steps {
        //         echo 'Starting Flask web app deployment to Kubernetes...'
        //         withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID'),
        //                         string(credentialsId: 'access-key', variable: 'AWS_ACCESS_KEY_ID'),
        //                         string(credentialsId: 'secret-key', variable: 'AWS_SECRET_ACCESS_KEY')]) {
        //             sh """
        //             aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com

        //             kubectl create secret generic my-secret \
        //             --from-literal=AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
        //             --from-literal=AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
        //             --dry-run=client -o yaml | kubectl apply -f -

        //             sed -i 's|\${AWS_ACCOUNT_ID}|'"${AWS_ACCOUNT_ID}"'|g' Kubernetes/deployment.yml
        //             kubectl apply -f Kubernetes/deployment.yml
        //             """
        //         }
        //         echo 'Flask web app deployment to Kubernetes completed.'
        //     }
        // }

        // stage('12. Restart Flask image Deployment to Apply Changes') {
        //     steps {
        //         echo 'Starting restart of Flask image deployment to apply changes...'
        //         script {
        //             sh "kubectl rollout restart deployment flask-image-deployment"
        //         }
        //         echo 'Flask image deployment restarted successfully.'
        //     }
        // }

        // stage('13. Expose Flask image Service in Kubernetes') {
        //     steps {
        //         echo 'Starting to expose Flask image service in Kubernetes...'
        //         sh "kubectl apply -f Kubernetes/service.yml"
        //         echo 'Flask image service exposed successfully in Kubernetes.'
        //     }
        // }


    }
}

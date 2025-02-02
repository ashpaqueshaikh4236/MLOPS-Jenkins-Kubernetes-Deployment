pipeline {
    agent any

    stages {
    //     stage('1. Git Checkout') {
    //         steps {
    //             git branch: 'main', url: 'https://github.com/ashpaqueshaikh4236/MLOPS-Jenkins-Kubernetes-Deployment.git'
    //         }
    //     }

        stage('2. Trivy Scan') {
            steps {
                sh "trivy fs . > trivy.txt"
            }
        }

        stage('3. Build Docker Image') {
            steps {
                sh "docker build -t my-flask-app ."
            }
        }

        stage('4. Create ECR repo') {
            steps {
                withCredentials([string(credentialsId: 'access-key', variable: 'AWS_ACCESS_KEY'), 
                                 string(credentialsId: 'secret-key', variable: 'AWS_SECRET_KEY')]) {
                    sh """
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY
                    aws configure set aws_secret_access_key $AWS_SECRET_KEY
                    aws ecr describe-repositories --repository-names mlops-project-repo --region ap-south-1 || \
                    aws ecr create-repository --repository-name mlops-project-repo --region ap-south-1
                    """
                }
            }
        }

        stage('5. Login to ECR & tag image') {
            steps {
                withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
                    sh """
                    aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com
                    docker tag my-flask-app ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:${BUILD_NUMBER}
                    docker tag my-flask-app ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:latest
                    """
                }
            }
        }

        stage('6. Push image to ECR') {
            steps {
                withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
                    sh """
                    docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:${BUILD_NUMBER}
                    docker push ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:latest
                    """
                }
            }
        }

        stage('7. Cleanup Images') {
            steps {
                withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {
                    sh """
                    docker rmi ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:${BUILD_NUMBER}
                    docker rmi ${AWS_ACCOUNT_ID}.dkr.ecr.ap-south-1.amazonaws.com/mlops-project-repo:latest
                    docker rmi my-flask-app
                    docker images
                    """
                    

                }
            }
        }

        stage('8. Deploy to Kubernetes') {
            steps {
                withCredentials([string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID')]) {

                    sh "kubectl apply -f Kubernetes/deployment.yml --validate=false"
                    
                }
            }
        }


        stage('9. Expose Service in Kubernetes') {
            steps {

                sh "kubectl apply -f Kubernetes/service.yml"

            }
        }

    }
}


module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.15.1"

  cluster_name                   = "My-cluster"
  cluster_endpoint_public_access = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
  }

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets

  eks_managed_node_groups = {
    My-nodes = {  
      min_size     = 1    
      max_size     = 5    
      desired_size = 1    

      instance_types = ["t2.large"]  
      capacity_type  = "ON_DEMAND"  

      tags = {
        ExtraTag = "My_Node"
      }
    }
  }

  tags = {
    Example = "My-cluster"
  }
}

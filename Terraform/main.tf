module "identity" {
  source = "./Modules/Identity"
}

module "network" {
  source             = "./Modules/Network"
  vpc-cidr           = var.vpc-cidr
  public-subnets     = var.public-subnets
  private-subnets    = var.private-subnets
  nat-gw-subnet-name = var.nat-gw-subnet-name
}

module "cluster" {
  source                     = "./Modules/Cluster"
  eks-subents-ids            = [for subnet in module.network.private-subnets : subnet.id]
  eks-control-plane-role-arn = module.identity.eks-control-plane-role.arn
  eks-worker-nodes-role-arn  = module.identity.eks-worker-nodes-role.arn
  eks-control-plane-sg-id    = module.network.control-plane-sg-id
  eks-worker-nodes-sg-id     = module.network.worker-nodes-sg-id
}

module "open-id-connect" {
  source            = "./Modules/OIDC"
  eks-oidc-provider = module.cluster.eks-oidc-provider
}

resource "null_resource" "kubeconfig" {
  provisioner "local-exec" {
    command = "aws eks update-kubeconfig --profile ${var.aws-profile} --region ${var.region} --name ${module.cluster.cluster-name}"
  }

  depends_on = [module.cluster]
}

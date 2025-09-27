output "eks-control-plane-role" {
  value = aws_iam_role.eks-control-plane-role
}

output "eks-worker-nodes-role" {
  value = aws_iam_role.eks-worker-nodes-role
}

variable "aws-profile" {
  type    = string
  default = "default"
}

variable "region" {
  type = string
}

variable "vpc-cidr" {
  type = string
}

variable "public-subnets" {
  type = list(object({
    name = string
    cidr = string
    zone = string
  }))
}

variable "private-subnets" {
  type = list(object({
    name = string
    cidr = string
    zone = string
  }))
}

variable "nat-gw-subnet-name" {
  type = string
}

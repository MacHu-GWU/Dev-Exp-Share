terraform {
  backend "s3" {
    profile = "eq_sanhe"
    bucket = "eq-sanhe-for-everything"
    key = "terraform/learn-tf/s3-backend.tfstate"
    region = "us-east-1"
  }
}
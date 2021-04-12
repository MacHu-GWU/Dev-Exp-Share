provider "aws" {
  profile   = "eq_sanhe"
  region    = "us-east-1"
}

resource "aws_s3_bucket" "eq-sanhe-learn-terraform-bucket" {
  bucket = "eq-sanhe-learn-terraform-bucket-${terraform.workspace}"
}
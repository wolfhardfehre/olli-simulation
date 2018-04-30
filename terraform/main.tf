module "network" {
  source = "./network"
}

provider "aws" {
  region     = "us-east-2"
}

resource "aws_key_pair" "deployer" {
  key_name   = "olli-deployer"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDTHKwpObNEf9C/gWU1xhOt8hUlltBGVzWFRGd7c0cucAtdazG9zhYSamc6NeCPFgreFnuNjPHbc0OQMPEhg+DZrUipuzbAQpGbPeeiqgTUkhDKsZdUPv9ffVlyL17UdA3OYxzu5e8NOTLXjaWUIBt+fyWjvqYu3HnKd3T84UePuVkCtYhofBkSj8+C1vaz/V0sn485MudiEOnq2b/tlhgw8Y7WJWiNUMvCvsvrbT4Z10cv206tTJrPCz05u0DC4WqUGZliHJf1XJ0XTsNGoLKOsgGfFbflzYvZ2h9ElUGRbENEuu4L8lubsobtEv5+EhABuhLpefZPKjmuH0rE/Msz"
}

resource "aws_instance" "olli-server" {
  ami           = "ami-976152f2"
  instance_type = "t2.micro"
  key_name = "${aws_key_pair.deployer.key_name}"
  vpc_security_group_ids = ["${module.network.security_group_id}"]
}

resource "aws_eip" "olli-ip" {
  instance = "${aws_instance.olli-server.id}"
  vpc = true
}

output "public_ip" {
  value = "${aws_eip.olli-ip.public_ip}"
}

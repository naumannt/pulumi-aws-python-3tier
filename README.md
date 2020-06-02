# Three-tier architecture using Pulumi, Python and AWS
## Project Contents
### VPC
To connect the second and third tier, we need to setup a shared VPC and respective subnets.

### Frontend Tier
Implements a simple structure to deploy a static frontend based on [this official example](https://github.com/pulumi/examples/tree/master/aws-py-static-website):
- Amazon S3 is used to store the website's contents.
- Amazon CloudFront is the CDN serving content.
- Amazon Route53 is used to set up the DNS for the website.
- Amazon Certificate Manager is used for securing things via HTTPS.

Credits go to `jaxxstorm`, `stack72` and the other Pulumi developers for this part!
Note that I added code to add a Route53 domain, otherwise it's just a copy of the example modified to fit into my stack.

### Backend Tier
We set up a simple EC2 instance into security groups able to connect to the database tier and be contacted from the internet gateway created ealier.

### Database Tier
We set up both a simple RDS Postgres-Instance into a security group to allow only the backend tier SG to connect, and a DynamoDB endpoint to allow applications in the backend tier to connect to DynamoDB directly without leaving AWS networking.

## Setting up the project:
1. Set up AWS(-CLI) beforehand. I recommend setting up a profile in your /.aws/credentials file and then referencing it via environment variable (`AWS_PROFILE`) or referencing the profile name in the Pulumi configuration.

2. create a Python virtualenv, activate it and install dependencies
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
3. use `pulumi up` to preview and start deployment

4. use `pulumi destroy` to destroy all deployed resources
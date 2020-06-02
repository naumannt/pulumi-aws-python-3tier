import pulumi_aws
from vpc_setup import shared_vpc, availableZones, subnet_application

ami=pulumi_aws.get_ami(filters=[
                {
                    "name": "name",
                    "values": ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"],
                },
                {
                    "name": "virtualization-type",
                    "values": ["hvm"],
                },
            ],
            most_recent=True,
            owners=["099720109477"])

ec2SecurityGroup = pulumi_aws.ec2.SecurityGroup(
    resource_name="pulumi-aws-example_application",
    vpc_id=shared_vpc.id,
    egress=[{
        'from_port' : '0',
        'to_port' : '0',
        'protocol' : '-1',
        'cidr_blocks' : ['0.0.0.0/0']
    }],
    ingress=[{
            'cidr_blocks' : ['0.0.0.0/0'],
            'from_port' : '80',
            'to_port' : '80',
            'protocol' : 'tcp',
            'description' : 'Allow internet access to instance'
        }])

ec2instance = pulumi_aws.ec2.Instance(
    resource_name="pulumi-aws-example",
    availability_zone=availableZones.names[0],
    security_groups=[ec2SecurityGroup.id],
    subnet_id=subnet_application.id,
    instance_type='t2.micro',
    ami=ami.id)
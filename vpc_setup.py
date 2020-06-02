import pulumi_aws

availableZones = pulumi_aws.get_availability_zones(state="available")

shared_vpc = pulumi_aws.ec2.Vpc(
    resource_name='pulumi-aws-example',
    assign_generated_ipv6_cidr_block=True,
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,enable_dns_support=True)

subnet_gateway = pulumi_aws.ec2.Subnet(
    resource_name='pulumi-aws-example_gateway',
    availability_zone=availableZones.names[0],
    cidr_block="10.0.10.0/24",
    vpc_id=shared_vpc.id)

subnet_application = pulumi_aws.ec2.Subnet(
    resource_name='pulumi-aws-example_application',
    availability_zone=availableZones.names[0],
    cidr_block="10.0.11.0/24",
    vpc_id=shared_vpc.id)

subnet_database = pulumi_aws.ec2.Subnet(
    resource_name='pulumi-aws-example_database',
    availability_zone=availableZones.names[0],
    cidr_block="10.0.12.0/24",
    vpc_id=shared_vpc.id)

subnet_database2 = pulumi_aws.ec2.Subnet(
    resource_name='pulumi-aws-example_database_2',
    availability_zone=availableZones.names[1],
    cidr_block="10.0.13.0/24",
    vpc_id=shared_vpc.id)

internet_gateway = pulumi_aws.ec2.InternetGateway(
    resource_name='pulumi-aws-example',
    vpc_id=shared_vpc.id)

gateway_eip = pulumi_aws.ec2.Eip(
    resource_name='pulumi-aws-example',
    vpc=True)

nat_gateway = pulumi_aws.ec2.NatGateway(
    resource_name='pulumi-aws-example',
    allocation_id=gateway_eip.id,
    subnet_id=subnet_gateway.id)

routetable_application = pulumi_aws.ec2.RouteTable(
    resource_name='pulumi-aws-example_application',
    vpc_id=shared_vpc.id,
    routes=[
        {
            "cidrBlock": "0.0.0.0/0",
            "gatewayId": nat_gateway.id
        }])

routetable_gateway = pulumi_aws.ec2.RouteTable(
    resource_name='pulumi-aws-example_gateway',
    vpc_id=shared_vpc.id,
    routes=[
        {
            "cidrBlock": "0.0.0.0/0",
            "gatewayId": internet_gateway.id
        }])

routetable_database = pulumi_aws.ec2.RouteTable(
    resource_name='pulumi-aws-example_database',
    vpc_id=shared_vpc.id)

routetableAssociation_application = pulumi_aws.ec2.RouteTableAssociation(
    resource_name='pulumi-aws-example_application',
    subnet_id=subnet_application.id,
    route_table_id=routetable_application)

routetableAssociation_database = pulumi_aws.ec2.RouteTableAssociation(
    resource_name='pulumi-aws-example_database',
    subnet_id=subnet_database.id,
    route_table_id=routetable_database.id)

routetableAssociation_gateway = pulumi_aws.ec2.RouteTableAssociation(
    resource_name='pulumi-aws-example_gateway',
    subnet_id=subnet_gateway.id,
    route_table_id=routetable_gateway.id)
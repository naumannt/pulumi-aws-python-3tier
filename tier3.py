import pulumi_aws
import vpc_setup
import tier2

databaseSecurityGroup = pulumi_aws.ec2.SecurityGroup(
    resource_name="pulumi-aws-example_database",
    vpc_id=vpc_setup.shared_vpc.id)

databaseSecurityGroupRule = pulumi_aws.ec2.SecurityGroupRule(
    resource_name="pulumi-aws-example",
    security_group_id=databaseSecurityGroup.id,
    source_security_group_id=tier2.ec2SecurityGroup,
    protocol="tcp",
    from_port=5432,
    to_port=5432,
    type="ingress"
    )

subnetGroup = pulumi_aws.rds.SubnetGroup(
    resource_name="pulumi-aws-example",
    subnet_ids=[vpc_setup.subnet_database.id, vpc_setup.subnet_database2.id]
)

database = pulumi_aws.rds.Instance(
    resource_name="pulumi-aws-example",
    db_subnet_group_name=subnetGroup,
    allocated_storage=20,
    port=5432,
    storage_type="gp2",
    engine="postgres",
    engine_version="10.6",
    instance_class="db.t2.micro",
    name="pulumiAwsExample",
    identifier="pulumi-aws-example",
    username="pulumiAwsExample",
    password="example1Password",
    apply_immediately=False,
    final_snapshot_identifier="pulumi-aws-example",
    skip_final_snapshot=False,
    vpc_security_group_ids=[databaseSecurityGroup.id]
)

dynamodbEndpoint = pulumi_aws.ec2.VpcEndpoint(
    resource_name="pulumi-aws-example_dynamodb",
    vpc_id=vpc_setup.shared_vpc.id,
    service_name="com.amazonaws.eu-west-1.dynamodb",
    route_table_ids=[vpc_setup.routetable_application.id]
)
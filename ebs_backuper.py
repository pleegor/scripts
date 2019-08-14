import boto3
import collections
import datetime

ec_inst = boto3.client('ec2')

def lambda_handler(event, context):
    reservations = ec_inst.describe_instances(
        Filters=[
            {'Name': 'tag:EBSBackup', 'Values': ['yes']},
        ]
    ).get(
        'Reservations', []
    )

    instances = [
        i for r in reservations
        for i in r['Instances']
    ]

    print "Found %d instances that need backing up" % len(instances)

    add_tag = collections.defaultdict(list)

    for instance in instances:
        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'Retention'][0]
        except IndexError:
            retention_days = 30

        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                continue
            vol_id = dev['Ebs']['VolumeId']
            print "Found EBS volume %s on instance %s" % (
                vol_id, instance['InstanceId'])

            snap = ec_inst.create_snapshot(
                VolumeId=vol_id,
            )

            add_tag[retention_days].append(snap['SnapshotId'])

            print "Retaining snapshot %s of volume %s from instance %s for %d days" % (
                snap['SnapshotId'],
                vol_id,
                instance['InstanceId'],
                retention_days,
            )


    for retention_days in add_tag.keys():
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        delete_fmt = delete_date.strftime('%Y-%m-%d')
        print "Will delete %d snapshots on %s" % (len(add_tag[retention_days]), delete_fmt)
        ec_inst.create_tags(
            Resources=add_tag[retention_days],
            Tags=[
                {'Key': 'DeleteOn', 'Value': delete_fmt},
            ]
        )

#!/usr/bin/env python

import boto.ec2.cloudwatch
import datetime
import time
import sys
from pyfirmata import Arduino


cw = boto.ec2.cloudwatch.connect_to_region("us-east-1")
asGroup = sys.argv[1];

arduino = Arduino('/dev/tty.usbmodem1421')
cpu_pin = arduino.get_pin('d:5:p')

def last_minute(metric, namespace, aggregation, dimensions):
  m = cw.get_metric_statistics(
      60,
      datetime.datetime.utcnow() - datetime.timedelta(seconds=120),
      datetime.datetime.utcnow(),
      metric,
      namespace,
      aggregation,
      dimensions
    )
  return m[len(m) - 1][aggregation]

def cpu_utilization(name):
    return last_minute(
      'CPUUtilization',
      'AWS/EC2',
      'Average',
      dimensions = {'AutoScalingGroupName':name}
    )

while True:
    cpu = cpu_utilization(asGroup)
    print '%s cpu: %2.2f' % (asGroup, cpu)

    cpu_pin.write(cpu / 100)
    
    time.sleep(10)

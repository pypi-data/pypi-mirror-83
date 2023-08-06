# -*- coding: utf-8 -*-
"""
This class allows you create logs in Amazon CloudWatch.
Within AWS CloudWatch, there are log groups and log streams. 
Log groups and log streams are defined by users. 
Usually an application's logs are within the same log group.
Within each log group are different log streams; Each log stream in a log group 
must have a unique log stream name.In this implementation, the log stream name 
is the date and time at which the cloudwatch object is created during runtime.

For more information, refer to documentation on Notion.
"""

from datetime import datetime
import time

import boto3

class Cloudwatch():
    
    def __init__(self, log_group_name, log_stream_name=None):
        log_stream_name = datetime.now().strftime("%Y/%m/%d  %H%M%S") \
                                    if not log_stream_name else log_stream_name
        group_name, stream_name = self.create_cloudwatch_logger(log_group_name, log_stream_name)
        self.log_group_name = group_name
        self.log_stream_name = stream_name
        self.sequence_token = None
                                        
    def create_cloudwatch_logger(self, log_group_name, log_stream_name):
        cw = boto3.client('logs')
        try:
            cw.create_log_group(logGroupName=log_group_name)
        except Exception as e:
            if 'ResourceAlreadyExistsException' != e.__class__.__name__:
                raise
        try:
            cw.create_log_stream(logGroupName=log_group_name,
                                 logStreamName=log_stream_name)
        except Exception as e:
            if 'ResourceAlreadyExistsException' != e.__class__.__name__:
                raise
        return log_group_name, log_stream_name
    
    def write_to_log_stream(self, message):
        timestamp =int(time.time() * 1000)
        event = {'timestamp': timestamp,
                 'message': message}
        cw = boto3.client('logs')
        if not self.sequence_token:
            response = cw.put_log_events(logGroupName=self.log_group_name,
                                         logStreamName=self.log_stream_name,
                                         logEvents=[event])
        else:
            response = cw.put_log_events(logGroupName=self.log_group_name,
                                         logStreamName=self.log_stream_name,
                                         logEvents=[event],
                                         sequenceToken=self.sequence_token)
        self.sequence_token = response['nextSequenceToken']
        
    def info(self, message, *args):
        message = '[INFO] ' + ((message % args) if args else message)
        self.write_to_log_stream(message)
        
    def exception(self, message, *args):
        message = '[EXCEPTION] ' + ((message % args) if args else message)
        self.write_to_log_stream(message)
        
    def warning(self, message, *args):
        message = '[WARNING] ' + ((message % args) if args else message)
        self.write_to_log_stream(message)
        
    
if __name__ == "__main__":        
    cw = Cloudwatch(log_group_name='test-logging')
    for i in range(2):
        cw.write_to_log_stream('test ' + str(i))


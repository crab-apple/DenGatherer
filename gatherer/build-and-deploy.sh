#!/bin/bash

set -e

original_artifact=target/gatherer-0.0.1-SNAPSHOT-zip-for-eb.zip
bucket=dengatherer-deploy
version_label=gatherer-$(date --utc -Iseconds)
target_file_name=$version_label.zip
application_name=$(eb config --display | grep ^ApplicationName: | awk '{print $2}')
environment_name=$(eb config --display | grep ^EnvironmentName: | awk '{print $2}')

mvn clean package
mvn assembly:single

aws s3 cp $original_artifact s3://$bucket/$target_file_name
aws elasticbeanstalk create-application-version --application-name $application_name --version-label $version_label --source-bundle S3Bucket="$bucket",S3Key="$target_file_name"
aws elasticbeanstalk update-environment --application-name $application_name --environment-name $environment_name --version-label $version_label


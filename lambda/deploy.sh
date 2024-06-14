#!/usr/bin/env zsh

# Create new virtualenv
# The venv has to be named `python` for Lambda to recognize it. 
# Ref: https://docs.aws.amazon.com/lambda/latest/dg/packaging-layers.html#packaging-layers-paths
BUILD_ENV=python
python -m venv $BUILD_ENV
source $BUILD_ENV/bin/activate
pip install .

# Zip up all Python dependencies, publish to S3
TIMESTAMP=$(date +%Y_%m_%d_%H_%M_%S)
LAYER_FILENAME=lambda_layer_${TIMESTAMP}.zip
zip -r $LAYER_FILENAME $BUILD_ENV
aws s3 cp $LAYER_FILENAME s3://acrossfc-lambda-layers/$LAYER_FILENAME

# Cleanup
rm -fr $BUILD_ENV
rm $LAYER_FILENAME

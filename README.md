# random-hungarian-proverb

AWS Lambda/API Gateway endpoint that returns a random Hungarian proverb

# Source of Hungarian proverbs

http://mek.oszk.hu/00200/00242/00242.htm

The `parse_source.py` script downloads and parses the HTML in order to get the
original Hungarian versions of the proverbs (and their potential alternate) and
their English translations. Dependencies can be found in `requirements-parse.txt`.

# Deployment

Using the [yoke](https://github.com/rackerlabs/yoke) tool:

```
export AWS_ACCESS_KEY_ID=<your-aws-access-key>
export AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
yoke deploy --stage=dev
```

TODO: set up the Lambda execution and API Gateway invoke IAM roles referenced
in the `yoke.yml` file.

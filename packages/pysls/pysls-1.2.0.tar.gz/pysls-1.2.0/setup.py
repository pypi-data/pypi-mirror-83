# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysls',
 'pysls.src',
 'pysls.src.create',
 'pysls.src.events',
 'pysls.src.localstack',
 'pysls.utils']

package_data = \
{'': ['*'],
 'pysls.src.events': ['model_files/alexa-skills-kit/*',
                      'model_files/alexa-smart-home/*',
                      'model_files/apigateway/*',
                      'model_files/batch/*',
                      'model_files/cloudformation/*',
                      'model_files/cloudfront/*',
                      'model_files/cloudwatch/*',
                      'model_files/codecommit/*',
                      'model_files/codepipeline/*',
                      'model_files/cognito/*',
                      'model_files/config/*',
                      'model_files/connect/*',
                      'model_files/dynamodb/*',
                      'model_files/kinesis/*',
                      'model_files/lex/*',
                      'model_files/rekognition/*',
                      'model_files/s3/*',
                      'model_files/sagemaker/*',
                      'model_files/ses/*',
                      'model_files/sns/*',
                      'model_files/sqs/*',
                      'model_files/stepfunctions/*']}

install_requires = \
['boto3>=1.15.16,<2.0.0']

entry_points = \
{'console_scripts': ['pysls = pysls.src.main:main']}

setup_kwargs = {
    'name': 'pysls',
    'version': '1.2.0',
    'description': '',
    'long_description': '<a href="https://codecov.io/gh/LucasFDutra/pysls">\n  <img src="https://codecov.io/gh/LucasFDutra/pysls/branch/master/graph/badge.svg" />\n</a>\n\n# OBJECTIVE\nTo facilitate the build of aws lambda projects in python. Building a directory structure, enabling deployment within the [localstack](https://github.com/localstack/localstack), invoke the function inside the container, view functions logs and create zip files to use for building layers.\n\n> NOTE.: If you use Windows, you may want to use Docker or WSL to build layers and build dependency packages, because some dependencies have C binaries. And the binaries on Linux are different from Windows, and lambda runs on Linux.\n\n# REQUIREMENTS\n\nIf you want to use localstack to run your tests, you need to install the docker. And to use the deploy function into the localstack, you will need the serverless framework too, so you will also need to install the node.\n\n- [docker](https://docs.docker.com/get-docker/)\n- [node](https://nodejs.org/en/)\n- [serverless](https://www.serverless.com/framework/docs/getting-started/)\n\n# HOW TO INSTALL\nTo install the application, just run the command below:\n\n```sh\n$ pip install pysls\n```\n\n# HOW TO USE\nOnce the package is installed, you can run it via the command line. The commands are as follows:\n\n---\n## CREATE FILE STRUCTURE\n\n```sh\n$ pysls --create_function=project_name\n```\nThe files structure is as follows:\n\n```sh\n├── docker-compose.yml\n├── lambda_test\n│   ├── __init__.py\n│   ├── src\n│   │   ├── lambda_function.py\n│   │   └── serverless.yml\n│   └── tests\n│       ├── integration\n│       ├── unit\n│       └── utils\n│           ├── files\n│           └── mocks\n├── pyproject.toml\n├── README.md\n└── requirements.txt\n```\n\n- `docker-compose.yml`: Contains a pre-assembled localstack structure;\n- `lambda_test/src/lambda_function.py`: This file contains the main function code, and any other files must exist within the src folder;\n- `lambda_test/src/serverless.yml`: Contains serverless framework settings (the localstack plugin is already included);\n- `tests`: Folder reserved for your tests;\n- `pyproject.toml`: This file is for those who want to use poetry as package manager, but pysls also needs it to retrieve information;\n- `requirements.txt`: pysls uses this file to create a layer and to build  a lambda function package to send to localstack.\n\n> OBS.: With the free version of localstack is not possible to use layers, but it is possible to send the code from the libraries together with the lambda code package.\n\n---\n## ASSEMBLING THE LAYER ZIP FILE\n\n```sh\n$ pysls --create_layer=layer_name\n```\n\nThis command will run the pip pointing to the folder `./python/lib/python+python_version/site-packages` as the final directory to place the library files, and after that it will compress the folder and delete it\n\n---\n## SEND TO LOCALSTACK\n\n```sh\n$ pysls --deploy\n```\n\nThis command will copy the `src` folder to `./src_tmp`, and after that it will run a npm command to add the `serverless-localstack` plugin. After that, it will add to the folder the libraries files that are listed in the file `requirements.txt`. The script will execute the deploy command into the localstack based on the deploy command of serverless framework. After all this, the folder `./src_tmp` will be deleted.\n\n> OBS.: The localstack must be active, if not, run the commando: `$ docker-compose -up`.\n\n## UPDATE FUNCTION CODE IN LOCALSTACK\n\n```sh\n$ pysls --update\n```\n\nThis command will do the same things as the `--deploy` command, but it will not create the entire structure again, it will just send the code, so this command is much faster. But, if you change the structure (memory, timeout, event, etc ...) you will need to run `--deploy` again.\n\n---\n## VIEW LOGS INSIDE THE LOCALSTACK\n\n```sh\n$ pysls --logs\n```\n\nThis command gets the settings inside the `pysls_config.json` file, and sets up the function\'s logGroupName: `/aws/lambda/<service_name>-dev-<function_name>`. With the full name, it is possible to view all logs related to the function.\n\n## CREATE A EVENT FILE\nAll lambda triggers send an event in json format. And [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-generate-event.html) is capable of generating these files for us, and with these files it is possible to go to their functions and test them. But I have implemented this function as well. I based all of my code on this part on SAM, and all of my event template files are a copy of the [SAM repository](https://github.com/aws/aws-sam-cli/tree/master/samcli/lib/generated_sample_events).\n\n```sh\n$ pysls --generate_event --service=aws_service --event_type=service_event --params --filename=event_file_name.json\n```\n\nExample:\n\n```sh\n# I will create an event.json file in my root folder, for a put s3 event in the my_bucket bucket, and the file that will trigger this event is in the lambda_folder folder and is named data.csv\n\n$ pysls --generate_event --service=s3 --event_type=put --bucket=my_bucket --key=lambda_folder/data.csv --filename=event.json\n```\n\n- All Services:\n  - `alexa-skills-kit`\n  - `alexa-smart-home`\n  - `apigateway`\n  - `batch`\n  - `cloudformation`\n  - `cloudfront`\n  - `codecommit`\n  - `codepipeline`\n  - `cognito`\n  - `config`\n  - `connect`\n  - `dynamodb`\n  - `cloudwatch`\n  - `kinesis`\n  - `lex`\n  - `rekognition`\n  - `s3`\n  - `sagemaker`\n  - `ses`\n  - `sns`\n  - `sqs`\n  - `stepfunctions`\n\nIf you execute the commands below, an event.json file will be created in your root folder, with the default parameters.\n\n```sh\n$ pysls --generate_event --service=s3 --event_type=put\n$ pysls --generate_event --service=alexa-skills-kit --event_type=end-session\n$ pysls --generate_event --service=dynamodb --event_type=update\n```\n\nIf you are interessted in know all events type in all services and all possible params, see the file [EVENT_INFO.md](https://github.com/LucasFDutra/pysls/blob/master/EVENT_INFO.md)\n\n---\n## EXECUTE THE FUNCTION BASED ON AN EVENT\n\n```sh\n$ pysls --invoke=event_file_path\n```\n\nThis command gets the settings inside `pysls_config.json` and with that it assembles the name that the function has inside the localstack `<service_name>-dev-<function_name>`. And use the python SDK to invoke lambda by passing the event file as a parameter. And then it shows the lambda\'s response.\n\nIt is possible not to send any files, in this case run the command `$ pysls --invoke`.\n\n## CONFIGURATIONS\n`serverless.yml` is the base configuration file for pysls. And it is extremely important that the project folder has the same name as the function described within the `serverless.yml` file.\n\n```sh\n├── docker-compose.yml\n├── lambda_test\n│   ├── __init__.py\n│   ├── src\n│   │   ├── lambda_function.py\n│   │   └── serverless.yml\n│   └── tests\n│       ├── integration\n│       ├── unit\n│       └── utils\n│           ├── files\n│           └── mocks\n├── pyproject.toml\n├── README.md\n└── requirements.txt\n```\n\n- serverless.yml\n  ```yaml\n  functions:\n    test_lambda:\n      handler: lambda_function.lambda_handler\n  ```\n\n# HOW TO CONTRIBUTE\n\n- Open an issue with your idea to discuss;\n- Then fork and send your pull request (please do not send too large pull requests).\n\n# FUTURE IDEAS\n\n- [x] Generate the event files by the tool itself;\n- [ ] Send to AWS\n- [ ] Add new future ideas kkk',
    'author': 'LucasFDutra',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LucasFDutra/pysls',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

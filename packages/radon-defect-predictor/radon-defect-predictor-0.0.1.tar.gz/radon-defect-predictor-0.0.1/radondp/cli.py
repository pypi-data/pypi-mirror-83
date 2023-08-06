import datetime
import io
import json
import joblib
import os
import pandas as pd
import requests

from ansiblemetrics import metrics_extractor as ansible_metrics_extractor
from toscametrics import metrics_extractor as tosca_metrics_extractor
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from dotenv import load_dotenv
from getpass import getpass
from repositoryscorer import scorer
from zipfile import ZipFile

from .predictors import DefectPredictor


def valid_dir(x: str) -> str:
    """
    Check the directory exists
    :param x: a path
    :return: the path if exists; raise an ArgumentTypeError otherwise
    """
    if not os.path.isdir(x):
        raise ArgumentTypeError('Insert a valid path')

    return x


def valid_file(x: str) -> str:
    """
    Check the file exists
    :param x: a path
    :return: the path if exists; raise an ArgumentTypeError otherwise
    """
    if not os.path.isfile(x):
        raise ArgumentTypeError('Insert a valid path')

    return x


def valid_balancers(x: str):
    """
    Check x is a list of valid balancers
    :param x: a string representing a list of balancers (e.g., "none rus ros")
    :return: the list of balancers if every argument in x is a valid balancer; raise an ArgumentTypeError otherwise
    """
    balancers = x.split(' ')
    for balancer in balancers:
        if balancer not in ('none', 'rus', 'ros'):
            raise ArgumentTypeError(f'{balancer} is not a valid argument')

    return balancers


def valid_normalizers(x: str):
    """
    Check x is a list of valid normalizers
    :param x: a string representing a list of normalizers (e.g., "none minmax std")
    :return: the list of normalizers if every argument in x is a valid normalizer; raise an ArgumentTypeError otherwise
    """
    normalizers = x.split(' ')
    for normalizer in normalizers:
        if normalizer not in ('none', 'minmax', 'std'):
            raise ArgumentTypeError(f'{normalizer} is not a valid argument')

    return normalizers


def valid_classifiers(x: str):
    """
    Check x is a list of valid classifiers
    :param x: a string representing a list of classifiers (e.g., "dt logit nb rf svm")
    :return: the list of classifiers if every argument in x is a valid classifier; raise an ArgumentTypeError otherwise
    """
    classifiers = x.split(' ')
    for classifier in classifiers:
        if classifier not in ('dt', 'logit', 'nb', 'rf', 'svm'):
            raise ArgumentTypeError(f'{classifier} is not a valid argument')

    return classifiers


def set_train_parser(subparsers):
    parser = subparsers.add_parser('train', help='Train a brand new model from scratch')
    parser.add_argument(action='store',
                        dest='path_to_csv',
                        type=valid_file,
                        help='the path to the csv file containing the data for training')

    parser.add_argument(dest='classifiers',
                        type=valid_classifiers,
                        help='a list of classifiers to train. Possible choices [dt, logit, nb, rf, svm]')

    parser.add_argument('-b', '--balancers',
                        required=False,
                        dest='balancers',
                        type=valid_balancers,
                        help='a list of balancer to balance training data. Possible choices [none, rus, ros]')

    parser.add_argument('-n', '--normalizers',
                        required=False,
                        dest='normalizers',
                        type=valid_normalizers,
                        help='a list of normalizers to normalize data. Possible choices [none, minmax, std]')

    # TODO: add feature-selectors


    """
    parser.add_argument('--verbose',
                        action='store_true',
                        dest='verbose',
                        default=False,
                        help='show log')
    """


def set_predict_parser(subparsers):
    parser = subparsers.add_parser('predict', help='Predict unseen instances')

    parser.add_argument(action='store',
                        dest='language',
                        type=str,
                        choices=['ansible', 'tosca'],
                        help='the language of the file (i.e., TOSCA or YAML-based Ansible)')

    parser.add_argument(action='store',
                        dest='path_to_artefact',
                        type=valid_file,
                        help='the path to the artefact to analyze (i.e., an Ansible or Tosca file or .csar')


def set_download_model_parser(subparsers):
    parser = subparsers.add_parser('download-model', help='Download a pre-trained model from the online APIs')

    parser.add_argument(action='store',
                        dest='language',
                        type=str,
                        choices=['ansible', 'tosca'],
                        help='the language the model is trained on')

    parser.add_argument(action='store',
                        dest='host',
                        type=str,
                        choices=['github', 'gitlab'],
                        help='the platform the user\'s repository is hosted to')

    parser.add_argument(action='store',
                        dest='repository_full_name_or_id',
                        type=str,
                        help='the remote repository full name or id (e.g., radon-h2020/radon-defect-prediction-cli)')

    parser.add_argument(action='store',
                        dest='path_to_repository',
                        type=valid_dir,
                        help='the local path to the user\'s repository')

    parser.add_argument('-t', '--token',
                        required=False,  # TODO: handle with environment variable
                        action='store',
                        dest='token',
                        type=str,
                        help='the Github or Gitlab personal access token')


def get_parser():
    description = 'A Python library to train machine learning models for defect prediction of infrastructure code'

    parser = ArgumentParser(prog='radon-defect-predictor', description=description)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')
    subparsers = parser.add_subparsers(dest='command')

    set_train_parser(subparsers)
    set_download_model_parser(subparsers)
    set_predict_parser(subparsers)

    return parser


def train(args: Namespace):
    dp = DefectPredictor()
    dp.balancers = args.balancers
    dp.normalizers = args.normalizers
    dp.classifiers = args.classifiers
    dp.train(pd.read_csv(args.path_to_csv))
    dp.dump_model(os.getcwd())
    exit(0)


def model(args: Namespace):
    load_dotenv()

    if not args.token:
        if args.host == 'github' and os.getenv('GITHUB_ACCESS_TOKEN'):
            args.token = os.getenv('GITHUB_ACCESS_TOKEN')
        elif args.host == 'gitlab' and os.getenv('GITLAB_ACCESS_TOKEN'):
            args.token = os.getenv('GITLAB_ACCESS_TOKEN')
        else:
            args.token = getpass('Github access token:')

    # TODO deal language {ansible, tosca}

    print('Downloading model...')
    scores = scorer.score_repository(
        path_to_repo=args.path_to_repository,
        access_token=args.token,
        full_name_or_id=args.repository_full_name_or_id,
        host=args.host
    )

    # TODO update depending on API body
    scores['commitFrequency'] = scores['commit_frequency']
    scores['coreContributors'] = scores['core_contributors']
    scores['issueFrequency'] = scores['issue_frequency']
    scores['percentComments'] = scores['percent_comment']
    scores['percentIac'] = scores['iac_ratio']
    scores['sloc'] = scores['repository_size']

    url = 'https://radon.giovanni.pink/api/models/pre-trained-model'
    response = requests.post(url, json=scores)

    if response.status_code != 200:
        print(f'Response returned status: {response.status_code}')
        exit(1)

    response_body = response.json()

    # TODO: move this process to the online APIs and make them return the joblib file

    if response_body['model'] and response_body['attributes']:
        joblib.dump({'model': response_body['model'],
                     'features': response_body['attributes']
                     }, os.path.join(os.getcwd(), 'radondp_model.joblib'))

    exit(0)


def predict(args: Namespace):
    dp = DefectPredictor()
    dp.load_model(os.getcwd())

    report = []

    # Extract metrics
    if args.language == 'ansible':
        # Read content of the script to analyze
        with open(args.path_to_artefact, 'r') as f:
            script_content = f.read()
        unseen_data = pd.DataFrame(ansible_metrics_extractor.extract_all(io.StringIO(script_content)), index=[0])
        prediction = dp.predict(unseen_data)
        report.append(dict(
            file=args.path_to_artefact,
            failure_prone=prediction,
            analyzed_at=str(datetime.date.today())
        ))

    else:  # tosca

        if args.path_to_artefact.endswith('.csar'):

            with ZipFile(args.path_to_artefact, 'r') as zip_file:
                for filepath in zip_file.namelist():
                    if filepath.endswith('.tosca'):
                        try:
                            script_content = zip_file.read(filepath).decode('utf-8')
                            unseen_data = pd.DataFrame(tosca_metrics_extractor.extract_all(io.StringIO(script_content)), index=[0])
                            prediction = dp.predict(unseen_data)
                            report.append(dict(
                                file=os.path.join(args.path_to_artefact, filepath),
                                failure_prone=prediction,
                                analyzed_at=str(datetime.date.today())
                            ))
                        except ValueError:
                            pass
        else:
            # Read content of the script to analyze
            with open(args.path_to_artefact, 'r') as f:
                script_content = f.read()

            unseen_data = pd.DataFrame(tosca_metrics_extractor.extract_all(io.StringIO(script_content)), index=[0])

            prediction = dp.predict(unseen_data)
            report.append(dict(
                file=args.path_to_artefact,
                failure_prone=prediction,
                analyzed_at=str(datetime.date.today())
            ))

    if report:
        destination = os.path.join(os.getcwd(), 'radondp_predictions.json')
        if os.path.isfile(destination):
            with open(destination, 'r') as f:
                report.extend(json.load(f))

        with open(destination, 'w') as f:
            json.dump(report, f)

    exit(0)


def main():
    args = get_parser().parse_args()
    if args.command == 'train':
        train(args)
    elif args.command == 'download-model':
        model(args)
    elif args.command == 'predict':
        predict(args)

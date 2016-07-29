import os
import re
from passepartout.strategies.github import GithubLocking


def lock(message, owner, repo):
    locking = GithubLocking(owner, repo, token=os.environ['GITHUB_TOKEN'])
    locking.lock()
    reply = 'https://github.com/{owner}/{repo} is locked'.format(owner=owner,
                                                                 repo=repo)
    return reply


def unlock(message, owner, repo):
    locking = GithubLocking(owner, repo, token=os.environ['GITHUB_TOKEN'])
    locking.unlock()
    reply = 'https://github.com/{owner}/{repo} is unlocked'.format(owner=owner,
                                                                   repo=repo)
    return reply


def status(message, owner, repo):
    locking = GithubLocking(owner, repo, token=os.environ['GITHUB_TOKEN'])
    response = locking.status()
    status = 'locked' if response else 'unlocked'
    reply = 'https://github.com/{owner}/{repo} is {status}'.format(owner=owner,
                                                                   repo=repo,
                                                                   status=status)
    return reply


actions = {
    'lock': {
        'regex': re.compile('lock (?P<owner>[\w-]+)/(?P<repo>[\w-]+)'),
        'callback': lock
    },
    'unlock': {
        'regex': re.compile('unlock (?P<owner>[\w-]+)/(?P<repo>[\w-]+)'),
        'callback': unlock
    },
    'status': {
        'regex': re.compile('status (?P<owner>[\w-]+)/(?P<repo>[\w-]+)'),
        'callback': status
    }
}

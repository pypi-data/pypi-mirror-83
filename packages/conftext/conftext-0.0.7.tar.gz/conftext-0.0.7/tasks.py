from invoke import run
from invoke import task


@task
def clean(ctxt):
    run('rm dist/*')


@task
def build(ctxt):
    run('python setup.py sdist bdist_wheel')


@task
def publish(ctxt):
    run('git push github')
    run('twine upload dist/*')

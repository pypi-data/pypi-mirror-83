# Python components of the Heptapod server

[![build status](https://foss.heptapod.net/heptapod/py-heptapod/badges/branch/default/build.svg)](https://foss.heptapod.net/heptapod/py-heptapod/commits/branch/default)
[![tests coverage](https://foss.heptapod.net/heptapod/py-heptapod/badges/branch/default/coverage.svg)](https://foss.heptapod.net/heptapod/py-heptapod/commits/branch/default)

[Heptapod](https://heptapod.net) is the friendly fork of GitLab that brings
Mercurial compatibility in. It is a system with multiple components, involving
several programmation languages, notably Ruby, Go and Python.

The purpose of this package is to centralize all Heptapod Python code that is
not (yet) in any other, more generic Python project (Mercurial, its extensions,
general-purpose libraries…), and keep them in a high state of quality.

## Scope and versioning policy

This Python project is not meant for anything else than being a component of
the Heptapod **server**, nor is it the whole of Heptapod, only
the parts that happen to be written in Python.

The interdependency with other Heptapod components is very tight, to the point
that they share common version numbers and tags and that using this Python
project in an Heptapod server with even a slight version mismatch is
expected to fail at this point.

This package is for now Python 2 only, meaning in particular that Python 3
utilities, such as the migration scripts are not hosted here yet.

We will migrate to Python 3 in one shot when Mercurial and hg-git do.

## Development guide

### Launching the tests

We have unit tests with `py.test`, they'd be typically run in a virtualenv.

```
virtualenv -p python2 venv
venv/bin/pip install -r install-requirements.txt -r test-requirements.txt
venv/bin/pytest
```

Note: relying on virtualenv activation to run the tests simply as `pytest` has
been playing tricks with us, but the direct form above worked in all cases

### Workflow rules

We follow the Heptapod default workflow. Please make a topic, and submit a
Merge Request.

Merge Request Pipelines have to pass, and coverage to stay at 100% for the MR
to be technically acceptable – we can help achieving these results, it's not
mandatory for submitting MRs and gather some feedback.


## Contents

### WSGI serving of repositories

Provided by `heptapod.wsgi` (not fully independent yet)


### Mercurial Hooks

`heptapod.hooks.check_publish.check_publish`:
   permission rules about public changesets in pushes.
`heptapod.hooks.git_sync.mirror`:
   synchronisation to inner auxiliary Git repository for exposition to GitLab
`heptapod.hooks.dev_util`: useful hooks for debug and development

### Mercurial extension

The `heptapod` extension will provide specific commands and generally everything
that should be done with full access to Mercurial internals.
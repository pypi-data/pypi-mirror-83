# platform-runtime-python36
SAMPv2 Runtime for python 3.6

## Writing User Code
At the time you create a model, you specify a handler, which is a function in your model, that runtime of model can invoke when the http request is received. Use the following general syntax structure when creating a handler function.

```
def handler(request, context):
    return {
        'status_code': 200,
        'content_type': 'application/json',
        'content': {'Hello': 'World!'},
    }
```

### Input

#### request
runtime of model will provide data by passing to `request` paramter.
`request` parameter is dict and file-like object.
you can get:

| key | gettable value |
| --- | -------------- |
| http_method | Request Http Method. (e.g. `GET`) |
| content_type | Request Content-Type |
| headers | Request Headers |
| contents | dict of Request contents |
| file_name | file name (only when Content-Type is `multipart/form-data` and set in `Content-Disposition`) |
| form_name | form name (only when Content-Type is `multipart/form-data` and set in `Content-Disposition`) |

Examples:
```
>>> request['http_method']
'POST'
>>> request['content_type']
'application/json'
>>> request['headers']
>>> [{'key': 'content-type', 'values': ['application/json']}, {'key': 'accept-encoding': 'values': ['gzip, deflate, br']}, ...]
>>> request.read()
b'{"foo": "bar"}'
```
```
>>> request['http_method']
'POST'
>>> request['content_type']
'multipart/form-data'
>>> contents = request['contents']
>>> contents[0]['content_type']
'application/json'
>>> contents[0]['form_name']
'file1'
>>> contents[0].read()
b'{"foo": "bar"}'
>>> contents[1]['content_type']
'image/jpeg'
>>> contents[1]['file_name']
'cat.jpg'
...
```

#### context
Now, `context` is empty dict.

### Output
You need to return `dict` including the following elements.

| key | value |
| --- | ----- |
| status_code | HTTP Status Code of Response. (default: `http.HTTPStatus.OK`) |
| content_type | Content-Type of Response. (default: `text/plain`) |
| content | Response Body |
| metadata | Additional HTTP Header of Response |

### Example
```
def handler(request, context):

    # some inference process...

    content = {
        'transaction_id': 1234567890,
        'category_id': 10,
        'predictions': predictions,
    }
    return {
        'status_code': http.HTTPStatus.OK,
        'content_type': 'application/json; charset=utf8',
        'content': content
    }

```

## Development

### Prerequisite
You need [pipenv](https://pipenv.readthedocs.io/en/latest/):
```
$ pip install pipenv
$ echo 'eval "$(pipenv --completion)"' >> ~/.bash_profile
$ source ~/.bash_profile
```

And, if you want to manage python version by [pyenv](https://github.com/pyenv/pyenv), you need install pyenv.
```
$ git clone git://github.com/yyuu/pyenv.git ~/.pyenv
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
$ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
$ source ~/.bash_profile
```

### Init
```
$ pipenv install
```

### Start/End Development
When you start develop:
```
$ pipenv shell
```

When you end develop:
```
$ pipenv exit
```

If it is troublesome, you can use [direnv](https://github.com/direnv/direnv).

### Test with samp-v2 (platform-model-proxy)

Setup platform-model-proxy according to [setup guide](https://github.com/abeja-inc/platform-model-proxy#setup-python-runtime)

To use developing python runtime (`abeja-runtime-python`), remove default python runtime.
```
$ pip uninstall abejaruntime
```

To use developing python runtime. Intall python runtime from current directory.
```
$ pip install -e .
```

Code change will be applied to the `abejaruntime` command immediately.

For example, try changing the version of the command.
Before changing,
```
$ abeja-runtime-python --version
INFO: start executing model with abeja-runtime-python (version: 1.0.0)
```

Make change
```diff
diff --git a/abejaruntime36/version.py b/abejaruntime36/version.py
index 6cc293e..12a5972 100644
--- a/abejaruntime36/version.py
+++ b/abejaruntime36/version.py
@@ -1 +1 @@
-VERSION = "0.4.0"
+VERSION = "x.y.z"
```
After change,
```
$ abeja-runtime-python --version
INFO: start executing model with abeja-runtime-python (version: x.y.z)
```



### Check code
You can check code with [mypy](http://mypy-lang.org/) and [flake8](http://flake8.pycqa.org/en/latest/).
```
$ make lint
```

### Run Tests
You can run tests with [pytest](https://docs.pytest.org/en/latest/).
```
$ make test
```

## Deploy
Use git-flow.

Synchronize master and develop branch.
```
$ git checkout master
$ git pull --rebase origin master
$ git checkout develop
$ git pull --rebase origin develop
```

Create release branch and prepare for release.
```
$ git flow release start X.X.X
# update to new version
$ vim abejaruntime36/version.py
$ vim CHANGELOG.md
$ git add CHANGELOG.md
$ git add abejaruntime36/version.py
$ git commit -m "bump version"
```

Pre-release.
```
$ git flow release publish X.X.X
```
X.X.X`rc1` version will be released to PyPI.

Release.
```
$ git flow release finish X.X.X
$ git push origin develop
$ git push origin X.X.X
$ git push origin master
```
X.X.X version will be released to PyPI.

## Contribution
> Feel free to ask the team directly about the best way to contribute!

[gitflow](https://github.com/nvie/gitflow) branching model is used, if you have a feature you want to contribute create a feature/FEATURE-NAME branch from the "develop" branch, and issue a Pull-Request to have your feature integrated.

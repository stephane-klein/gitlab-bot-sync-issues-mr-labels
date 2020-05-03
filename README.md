
# GitLab bot to sync Issues labels and MergeRequest labels

GitLab bot behaviours:

- When a user update GitLab issue labels, if this issue is closed only by one Merge Request then this GitLab Bot synchronise Merge Request labels with issue labels.
- When a user update GitLab Merge Request labels, GitLab Bot synchronise issues labels closed by this issue, only if this issue are closed by only one Merge Request.

## Usage

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

```
$ cp .env.sample .env
```

Update `label_sync_filter` function in `main.py` to configure the label to sync.

Configure:

- GitLab Webhook
- GitLab Access Tokens

Update `.env` file with GitLab secrets.

```
$ source .env
```

Start bot:

```
$ python main.py
```

Optionnal: in another terminal, create a SSH port forwarding to develop on laptop behind NAT network:

```
$ ssh -R 127.0.0.1:8080:0.0.0.0:8080 triton
```

## Ressources

Tools:

- [beenje/gidgetlab](https://gitlab.com/beenje/gidgetlab) - An async GitLab API library for Python based on https://github.com/brettcannon/gidgethub
- [python-gitlab/python-gitlab](https://github.com/python-gitlab/python-gitlab) - Python wrapper for the GitLab API

API v4:

- [Merge requests API](https://docs.gitlab.com/ee/api/merge_requests.html)

# GitLab bot to sync Issues labels and MergeRequest labels

GitLab bot behaviours:

- When a user update GitLab issue labels, if this issue is closed only by one Merge Request then this GitLab Bot synchronise Merge Request labels with issue labels.
- When a user update GitLab Merge Request labels, GitLab Bot synchronise issues labels closed by this issue, only if this issue are closed by only one Merge Request.

## GitLab configuration

```
$ cp .source.sample .source
```

- Create [GitLab Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token)
  - Select `api` scope
  - Fill ` Your New Personal Access Token` in `GL_ACCESS_TOKEN` in `.env`
- Create [GitLab Webhooks](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html)
  - Fill URL with url where is hosted `gitlab-bot` service
  - Generate `Secret Token` and fill this value in `GL_SECRET` in `.env`

## Usage without Docker

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Update `label_sync_filter` function in `main.py` to configure the label to sync.

```
$ source .source
```

Start bot:

```
$ python main.py
```

Optionnal: in another terminal, create a SSH port forwarding to develop on laptop behind NAT network:

```
$ ssh -R 127.0.0.1:8080:0.0.0.0:8080 triton
```

## Build Docker image

```
$ ./scripts/build-docker-image.sh
```

## Usage with Docker

```
$ source .source
$ docker-compose up -d
```

## Ressources

Tools:

- [beenje/gidgetlab](https://gitlab.com/beenje/gidgetlab) - An async GitLab API library for Python based on https://github.com/brettcannon/gidgethub
- [python-gitlab/python-gitlab](https://github.com/python-gitlab/python-gitlab) - Python wrapper for the GitLab API

API v4:

- [Merge requests API](https://docs.gitlab.com/ee/api/merge_requests.html)

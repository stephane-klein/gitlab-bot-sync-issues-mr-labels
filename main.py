import os
import logging

import gitlab
from gidgetlab.aiohttp import GitLabBot

from utils import labels_sync

logger = logging.getLogger("bot")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

bot = GitLabBot(os.getenv("BOT_USERNAME", "gitlab-bot"))

gl = gitlab.Gitlab(
    os.getenv("GL_URL", "https://gitlab.com"),
    private_token=os.getenv("GL_ACCESS_TOKEN")
)

# See GitLab events https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#merge-request-events


def label_sync_filter(label):
    return label.startswith("workflow::")


@bot.router.register("Issue Hook")
async def issue_event(event, *args, **kwargs):
    logger.debug("issue_opened_event")
    if "labels" not in event.data["changes"]:
        logger.debug("Labels not chaned")
        return

    source_labels = set(
        [item["title"] for item in event.data["changes"]["labels"]["current"]]
    )

    issue_obj = gl.projects.get(id=event.data["project"]["id"]).issues.get(
        id=event.data["object_attributes"]["iid"]
    )
    if len(issue_obj.closed_by()) > 1:
        logger.info(
            "Issue %s/#%s have several closed by merge request, then Issue Labels isn't sync with Issue "
            % (path_with_namespace, event.data["object_attributes"]["iid"])
        )
        return

    for mr in issue_obj.closed_by():
        mr_obj = gl.projects.get(id=mr["project_id"]).mergerequests.get(id=mr["iid"])
        new_labels = labels_sync(
            source=source_labels,
            destination=set(mr_obj.labels),
            sync_filter=label_sync_filter,
        )

        if set(mr_obj.labels) != new_labels:
            logger.info("Update MergeRequest #%s labels " % mr_obj.iid)
            logger.debug("Previous labels %s" % mr_obj.labels)
            logger.debug("News labels %s" % new_labels)
            mr_obj.labels = list(new_labels)
            mr_obj.save()


@bot.router.register("Merge Request Hook")
async def merge_request_event(event, *args, **kwargs):
    logger.debug("merge_request_event")
    if "labels" not in event.data["changes"]:
        logger.debug("Labels not chaned")
        return

    source_labels = set(
        [item["title"] for item in event.data["changes"]["labels"]["current"]]
    )

    mr_obj = gl.projects.get(id=event.data["project"]["id"]).mergerequests.get(
        id=event.data["object_attributes"]["iid"]
    )
    for issue_obj in mr_obj.closes_issues():
        if len(issue_obj.closed_by()) > 1:
            logger.info(
                "Issue #%s have several closed by merge request, then Issue Labels isn't sync with MergeRequest "
                % (issue_obj.iid)
            )
            continue

        new_labels = labels_sync(
            source=source_labels,
            destination=set(issue_obj.labels),
            sync_filter=label_sync_filter,
        )
        if set(issue_obj.labels) != new_labels:
            logger.info("Update Issue #%s labels " % issue_obj.iid)
            logger.debug("Previous labels %s" % issue_obj.labels)
            logger.debug("News labels %s" % new_labels)
            issue_obj.labels = list(new_labels)
            issue_obj.save()

bot.run()
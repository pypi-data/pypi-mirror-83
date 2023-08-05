# Copyright (C) 2020  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from .base import PROJECT, PULL_REQUEST, PULL_REQUEST_FLAG, PagureMessage, SCHEMA_URL


class PullRequestAssignedAddedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.request.assigned.added"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "request": PULL_REQUEST,
            "project": PROJECT,
        },
        "required": ["agent", "request", "project"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-request {name}#{id} was assigned\nBy: {agent}".format(
            agent=self.body["agent"],
            name=self.body["request"]["project"]["fullname"],
            id=self.body["request"]["id"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{username} assigned the pull-request {name}#{id} to {assignee}".format(
            name=self.body["request"]["project"]["fullname"],
            id=self.body["request"]["id"],
            username=self.body["agent"],
            assignee=self.body["request"]["assignee"]["name"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["request"]["project"]["url_path"]
        prid = self.body["request"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestAssignedResetV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.request.assigned.reset"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "request": PULL_REQUEST,
            "project": PROJECT,
        },
        "required": ["agent", "request", "project"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-request {name}#{id} was un-assigned\nBy: {agent}".format(
            agent=self.body["agent"],
            name=self.body["request"]["project"]["fullname"],
            id=self.body["request"]["id"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{username} reset the assignee of the pull-request {name}#{id}".format(
            name=self.body["request"]["project"]["fullname"],
            id=self.body["request"]["id"],
            username=self.body["agent"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        prid = self.body["request"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestClosedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.closed"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
            "merged": {"type": "boolean"},
        },
        "required": ["agent", "pullrequest", "merged"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-Request: {fullname}#{id} has been {action}\nBy: {agent}".format(
            fullname=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            agent=self.body["agent"],
            action="merged" if self.body["merged"] else "closed without merging",
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} {action} the pull-request {name}#{id}".format(
            agent=self.body["agent"],
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            action="merged" if self.body["merged"] else "closed without merging",
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["pullrequest"]["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestCommentAddedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.comment.added"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
        },
        "required": ["agent", "pullrequest"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-Request: {fullname}#{id} has a new comment\nBy: {agent}".format(
            fullname=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} commented on the pull-request {name}#{id}".format(
            agent=self.body["agent"],
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["pullrequest"]["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]
        commentid = self.body["pullrequest"]["comments"][-1]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}#comment-{commentid}"
        return tmpl.format(
            base_url=base_url, fullname=fullname, prid=prid, commentid=commentid
        )


class PullRequestFlagAddedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.flag.added"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
            "flag": PULL_REQUEST_FLAG,
        },
        "required": ["agent", "pullrequest", "flag"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "New pull-request flag: {username} {status}\nBy: {agent}".format(
            agent=self.body["agent"],
            username=self.body["flag"]["username"],
            status=self.body["flag"]["status"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "Pull-request {name}#{id} was flagged as {status} by {username}".format(
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            username=self.body["flag"]["username"],
            status=self.body["flag"]["status"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["pullrequest"]["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestFlagUpdatedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.flag.updated"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
            "flag": PULL_REQUEST_FLAG,
        },
        "required": ["agent", "pullrequest", "flag"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-request flag updated: {username} {status}\nBy: {agent}".format(
            agent=self.body["agent"],
            username=self.body["flag"]["username"],
            status=self.body["flag"]["status"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{username} updated flag on pull-request {name}#{id} to {status}".format(
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            username=self.body["flag"]["username"],
            status=self.body["flag"]["status"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["pullrequest"]["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestInitialCommentEditedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.initial_comment.edited"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "pullrequest": PULL_REQUEST,
        },
        "required": ["agent", "pullrequest", "project"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Description of pull-request {name}#{id} edited\nBy: {agent}".format(
            agent=self.body["agent"],
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{username} has edited the description of the pull-request {name}#{id}".format(
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            username=self.body["agent"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestNewV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.new"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
        },
        "required": ["agent", "pullrequest"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "New Pull-Request: {fullname}#{id}\nBy: {agent}".format(
            fullname=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} opened a pull-request {fullname}#{id}: {title}".format(
            agent=self.body["agent"],
            fullname=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            title=self.body["pullrequest"]["title"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["pullrequest"]["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestRebasedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.rebased"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
        },
        "required": ["agent", "pullrequest"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-request {name}#{id} was rebased\nBy: {agent}".format(
            agent=self.body["agent"],
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{username} rebased the pull-request {name}#{id}".format(
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            username=self.body["agent"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["pullrequest"]["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestReopenedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.reopened"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
        },
        "required": ["agent", "pullrequest"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-request {name}#{id} was re-opened\nBy: {agent}".format(
            agent=self.body["agent"],
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{username} re-opened the pull-request {name}#{id}".format(
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            username=self.body["agent"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["pullrequest"]["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestTagAddedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.tag.added"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
            "project": PROJECT,
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent", "pullrequest", "project", "tags"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-request {name}#{id} was tagged\nBy: {agent}".format(
            agent=self.body["agent"],
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{username} tagged the pull-request {name}#{id} with {tags}".format(
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            username=self.body["agent"],
            tags=", ".join(self.body["tags"]),
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestTagRemovedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.tag.removed"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
            "project": PROJECT,
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent", "pullrequest", "project", "tags"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-request {name}#{id} was un-tagged\nBy: {agent}".format(
            agent=self.body["agent"],
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{username} un-tagged the pull-request {name}#{id} with: {tags}".format(
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            username=self.body["agent"],
            tags=", ".join(self.body["tags"]),
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)


class PullRequestUpdatedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.pull-request.updated"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "pullrequest": PULL_REQUEST,
        },
        "required": ["agent", "pullrequest"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Pull-request {name}#{id} was updated\nBy: {agent}".format(
            agent=self.body["agent"],
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{username} updated the pull-request {name}#{id}".format(
            name=self.body["pullrequest"]["project"]["fullname"],
            id=self.body["pullrequest"]["id"],
            username=self.body["agent"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["pullrequest"]["project"]["url_path"]
        prid = self.body["pullrequest"]["id"]

        tmpl = "{base_url}/{fullname}/pull-request/{prid}"
        return tmpl.format(base_url=base_url, fullname=fullname, prid=prid)

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

from .base import GIT_RECEIVE_USER, PROJECT, PagureMessage, SCHEMA_URL


class GitBranchCreationV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.git.branch.creation"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "repo": PROJECT,
            "tag": {"type": "string"},
            "rev": {"type": "string"},
            "authors": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent", "repo", "branch", "rev", "authors"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Git branch: {branch} created\nBy: {agent}".format(
            branch=self.body["branch"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} created the branch {branch} on {name}".format(
            agent=self.body["agent"],
            name=self.body["repo"]["fullname"],
            branch=self.body["branch"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["repo"]["url_path"]

        item = self.body["branch"]
        if "refs/heads/" in item:
            item = item.replace("refs/heads/", "")

        tmpl = "{base_url}/{fullname}/tree/{item}"
        return tmpl.format(base_url=base_url, fullname=fullname, item=item)


class GitBranchDeletionV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.git.branch.deletion"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "repo": PROJECT,
            "tag": {"type": "string"},
            "rev": {"type": "string"},
            "authors": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent", "repo", "branch", "rev", "authors"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Git branch: {branch} deleted\nBy: {agent}".format(
            branch=self.body["branch"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} deleted the branch {branch} on {name}".format(
            agent=self.body["agent"],
            name=self.body["repo"]["fullname"],
            branch=self.body["branch"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["repo"]["url_path"]

        tmpl = "{base_url}/{fullname}"
        return tmpl.format(base_url=base_url, fullname=fullname)


class GitReceiveV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.git.receive"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "forced": {"type": "boolean"},
            "repo": PROJECT,
            "old_commit": {"type": "string"},
            "branch": {"type": "string"},
            "authors": {"type": "array", "items": GIT_RECEIVE_USER},
            "total_commits": {"type": "number"},
            "start_commit": {"type": "string"},
            "end_commit": {"type": "string"},
        },
        "required": [
            "agent",
            "forced",
            "repo",
            "old_commit",
            "branch",
            "authors",
            "total_commits",
            "start_commit",
            "end_commit",
        ],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "New commit: {count} commits\nBy: {agent}".format(
            count=self.body["total_commits"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} pushed {count} commits on {fullname} (branch: {branch})".format(
            agent=self.body["agent"],
            fullname=self.body["repo"]["fullname"],
            count=self.body["total_commits"],
            branch=self.body["branch"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["repo"]["url_path"]

        item = self.body["branch"]
        if "refs/heads/" in item:
            item = item.replace("refs/heads/", "")

        tmpl = "{base_url}/{fullname}/tree/{item}"
        return tmpl.format(base_url=base_url, fullname=fullname, item=item)


class GitTagCreationV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.git.tag.creation"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "repo": PROJECT,
            "tag": {"type": "string"},
            "rev": {"type": "string"},
            "authors": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent", "repo", "tag", "rev", "authors"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Git tag: {tag} created\nBy: {agent}".format(
            tag=self.body["tag"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} tagged the commit {rev} on {name} as {tag}".format(
            agent=self.body["agent"],
            name=self.body["repo"]["fullname"],
            tag=self.body["tag"],
            rev=self.body["rev"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["repo"]["url_path"]
        tag = self.body["tag"]

        tmpl = "{base_url}/{fullname}/commits/{tag}"
        return tmpl.format(base_url=base_url, fullname=fullname, tag=tag)


class GitTagDeletionV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.git.tag.deletion"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "repo": PROJECT,
            "tag": {"type": "string"},
            "rev": {"type": "string"},
            "authors": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent", "repo", "tag", "rev", "authors"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Git tag: {tag} deleted\nBy: {agent}".format(
            tag=self.body["tag"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} deleted the tag {tag} of commit {rev} on {name}".format(
            agent=self.body["agent"],
            name=self.body["repo"]["fullname"],
            tag=self.body["tag"],
            rev=self.body["rev"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["repo"]["url_path"]

        tmpl = "{base_url}/{fullname}/releases"
        return tmpl.format(base_url=base_url, fullname=fullname)

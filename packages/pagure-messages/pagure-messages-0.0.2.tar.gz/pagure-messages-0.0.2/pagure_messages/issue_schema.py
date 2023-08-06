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

from .base import ISSUE, PROJECT, PagureMessage, SCHEMA_URL


class IssueAssignedAddedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when an issue is deleted.
    """

    topic = "pagure.issue.assigned.added"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
        },
        "required": ["agent", "project", "issue"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Issue: {fullname}#{id} assigned to {assignee}\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
            assignee=self.body["issue"]["assignee"]["name"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} assigned issue {name}#{id} to {assignee}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            assignee=self.body["issue"]["assignee"]["name"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        issueid = self.body["issue"]["id"]

        tmpl = "{base_url}/{fullname}/issue/{issueid}"
        return tmpl.format(base_url=base_url, fullname=fullname, issueid=issueid)


class IssueAssignedResetV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when an issue is deleted.
    """

    topic = "pagure.issue.assigned.reset"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
        },
        "required": ["agent", "project", "issue"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Issue un-assigned: {fullname}#{id}\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} reset the assignee on issue {name}#{id}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        issueid = self.body["issue"]["id"]

        tmpl = "{base_url}/{fullname}/issue/{issueid}"
        return tmpl.format(base_url=base_url, fullname=fullname, issueid=issueid)


class IssueCommentAddedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when an issue is deleted.
    """

    topic = "pagure.issue.comment.added"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
        },
        "required": ["agent", "project"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Issue: {fullname}#{id} has a new comment\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} commented on the issue {name}#{id}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        issueid = self.body["issue"]["id"]
        commentid = self.body["issue"]["comments"][-1]["id"]

        tmpl = "{base_url}/{fullname}/issue/{issueid}#comment-{commentid}"
        return tmpl.format(
            base_url=base_url, fullname=fullname, issueid=issueid, commentid=commentid
        )


class IssueDependencyAddedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when an issue is deleted.
    """

    topic = "pagure.issue.dependency.added"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
            "added_dependency": {"type": "number"},
        },
        "required": ["agent", "project", "added_dependency"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Issue: {fullname}#{id} depends on #{depissueid}\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
            depissueid=self.body["added_dependency"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} set the issue {name}#{id} as depending on #{depissueid}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            depissueid=self.body["added_dependency"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        issueid = self.body["issue"]["id"]

        tmpl = "{base_url}/{fullname}/issue/{issueid}"
        return tmpl.format(base_url=base_url, fullname=fullname, issueid=issueid)


class IssueDependencyRemovedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when an issue is deleted.
    """

    topic = "pagure.issue.dependency.removed"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
            "removed_dependency": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["agent", "project", "removed_dependency"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Issue: {fullname}#{id} no longer depending on #{depissueid}\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
            depissueid=", #".join([str(i) for i in self.body["removed_dependency"]]),
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} removed the dependency on #{depissueid} on the issue {name}#{id}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            depissueid=", #".join([str(i) for i in self.body["removed_dependency"]]),
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        issueid = self.body["issue"]["id"]

        tmpl = "{base_url}/{fullname}/issue/{issueid}"
        return tmpl.format(base_url=base_url, fullname=fullname, issueid=issueid)


class IssueDropV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when an issue is deleted.
    """

    topic = "pagure.issue.drop"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
        },
        "required": ["agent", "project", "issue"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Issue deleted: {fullname}#{id}\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} deleted issue {name}#{id}: {title}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            title=self.body["issue"]["title"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]

        tmpl = "{base_url}/{fullname}/issues"
        return tmpl.format(base_url=base_url, fullname=fullname)


class IssueEditV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when an issue is updated.
    """

    topic = "pagure.issue.edit"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
            "fields": {"type": "array", "items": {"type": ["string", "null"]}},
        },
        "required": ["agent", "project", "issue", "fields"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Edited Issue: {fullname}#{id}\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} edited fields {fields} of issue {name}#{id}: {title}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            title=self.body["issue"]["title"],
            fields=", ".join(self.body["fields"]),
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        issueid = self.body["issue"]["id"]

        tmpl = "{base_url}/{fullname}/issue/{issueid}"
        return tmpl.format(base_url=base_url, fullname=fullname, issueid=issueid)


class IssueNewV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when a new thing is created.
    """

    topic = "pagure.issue.new"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
        },
        "required": ["agent", "project", "issue"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "New Issue: {fullname}#{id}\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} created issue {name}#{id}: {title}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            title=self.body["issue"]["title"],
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        issueid = self.body["issue"]["id"]

        tmpl = "{base_url}/{fullname}/issue/{issueid}"
        return tmpl.format(base_url=base_url, fullname=fullname, issueid=issueid)


class IssueTagAddedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when an issue is deleted.
    """

    topic = "pagure.issue.tag.added"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent", "project"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Issue: {fullname}#{id} tagged with {tags}\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
            tags=", ".join(self.body["tags"]),
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} tagged the issue {name}#{id} with: {tags}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            tags=", ".join(self.body["tags"]),
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        issueid = self.body["issue"]["id"]

        tmpl = "{base_url}/{fullname}/issue/{issueid}"
        return tmpl.format(base_url=base_url, fullname=fullname, issueid=issueid)


class IssueTagRemovedV1(PagureMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by pagure when an issue is deleted.
    """

    topic = "pagure.issue.tag.removed"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new project is created",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "project": PROJECT,
            "issue": ISSUE,
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent", "project"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return "Issue: {fullname}#{id} un-tagged with {tags}\nBy: {agent}".format(
            fullname=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            agent=self.body["agent"],
            tags=", ".join(self.body["tags"]),
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return "{agent} removed tags {tags} from issue {name}#{id}".format(
            agent=self.body["agent"],
            name=self.body["project"]["fullname"],
            id=self.body["issue"]["id"],
            tags=", ".join(self.body["tags"]),
        )

    @property
    def url(self):
        base_url = self.get_base_url()
        fullname = self.body["project"]["url_path"]
        issueid = self.body["project"]["id"]

        tmpl = "{base_url}/{fullname}/issue/{issueid}"
        return tmpl.format(base_url=base_url, fullname=fullname, issueid=issueid)

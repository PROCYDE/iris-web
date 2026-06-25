#  IRIS Source Code
#  Copyright (C) 2021 - Airbus CyberSecurity (SAS)
#  ir@cyberactionlab.net
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Note: Artifact functionalty not available in pr10_head. This module provides stub implementations.

from typing import List, Optional


def get_artifacts(caseid):
    """Get artifacts for a case. Feature not available in pr10_head."""
    return []


def get_artifacts_by_case(case_identifier) -> list:
    """Get artifacts by case. Feature not available in pr10_head."""
    return []


def get_artifact(artifact_id, caseid=None):
    """Get a specific artifact. Feature not available in pr10_head."""
    return None


def update_artifact(artifact_type, artifact_tags, artifact_value, artifact_description, artifact_tlp, userid, artifact_id):
    """Update an artifact. Feature not available in pr10_head."""
    return False


def escalate_artifact(artifact, caseid):
    """Escalate an artifact. Feature not available in pr10_head."""
    return True


def delete_artifact(artifact, caseid):
    """Delete an artifact. Feature not available in pr10_head."""
    return True


def add_artifact(artifact_type, artifact_tags, artifact_value, artifact_description, artifact_tlp, userid, custom_attributes, caseid):
    """Add an artifact. Feature not available in pr10_head."""
    return {'artifact_id': None}


def add_artifact_link(ioc_id, artifact_id):
    """Add artifact link. Feature not available in pr10_head."""
    return True


def check_artifact_type_id(artifact_type_id):
    """Check artifact type ID. Feature not available in pr10_head."""
    return True


def get_artifact_types_list():
    """Get artifact types list. Feature not available in pr10_head."""
    return []


def get_artifact_type_id(type_name):
    """Get artifact type ID. Feature not available in pr10_head."""
    return None


def get_tlps():
    """Get TLPs. Feature not available in pr10_head."""
    return []


def get_tlps_dict():
    """Get TLPs as dict. Feature not available in pr10_head."""
    return {}


def get_case_artifact_comments(artifact_id, caseid):
    """Get artifact comments. Feature not available in pr10_head."""
    return []


def add_comment_to_artifact(artifact_id, caseid, user_id, comment_text):
    """Add comment to artifact. Feature not available in pr10_head."""
    return None


def get_case_artifacts_comments_count(caseid):
    """Get artifact comments count. Feature not available in pr10_head."""
    return 0


def get_case_artifact_comment(comment_id):
    """Get artifact comment. Feature not available in pr10_head."""
    return None


def delete_artifact_comment(comment_id, caseid):
    """Delete artifact comment. Feature not available in pr10_head."""
    return True


def get_artifact_links(artifact_id=None):
    """Get artifact links. Feature not available in pr10_head."""
    return []


def get_detailed_artifacts(caseid, per_page=10, page=1):
    """Get detailed artifacts. Feature not available in pr10_head."""
    return {'artifacts': [], 'totalRows': 0}

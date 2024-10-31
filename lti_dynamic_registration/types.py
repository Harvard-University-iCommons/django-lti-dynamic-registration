import json
from typing import Any, Dict, List, Optional, Sequence

from .constants import CanvasPrivacyLevel, CanvasVisibility


# https://www.imsglobal.org/spec/lti-dr/v1p0#lti-message
class LtiMessage:
    def __init__(
        self,
        type: str,
        icon_uri: Optional[str] = None,
        label: Optional[str] = None,
        placements: Optional[List[str]] = None,
        target_link_uri: Optional[str] = None,
        custom_parameters: Optional[Dict[str, str]] = None,
        roles: Optional[List[str]] = None,
    ):
        self.type = type
        self.icon_uri = icon_uri
        self.label = label
        self.placements = placements
        self.target_link_uri = target_link_uri
        self.custom_parameters = custom_parameters
        self.roles = roles

    def to_dict(self) -> Dict[str, Any]:
        # prune empty values from the dictionary
        return {k: v for k, v in self.__dict__ if v}

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# https://canvas.instructure.com/doc/api/file.registration.html (LTI Message schema section)
class CanvasLtiMessage(LtiMessage):

    def __init__(
        self,
        type: str,
        icon_uri: Optional[str] = None,
        label: Optional[str] = None,
        placements: Optional[List[str]] = None,
        target_link_uri: Optional[str] = None,
        custom_parameters: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        roles: Optional[List[str]] = None,
        display_type: Optional[str] = None,
        default_enabled: Optional[bool] = None,
        visibility: Optional[CanvasVisibility] = None,
    ):
        super().__init__(
            type=type,
            icon_uri=icon_uri,
            label=label,
            placements=placements,
            target_link_uri=target_link_uri,
            custom_parameters=CanvasLtiRegistration.format_custom_params(
                custom_params=custom_parameters, permissions=permissions
            ),
            roles=roles,
        )
        self.display_type = display_type
        self.default_enabled = default_enabled
        self.visibility = visibility

    def to_dict(self) -> Dict[str, Any]:
        new_dict = {
            "type": self.type,
            "icon_uri": self.icon_uri,
            "label": self.label,
            "placements": self.placements,
            "target_link_uri": self.target_link_uri,
            "custom_parameters": self.custom_parameters,
            "roles": self.roles,
            "https://canvas.instructure.com/lti/display_type": self.display_type,
            "https://canvas.instructure.com/lti/course_navigation/default_enabled": self.default_enabled,
            "https://canvas.instructure.com/lti/visibility": self.visibility,
        }

        # prune empty values from the dictionary
        return {k: v for k, v in new_dict.items() if v}

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# https://www.imsglobal.org/spec/lti-dr/v1p0#lti-configuration-0
class LmsLtiToolConfiguration:
    """
    Represents the LTI configuration for a tool in an LMS.
    """

    def __init__(
        self,
        domain: str,
        target_link_uri: str,
        claims: List[str],
        messages: Sequence[LtiMessage],
        custom_parameters: Optional[Dict[str, str]] = None,
        secondary_domains: Optional[List[str]] = None,
        description: Optional[str] = None,
    ):
        self.claims = claims
        self.custom_parameters = custom_parameters
        self.domain = domain
        self.messages = messages
        self.target_link_uri = target_link_uri
        self.secondary_domains = secondary_domains
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        new_dict = {
            "claims": self.claims,
            "custom_parameters": self.custom_parameters,
            "domain": self.domain,
            "messages": [message.to_dict() for message in self.messages],
            "target_link_uri": self.target_link_uri,
            "secondary_domains": self.secondary_domains,
            "description": self.description,
        }

        # prune empty values from the dictionary
        return {k: v for k, v in new_dict.items() if v}


# https://canvas.instructure.com/doc/api/file.registration.html (LTI Configuration schema section)
class CanvasLtiToolConfiguration(LmsLtiToolConfiguration):
    """
    Represents the LTI configuration for a tool in Canvas.
    """

    def __init__(
        self,
        domain: str,
        target_link_uri: str,
        claims: List[str],
        messages: Sequence[CanvasLtiMessage],
        custom_parameters: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        secondary_domains: Optional[List[str]] = None,
        description: Optional[str] = None,
        privacy_level: Optional[CanvasPrivacyLevel] = None,
        tool_id: Optional[str] = None,
    ):
        super().__init__(
            domain=domain,
            target_link_uri=target_link_uri,
            claims=claims,
            messages=messages,
            custom_parameters=CanvasLtiRegistration.format_custom_params(
                custom_params=custom_parameters, permissions=permissions
            ),
            secondary_domains=secondary_domains,
            description=description,
        )
        self.privacy_level = privacy_level
        self.tool_id = tool_id

    def to_dict(self) -> Dict[str, Any]:
        new_dict = {
            "claims": self.claims,
            "custom_parameters": self.custom_parameters,
            "domain": self.domain,
            "messages": [message.to_dict() for message in self.messages],
            "target_link_uri": self.target_link_uri,
            "secondary_domains": self.secondary_domains,
            "description": self.description,
            "https://canvas.instructure.com/lti/privacy_level": self.privacy_level,
            "https://canvas.instructure.com/lti/tool_id": self.tool_id,
        }

        # prune empty values from the dictionary
        return {k: v for k, v in new_dict.items() if v}


# https://www.imsglobal.org/spec/lti-dr/v1p0#openid-configuration-0
class LmsLtiRegistration:
    """
    Represents a tool registration in an LMS.
    """

    def __init__(
        self,
        client_name: str,
        jwks_uri: str,
        initiate_login_uri: str,
        target_link_uri: str,
        scopes: List[str],
        lti_tool_configuration: LmsLtiToolConfiguration,
    ):
        self.application_type = "web"
        self.grant_types = ["client_credentials", "implicit"]
        self.initiate_login_uri = initiate_login_uri
        self.redirect_uris = [target_link_uri]
        self.response_types = ["id_token"]
        self.client_name = client_name
        self.jwks_uri = jwks_uri
        self.token_endpoint_auth_method = "private_key_jwt"
        self.scopes = scopes
        self.lti_tool_configuration = lti_tool_configuration

    def to_dict(self) -> Dict[str, Any]:
        new_dict = {
            "application_type": self.application_type,
            "grant_types": self.grant_types,
            "initiate_login_uri": self.initiate_login_uri,
            "redirect_uris": self.redirect_uris,
            "response_types": self.response_types,
            "client_name": self.client_name,
            "jwks_uri": self.jwks_uri,
            "token_endpoint_auth_method": self.token_endpoint_auth_method,
            "scope": " ".join(self.scopes),
            "https://purl.imsglobal.org/spec/lti-tool-configuration": self.lti_tool_configuration.to_dict(),
        }

        # prune empty values from the dictionary
        return {k: v for k, v in new_dict.items() if v}

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# https://canvas.instructure.com/doc/api/file.registration.html (LTI Registration schema section)
class CanvasLtiRegistration(LmsLtiRegistration):
    """
    Represents a tool registration in Canvas.
    """

    def __init__(
        self,
        client_name: str,
        jwks_uri: str,
        initiate_login_uri: str,
        target_link_uri: str,
        scopes: List[str],
        lti_tool_configuration: CanvasLtiToolConfiguration,
    ):
        super().__init__(
            client_name=client_name,
            jwks_uri=jwks_uri,
            initiate_login_uri=initiate_login_uri,
            target_link_uri=target_link_uri,
            scopes=scopes,
            lti_tool_configuration=lti_tool_configuration,
        )

    @staticmethod
    def format_custom_params(
        custom_params: Optional[List[str]], permissions: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        This function takes a list of custom parameters as provided by the platform and
        converts them into a dictionary that can be used to populate the custom_parameters field.
        The dictionary keys are converted to snake_case and the values are the original custom
        parameter names prefixed with a "$" character.

        Example input:
        [
            "Canvas.user.sisIntegrationId",
            "Canvas.course.sectionIds",
            "Canvas.group.contextIds",
            "Canvas.xapi.url",
            "Caliper.url",
        ]

        Example output:
        {
            "canvas_user_sisintegrationid": "$Canvas.user.sisIntegrationId",
            "canvas_course_sectionids": "$Canvas.course.sectionIds",
            "canvas_group_contextids": "$Canvas.group.contextIds",
            "canvas_xapi_url": "$Canvas.xapi.url",
            "caliper_url": "$Caliper.url",
        }
        """
        if custom_params is None:
            return {}

        custom_params_dict = {}
        for param in custom_params:
            param_name = (
                param.lower().replace(".", "_").replace("<", "").replace(">", "")
            )
            if param == "Canvas.membership.permissions<>":
                # This is a special parameter that requires a list of permissions to be passed in inside the angle brackets
                # Canvas will return a filtered list of the permissions that the user has in the context.
                if permissions:
                    param = f"Canvas.membership.permissions<{','.join(permissions)}>"
                else:
                    # skip the Canvas.membership.permissions<> custom parameter if there are no permissions
                    continue
            param_value = f"${param}"
            custom_params_dict[param_name] = param_value
        return custom_params_dict

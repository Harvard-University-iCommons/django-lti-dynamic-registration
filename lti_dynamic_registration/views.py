import uuid
import requests
from django.http import HttpResponse
from django.views import View
from lti_tool.models import LtiRegistration

from .types import LmsLtiRegistration


class DynamicRegistrationBaseView(View):

    tool_friendly_name: str = "Override this in your subclass"

    def get(self, request, *args, **kwargs):
        # handle get requests here
        raise NotImplementedError(
            "Subclasses of DynamicRegistrationBaseView must implement get"
        )

    def post(self, request, *args, **kwargs):
        # handle post requests here
        raise NotImplementedError(
            "Subclasses of DynamicRegistrationBaseView must implement post"
        )

    def get_openid_config(self) -> dict:
        openid_configuration_url = self.request.GET.get("openid_configuration")
        registration_token = self.request.GET.get("registration_token")

        if not openid_configuration_url or not registration_token:
            raise ValueError(
                "openid_configuration_url and registration_token are required (this view must be accessed from within a dynamic registration flow)"
            )

        headers = {"Authorization": f"Bearer {registration_token}"}
        response = requests.get(openid_configuration_url, headers=headers)
        response.raise_for_status()
        openid_config = response.json()

        # make sure that the openid_configuration_url starts with the issuer from the openid_config
        if not openid_configuration_url.startswith(openid_config["issuer"]):
            raise ValueError(
                "invalid openid_configuration_url: does not match the issuer in the openid config"
            )
        return openid_config

    def register_tool_in_platform(
        self,
        openid_config: dict,
        tool_platform_registration: LmsLtiRegistration,
    ) -> str:

        registration_token = self.request.GET.get("registration_token")

        response = requests.post(
            openid_config["registration_endpoint"],
            json=tool_platform_registration.to_dict(),
            headers={
                "Authorization": f"Bearer {registration_token}",
                "Content-Type": "application/json",
            },
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Status:", e.response.status_code)
            print("Reason:", e.response.reason)
            print("Body:", e.response.text)
            raise

        response_data = response.json()
        client_id = response_data["client_id"]
        return client_id

    def register_platform_in_tool(
        self, consumer_name: str, openid_config: dict
    ) -> LtiRegistration:
        temp_client_id = f"temporary-{uuid.uuid4()}"
        
        reg = LtiRegistration(
            name=consumer_name,
            issuer=openid_config["issuer"],
            auth_url=openid_config["authorization_endpoint"],
            token_url=openid_config["token_endpoint"],
            keyset_url=openid_config["jwks_uri"],
            client_id=temp_client_id,
        )
        reg.save()
        return reg

    def success_response(self) -> HttpResponse:
        return HttpResponse(
            """
            <html>
            <head>
                <title>Dynamic Registration Successful</title>
            </head>
            <body>
                <script>
                    window.parent.postMessage({subject: 'org.imsglobal.lti.close'}, '*');
                </script>
            </body>
            </html>
            """
        )

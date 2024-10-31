# django-lti-dynamic-registration

Add-on to django-lti to support dynamic registration.

See: https://www.imsglobal.org/spec/lti-dr/v1p0

More details to come.

## Using

```python
from lti_dynamic_registration.views import DynamicRegistrationBaseView
from lti_dynamic_registration.types import (
    CanvasLtiMessage,
    CanvasLtiRegistration,
    CanvasLtiToolConfiguration,
)
from django.shortcuts import redirect, render


class DynamicRegistrationView(DynamicRegistrationBaseView):
    tool_friendly_name = "Tool Name"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # Return a form to the user where they can customize the registration
        return render(request, 'registration.html')


    def post(self, request, *args, **kwargs) -> HttpResponse:
        # Perform the registration steps. Typically this would involve:
        # 1. Register the platform in the tool
        # 2. Register the tool in the platform
        # 3. Update the platform registration with the client ID returned in step 2


        # Return a page containing javascript that calls a special
        # platform postMessage endpoint
        return self.success_response()
```

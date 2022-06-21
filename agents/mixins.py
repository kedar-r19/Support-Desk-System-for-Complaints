from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OwnerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an owner"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_owner:
            return redirect("/complaints")
        return super().dispatch(request, *args, **kwargs)

class CustomerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an owner"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_customer:
            return redirect("/complaints")
        return super().dispatch(request, *args, **kwargs)

class AgentAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an owner"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_agent:
            return redirect("/complaints")
        return super().dispatch(request, *args, **kwargs)


class OwnerCustomerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an owner or customer"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_owner and not request.user.is_customer:
            return redirect("/complaints")
        return super().dispatch(request, *args, **kwargs)

class OwnerAgentAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an owner or customer"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_owner and not request.user.is_agent:
            return redirect("/complaints")
        return super().dispatch(request, *args, **kwargs)
from typing import Iterable, Mapping, Tuple

from django.http import Http404

from sentry.models import (
    Identity,
    IdentityProvider,
    IdentityStatus,
    Integration,
    Organization,
    User,
)
from sentry.types.integrations import EXTERNAL_PROVIDERS, ExternalProviders


def get_identity_or_404(
    provider: ExternalProviders, user: User, organization_id: int, integration_id: int
) -> Tuple[Organization, Integration, IdentityProvider]:
    """For endpoints, short-circuit with a 404 if we cannot find everything we need."""
    try:
        organization = Organization.objects.get(id__in=user.get_orgs(), id=organization_id)
        integration = Integration.objects.get(id=integration_id, organizations=organization)
        idp = IdentityProvider.objects.get(
            external_id=integration.external_id, type=EXTERNAL_PROVIDERS[provider]
        )
    except Exception:
        raise Http404
    return organization, integration, idp


def get_identities_by_user(idp: IdentityProvider, users: Iterable[User]) -> Mapping[User, Identity]:
    identity_models = Identity.objects.filter(
        idp=idp,
        user__in=users,
        status=IdentityStatus.VALID,
    )
    return {identity.user: identity for identity in identity_models}

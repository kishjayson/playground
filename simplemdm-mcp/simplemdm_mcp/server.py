from __future__ import annotations

from typing import Any

from mcp.server import MCPServer

from .client import SimpleMDMClient

mcp = MCPServer("SimpleMDM")


def _page_params(limit: int, starting_after: int, direction: str) -> dict[str, Any]:
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    if direction not in {"asc", "desc"}:
        raise ValueError("direction must be 'asc' or 'desc'")
    return {"limit": limit, "starting_after": starting_after, "direction": direction}


async def _get(path: str, *, redact_device_secrets: bool = False, **params: Any) -> dict[str, Any]:
    async with SimpleMDMClient() as client:
        return await client.get(path, redact_device_secrets=redact_device_secrets, **params)


async def _get_content(path: str, **params: Any) -> dict[str, str]:
    async with SimpleMDMClient() as client:
        return await client.get_content(path, **params)


@mcp.tool()
async def get_account() -> dict[str, Any]:
    """Get the SimpleMDM account record and subscription information exposed by the API."""
    return await _get("/account")


@mcp.tool()
async def get_devices(
    search: str = "",
    include_awaiting_enrollment: bool = False,
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List devices without secret custom attributes or recovery/password values."""
    params = _page_params(limit, starting_after, direction)
    params.update(
        search=search,
        include_awaiting_enrollment=str(include_awaiting_enrollment).lower(),
        include_secret_custom_attributes="false",
    )
    return await _get("/devices", redact_device_secrets=True, **params)


@mcp.tool()
async def get_device(device_id: int) -> dict[str, Any]:
    """Get one device without secret custom attributes or recovery/password values."""
    return await _get(
        f"/devices/{device_id}",
        redact_device_secrets=True,
        include_secret_custom_attributes="false",
    )


@mcp.tool()
async def get_device_profiles(
    device_id: int,
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List profiles directly assigned to a device. Group-assigned profiles are not included by this endpoint."""
    return await _get(f"/devices/{device_id}/profiles", **_page_params(limit, starting_after, direction))


@mcp.tool()
async def get_device_installed_apps(
    device_id: int,
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List applications SimpleMDM reports as installed on one device."""
    return await _get(f"/devices/{device_id}/installed_apps", **_page_params(limit, starting_after, direction))


@mcp.tool()
async def get_assignment_groups(
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List assignment groups and their app, group, device, and profile relationships."""
    return await _get("/assignment_groups", **_page_params(limit, starting_after, direction))


@mcp.tool()
async def get_assignment_group(assignment_group_id: int) -> dict[str, Any]:
    """Get one assignment group by numeric ID."""
    return await _get(f"/assignment_groups/{assignment_group_id}")


@mcp.tool()
async def get_apps(
    include_shared: bool = False,
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List apps in the SimpleMDM app catalog."""
    params = _page_params(limit, starting_after, direction)
    params["include_shared"] = str(include_shared).lower()
    return await _get("/apps", **params)


@mcp.tool()
async def get_app_installs(
    app_id: int,
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List devices on which a catalog app is installed."""
    return await _get(f"/apps/{app_id}/installs", **_page_params(limit, starting_after, direction))


@mcp.tool()
async def get_profiles(
    search: str = "",
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List profiles in the account. Search matches profile name or type."""
    params = _page_params(limit, starting_after, direction)
    params["search"] = search
    return await _get("/profiles", **params)


@mcp.tool()
async def get_profile(profile_id: int) -> dict[str, Any]:
    """Get one profile by numeric ID."""
    return await _get(f"/profiles/{profile_id}")


@mcp.tool()
async def get_custom_configuration_profiles(
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List custom configuration profiles."""
    return await _get("/custom_configuration_profiles", **_page_params(limit, starting_after, direction))


@mcp.tool()
async def get_custom_configuration_profile_content(profile_id: int) -> dict[str, str]:
    """Download one custom configuration profile. The returned payload may contain managed secrets."""
    return await _get_content(f"/custom_configuration_profiles/{profile_id}/download")


@mcp.tool()
async def get_custom_declarations(
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List custom Declarative Device Management declarations."""
    return await _get("/custom_declarations", **_page_params(limit, starting_after, direction))


@mcp.tool()
async def get_custom_declaration_content(profile_id: int) -> dict[str, str]:
    """Download one custom declaration payload. The returned payload may contain managed secrets."""
    return await _get_content(f"/custom_declarations/{profile_id}/download")


@mcp.tool()
async def get_scripts(
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List scripts in the account. SimpleMDM includes script content in this endpoint."""
    return await _get("/scripts", **_page_params(limit, starting_after, direction))


@mcp.tool()
async def get_script(script_id: int) -> dict[str, Any]:
    """Get one SimpleMDM script, including its content, by numeric ID."""
    return await _get(f"/scripts/{script_id}")


@mcp.tool()
async def get_enrollments(
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List manual and account-driven enrollments. Automated Enrollment records are exposed through DEP servers."""
    return await _get("/enrollments", **_page_params(limit, starting_after, direction))


@mcp.tool()
async def get_dep_servers(
    limit: int = 100,
    starting_after: int = 0,
    direction: str = "asc",
) -> dict[str, Any]:
    """List Apple Business/School Manager Automated Device Enrollment server associations."""
    return await _get("/dep_servers", **_page_params(limit, starting_after, direction))


@mcp.tool()
async def get_push_certificate() -> dict[str, Any]:
    """Get metadata for the Apple Push Notification certificate used by the account."""
    return await _get("/push_certificate")


if __name__ == "__main__":
    mcp.run()

from __future__ import annotations

from typing import Any

from .client import SimpleMDMClient


def _bool(value: bool) -> str:
    return str(value).lower()


def _clean(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


async def _post(
    path: str,
    *,
    data: dict[str, Any] | None = None,
    files: dict[str, tuple[str, str, str]] | None = None,
) -> dict[str, Any]:
    async with SimpleMDMClient() as client:
        return await client.post(path, data=data, files=files)


async def _patch(
    path: str,
    *,
    data: dict[str, Any] | None = None,
    files: dict[str, tuple[str, str, str]] | None = None,
) -> dict[str, Any]:
    async with SimpleMDMClient() as client:
        return await client.patch(path, data=data, files=files)


async def _delete(path: str) -> dict[str, Any]:
    async with SimpleMDMClient() as client:
        return await client.delete(path)


def register_write_tools(mcp: Any) -> None:
    @mcp.tool()
    async def create_custom_configuration_profile(
        name: str,
        mobileconfig: str,
        user_scope: bool = False,
        attribute_support: bool = False,
        escape_attributes: bool = False,
        reinstall_after_os_update: bool = False,
        declarative: bool = False,
        auto_renew_scep_based_certificates: bool = False,
        minimum_macos_version: str = "",
        maximum_macos_version: str = "",
        allowed_macos_architecture: str = "any",
    ) -> dict[str, Any]:
        """Create a SimpleMDM custom configuration profile from mobileconfig XML."""
        data = _clean(
            {
                "name": name,
                "user_scope": _bool(user_scope),
                "attribute_support": _bool(attribute_support),
                "escape_attributes": _bool(escape_attributes),
                "reinstall_after_os_update": _bool(reinstall_after_os_update),
                "declarative": _bool(declarative),
                "auto_renew_scep_based_certificates": _bool(auto_renew_scep_based_certificates),
                "minimum_macos_version": minimum_macos_version or None,
                "maximum_macos_version": maximum_macos_version or None,
                "allowed_macos_architecture": allowed_macos_architecture,
            }
        )
        files = {"mobileconfig": ("profile.mobileconfig", mobileconfig, "application/x-apple-aspen-config")}
        return await _post("/custom_configuration_profiles", data=data, files=files)

    @mcp.tool()
    async def update_custom_configuration_profile(
        profile_id: int,
        name: str = "",
        mobileconfig: str = "",
        user_scope: bool | None = None,
        attribute_support: bool | None = None,
        escape_attributes: bool | None = None,
        reinstall_after_os_update: bool | None = None,
        declarative: bool | None = None,
        auto_renew_scep_based_certificates: bool | None = None,
        minimum_macos_version: str = "",
        maximum_macos_version: str = "",
        allowed_macos_architecture: str = "",
    ) -> dict[str, Any]:
        """Update a SimpleMDM custom configuration profile. Empty string fields are left unchanged."""
        data = _clean(
            {
                "name": name or None,
                "user_scope": _bool(user_scope) if user_scope is not None else None,
                "attribute_support": _bool(attribute_support) if attribute_support is not None else None,
                "escape_attributes": _bool(escape_attributes) if escape_attributes is not None else None,
                "reinstall_after_os_update": _bool(reinstall_after_os_update) if reinstall_after_os_update is not None else None,
                "declarative": _bool(declarative) if declarative is not None else None,
                "auto_renew_scep_based_certificates": _bool(auto_renew_scep_based_certificates) if auto_renew_scep_based_certificates is not None else None,
                "minimum_macos_version": minimum_macos_version or None,
                "maximum_macos_version": maximum_macos_version or None,
                "allowed_macos_architecture": allowed_macos_architecture or None,
            }
        )
        files = None
        if mobileconfig:
            files = {"mobileconfig": ("profile.mobileconfig", mobileconfig, "application/x-apple-aspen-config")}
        return await _patch(f"/custom_configuration_profiles/{profile_id}", data=data, files=files)

    @mcp.tool()
    async def delete_custom_configuration_profile(profile_id: int) -> dict[str, Any]:
        """Delete a custom configuration profile from SimpleMDM."""
        return await _delete(f"/custom_configuration_profiles/{profile_id}")

    @mcp.tool()
    async def assign_custom_configuration_profile_to_device(profile_id: int, device_id: int) -> dict[str, Any]:
        """Assign a custom configuration profile directly to one device."""
        return await _post(f"/custom_configuration_profiles/{profile_id}/devices/{device_id}")

    @mcp.tool()
    async def unassign_custom_configuration_profile_from_device(profile_id: int, device_id: int) -> dict[str, Any]:
        """Remove a directly assigned custom configuration profile from one device."""
        return await _delete(f"/custom_configuration_profiles/{profile_id}/devices/{device_id}")

    @mcp.tool()
    async def create_custom_declaration(
        name: str,
        declaration_type: str,
        payload: str,
        user_scope: bool = True,
        attribute_support: bool = False,
        escape_attributes: bool = False,
        activation_predicate: str = "",
    ) -> dict[str, Any]:
        """Create a SimpleMDM custom Declarative Device Management declaration from JSON."""
        data = _clean(
            {
                "name": name,
                "declaration_type": declaration_type,
                "user_scope": _bool(user_scope),
                "attribute_support": _bool(attribute_support),
                "escape_attributes": _bool(escape_attributes),
                "activation_predicate": activation_predicate or None,
            }
        )
        files = {"payload": ("declaration.json", payload, "application/json")}
        return await _post("/custom_declarations", data=data, files=files)

    @mcp.tool()
    async def update_custom_declaration(
        profile_id: int,
        name: str = "",
        declaration_type: str = "",
        payload: str = "",
        user_scope: bool | None = None,
        attribute_support: bool | None = None,
        escape_attributes: bool | None = None,
        activation_predicate: str = "",
    ) -> dict[str, Any]:
        """Update a custom DDM declaration. Empty string fields are left unchanged."""
        data = _clean(
            {
                "name": name or None,
                "declaration_type": declaration_type or None,
                "user_scope": _bool(user_scope) if user_scope is not None else None,
                "attribute_support": _bool(attribute_support) if attribute_support is not None else None,
                "escape_attributes": _bool(escape_attributes) if escape_attributes is not None else None,
                "activation_predicate": activation_predicate or None,
            }
        )
        files = None
        if payload:
            files = {"payload": ("declaration.json", payload, "application/json")}
        return await _patch(f"/custom_declarations/{profile_id}", data=data, files=files)

    @mcp.tool()
    async def delete_custom_declaration(profile_id: int) -> dict[str, Any]:
        """Delete a custom DDM declaration from SimpleMDM."""
        return await _delete(f"/custom_declarations/{profile_id}")

    @mcp.tool()
    async def assign_custom_declaration_to_device(profile_id: int, device_id: int) -> dict[str, Any]:
        """Assign a custom DDM declaration directly to one device."""
        return await _post(f"/custom_declarations/{profile_id}/devices/{device_id}")

    @mcp.tool()
    async def unassign_custom_declaration_from_device(profile_id: int, device_id: int) -> dict[str, Any]:
        """Remove a directly assigned custom DDM declaration from one device."""
        return await _delete(f"/custom_declarations/{profile_id}/devices/{device_id}")

    @mcp.tool()
    async def assign_profile_to_assignment_group(assignment_group_id: int, profile_id: int) -> dict[str, Any]:
        """Assign an existing profile to an assignment group. Call sync_assignment_group_profiles afterward to deploy it."""
        return await _post(f"/assignment_groups/{assignment_group_id}/profiles/{profile_id}")

    @mcp.tool()
    async def unassign_profile_from_assignment_group(assignment_group_id: int, profile_id: int) -> dict[str, Any]:
        """Unassign a profile from an assignment group. Call sync_assignment_group_profiles afterward to remove it."""
        return await _delete(f"/assignment_groups/{assignment_group_id}/profiles/{profile_id}")

    @mcp.tool()
    async def sync_assignment_group_profiles(assignment_group_id: int) -> dict[str, Any]:
        """Sync profile changes for an assignment group. SimpleMDM rate-limits this endpoint to once every 30 seconds."""
        return await _post(f"/assignment_groups/{assignment_group_id}/sync_profiles")

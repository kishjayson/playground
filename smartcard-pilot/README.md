# Smart Card Pilot

This is a deliberately staged macOS smart-card test.

The first profile proves delivery and pairing behavior without making the smart card mandatory for authentication.

## Stage 1 — pair and observe

`smartcard-pilot.mobileconfig` configures the native `com.apple.security.smartcard` payload with:

```text
allowSmartCard          true
UserPairing             true
oneCardPerUser          false
tokenRemovalAction      1
checkCertificateTrust   0
enforceSmartCard        false
```

This keeps password authentication available while allowing a smart card to be paired and tested. After pairing, removing the token should start the screen saver.

For login use, the token needs a PIV authentication identity. A key-management identity is also important so macOS can wrap the login keychain without repeatedly prompting for the account password.

## Stage 2 — enforce

Do not enable `enforceSmartCard` until the target account has been paired and smart-card login has been verified.

At that point, change only the controls that are actually being tested. In particular, certificate trust checking and mandatory smart-card authentication should be introduced deliberately rather than bundled into the initial delivery test.

## Recovery

macOS provides a recoveryOS path for temporarily skipping smart-card enforcement if a card is lost or unavailable. Preserve a known-good recovery path before enabling enforcement.

## Scope

Keep the pilot directly assigned to the test Mac rather than adding it to the shared macOS assignment group. Apple permits only one Smart Card payload on a device, so verify that no other `com.apple.security.smartcard` payload is already installed before assignment.

Secure cookies
==============

The client uses cookies to track account logins and active survey sessions.
Both uses are security sensitive, which means the cookies should be
authenticated before they can be trusted.

To do this we a simple signing system for both cookies. An account gets
a new `secret` property which contains random data. This will be used
to create a signature for cookie values. On each login a new secret
is generated to prevent replay attacks.

The cookie value is be a base64 encoded string containing the signature
and data separated by a single space. The signature is a MD5 hash
of the secret and the data.


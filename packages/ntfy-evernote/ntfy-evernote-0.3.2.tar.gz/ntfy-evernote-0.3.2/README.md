# ntfy-evernote

Evernote backend for ntfy.

## Usage

``` yaml
ntfy_evernote:
    access_token: ...
    china: false
```

*If you don't provide the access token, a login guide will auto start.*

Required parameters:

- `access_token` - string, the access token grant from evernote.

Optional parameters:

- `notebook` - string, name of the notebook to push message.
- `sandbox` - bool.
- `china` - bool, is in china.

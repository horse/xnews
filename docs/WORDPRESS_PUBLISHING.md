# XNEWS Japanese WordPress Publishing

The Japanese Markdown files in `content/ja/2026-08-01/` are the publishing source. The edition manifest at `wordpress/ja/2026-08-01/wordpress.yml` is authoritative for WordPress publication settings.

For this edition:

- publication time: `2026-08-01 06:00:00` Japan Standard Time;
- WordPress status: `publish`;
- comments: closed;
- pingbacks and trackbacks: closed;
- author: the authenticated WordPress user, unless `WP_AUTHOR_ID` is set;
- existing posts with the same slug are updated rather than duplicated.

## Install

```bash
python -m pip install -r requirements-wordpress.txt
```

## Validate without publishing

```bash
python tools/wordpress_publish.py wordpress/ja/2026-08-01/wordpress.yml
```

The command validates the manifest, required Markdown fields, file presence and duplicate slugs. It prints the publication plan without contacting WordPress.

## Local publish

Set credentials only in environment variables. Never commit an application password.

```bash
export WP_SITE_URL='https://example.jp'
export WP_USERNAME='wordpress-user'
export WP_APPLICATION_PASSWORD='xxxx xxxx xxxx xxxx xxxx xxxx'

python tools/wordpress_publish.py \
  wordpress/ja/2026-08-01/wordpress.yml \
  --publish
```

Optional explicit author mapping:

```bash
export WP_AUTHOR_ID='12'
```

## GitHub Actions publish

For remote publication, add these repository secrets under **Settings → Secrets and variables → Actions**:

- `WP_SITE_URL`
- `WP_USERNAME`
- `WP_APPLICATION_PASSWORD`
- `WP_AUTHOR_ID` only when an explicit numeric author ID is required

The workflow `.github/workflows/publish-wordpress-ja.yml` runs only when manually dispatched or when the `wordpress-publish` branch is pushed. Do not create or update that branch until the secrets are configured.

The publisher creates missing categories and tags, converts Markdown to HTML, publishes or updates posts by slug, and rewrites links in the daily index from local `.md` paths to the WordPress post URLs returned by the API.

## Required WordPress settings

- WordPress REST API must be reachable at `/wp-json/wp/v2/`.
- Application Passwords must be enabled.
- The authenticated account must be allowed to publish posts and create categories and tags.
- HTTPS is strongly recommended.

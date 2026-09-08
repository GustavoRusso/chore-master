# Google OAuth setup for local development

Each developer creates their own OAuth 2.0 Web client (or uses a shared team **dev** client from a password manager). Do **not** commit secrets. This guide is for local Sign-In setup, not for graph/agent process work.

There is no local bypass: Google Sign-In needs a real client ID and secret.

Google renamed the old **OAuth consent screen** to **Google Auth Platform**. If you see “Google Auth Platform not configured yet”, that is normal — click **Get started**.

## 1. Open Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in with the Google account you will use for local Sign-In.
3. Create a project (or select an existing one). Example name: `chore-master-local`.
4. Confirm the project is selected in the top bar.

## 2. Configure Google Auth Platform

Do this in order. **Branding must be complete before Audience or Clients will work.**

### 2a. Get started (if prompted)

1. Open **APIs & Services** → **Google Auth Platform** (or **OAuth consent screen** — both may open the same place).
2. If you see **Google Auth Platform not configured yet**, click **Get started**.
3. Walk through the wizard if it appears (app name, audience **External**, contact email, accept policy → **Create**).

### 2b. Finish Branding (required)

If Audience shows *“OAuth configuration is incomplete… visit the Branding page”*, open **Google Auth Platform** → **Branding** and fill every required field (marked with `*`):

| Field | What to enter (local/dev) |
|-------|---------------------------|
| App name | Example: `Chore Master local` |
| User support email | Your Google account email |
| App logo | Optional — leave empty |
| App domain / authorized domains | Optional — leave empty for local/dev |
| Developer contact information | Your email |

Click **Save**. Stay on Branding until the incomplete-configuration warning is gone.

### 2c. Audience and test users

1. Open **Audience**.
2. Confirm user type **External** (use **Internal** only if your Google Workspace org requires it).
3. If status is **Testing**, under **Test users** click **Add users**, enter the Google account(s) that will sign in locally, and **Save**.

You do not need extra scopes for basic Sign-In with Google (profile/email).

## 3. Create an OAuth 2.0 Web client

1. In **Google Auth Platform**, open **Clients** (or **APIs & Services** → **Credentials**).
2. Click **Create client** / **Create credentials** → **OAuth client ID**.
3. Application type: **Web application**.
4. Name it (example: `Chore Master local`).
5. Under **Authorized redirect URIs**, add **both** of these (exact match, including the trailing slash):

```text
http://127.0.0.1:8000/accounts/google/login/callback/
http://localhost:8000/accounts/google/login/callback/
```

Google treats `127.0.0.1` and `localhost` as different hosts. Prefer opening the app at http://127.0.0.1:8000/ after setup.

6. Create / save the client. Copy the **Client ID** and **Client secret**.

If you already created the client, open it, add any missing URI, and **Save**. Changes can take a minute to apply.

## 4. Put values in `.env`

From the project root (if you do not have `.env` yet):

```bash
cp .env.example .env
```

Edit `.env`:

```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

Never commit `.env`.

If you edited `.env` on Windows, save it with **LF** line endings (not CRLF). CRLF makes bash keep a hidden `\r` on the client ID and Google returns **invalid_client**.

## 5. Load env and run

```bash
set -a && source .env && set +a
uv run python manage.py runserver 0.0.0.0:8000
```

Open http://127.0.0.1:8000/ and use **Sign in with Google**.

## Team option

A team may share one **non-production** OAuth client (same ID/secret) via a password manager. Each developer still puts those values in a local gitignored `.env`. Do not put them in the repo.

## Common problems

| Symptom | Check |
|---------|--------|
| “Google Auth Platform not configured yet” | Click **Get started** and finish the wizard (section 2a). |
| “OAuth configuration is incomplete… visit Branding” | Open **Branding**, fill required fields, **Save** (section 2b). Then return to **Audience**. |
| Access blocked: **invalid_client** / “OAuth client was not found” | Usually a bad Client ID/secret, or Windows `CRLF` in `.env` (hidden `\r`). Re-copy only the ID/secret from Console into `.env` (do not `cp .env.example .env` again after filling values). Run `sed -i 's/\r$//' .env`, then stop `runserver`, re-`source`, and start again. The app also strips `\r` from these env vars at load time. |
| Access blocked: **redirect_uri_mismatch** | In Console → **Clients** → your Web client, **Authorized redirect URIs** must include the URI the app sent. Add both `http://127.0.0.1:8000/accounts/google/login/callback/` and `http://localhost:8000/accounts/google/login/callback/`, then **Save**. Open the app with the same host you registered (prefer `127.0.0.1`). |
| Access blocked / app not verified | App is in Testing; add your Google account as a **Test user** under **Audience**. |
| Empty or wrong credentials | `.env` loaded in this shell (`set -a && source .env && set +a`) before `runserver`. |
| Sign-In works on one machine only | Each machine needs `.env` filled; OAuth values are not in git. |

Product auth lock (Google only for MVP): [`plan.md`](plan.md). Short setup pointer: [`../README.md`](../README.md).

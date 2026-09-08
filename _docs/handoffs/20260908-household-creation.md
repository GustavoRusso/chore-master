# Handoff: 20260908-household-creation

Blank template for live runs. Filled sample (not a live handoff): [`_example.md`](_example.md).

## Status

- **Status:** `ready_for_human`
- **Review cycles:** 0
- **Backlog:** #3
- **Needs human review:** no
- **Pending question:**

## Goal

A signed-in family member with no household can create one (name + generated invite code), become a member, and see the household home. They are always themselves.

## Acceptance criteria

- [ ] A logged-in user with **no** household sees create-household (including a name field) and does **not** see a household member list
- [ ] Creating a household with a name adds the creator as a member, generates an invite code, and opens the household home
- [ ] The household home shows the household name, the invite code, and every member (each as themselves — no “switch person”)
- [ ] After create, the user does **not** stay on the empty signed-in home from #2
- [ ] Submitting create with an empty name does not create a household and shows a visible error; they still have no household
- [ ] A user who **already** belongs to a household sees that household home and is not offered create as the main path
- [ ] A user who already belongs cannot create a second household (they stay in the original household)
- [ ] An anonymous visitor cannot open create or the household home; they are sent to login
- [ ] Automated tests cover create, empty-name failure, already-a-member (no second household), and login-required redirect (in-app only)

## Out of scope

- Accept invitation / join with invite code — backlog #4
- Assign chores — backlog #5
- Inbox actions, week board, complete + points, scoreboard, playful polish — backlog #6–#10
- Leave household, remove a member, rename a household, or regenerate the invite code
- More than one household per user; household owner/admin roles
- Sending the invite code by email (MVP has no email invites per [`plan.md`](../plan.md))
- Changing Google Sign-In from #2
- Automated tests of live email or other external systems — see [`software-engineer.md`](../team/software-engineer.md) **Mandatory test depth**

## Constraints

- Depends on #2 (Google session auth and the login-required home). Stay inside the existing Django project under `src/`; add a small `households` app (or equivalent) for models/views/templates/urls
- Replace the empty signed-in home from #2 with this task’s create gate and household home (do not leave a separate dead “you are signed in” page as the post-login landing)
- Models: `Household` (name + unique invite code) and membership (user belongs to at most one household). The app generates the invite code; the family does not invent it
- Do **not** implement join / accept invitation in this task — that is #4
- Honor [`plan.md`](../plan.md): one shared household; no “switch person”; simple invite code; no username/password path
- Server-rendered Django templates and form posts are enough (HTMX is for later inbox / mark-done work)
- Tests: Django test client for in-app create/membership behavior only; no browser e2e; honor [`software-engineer.md`](../team/software-engineer.md) **Mandatory test depth** (no live external systems; no mocks of systems this project does not own)

## Evidence

Implemented create-household and household home in a new `households` app. Replaced the empty signed-in home with a gate: no household goes to create; a member goes to household home. Join with invite code is not in this work.

### Tests

```text
$ uv run python manage.py test
Creating test database for alias 'default'...
............
----------------------------------------------------------------------
Ran 12 tests in 1.460s

OK
Destroying test database for alias 'default'...
Found 12 test(s).
System check identified no issues (0 silenced).
```

### Migrate check

```text
$ uv run python manage.py migrate --check
# exit 0 (no pending migrations)

$ uv run python manage.py showmigrations
account
 [X] 0001_initial
 [X] 0002_email_max_length
 [X] 0003_alter_emailaddress_create_unique_verified_email
 [X] 0004_alter_emailaddress_drop_unique_email
 [X] 0005_emailaddress_idx_upper_email
 [X] 0006_emailaddress_lower
 [X] 0007_emailaddress_idx_email
 [X] 0008_emailaddress_unique_primary_email_fixup
 [X] 0009_emailaddress_unique_primary_email
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
 [X] 0012_alter_user_first_name_max_length
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
households
 [X] 0001_initial
sessions
 [X] 0001_initial
socialaccount
 [X] 0001_initial
 [X] 0002_token_max_lengths
 [X] 0003_extra_data_default_dict
 [X] 0004_app_provider_id_settings
 [X] 0005_socialtoken_nullable_app
 [X] 0006_alter_socialaccount_extra_data
```

## Review

## QA: PASS

- [x] A logged-in user with **no** household sees create-household (including a name field) and does **not** see a household member list - PASS
- [x] Creating a household with a name adds the creator as a member, generates an invite code, and opens the household home - PASS
- [x] The household home shows the household name, the invite code, and every member (each as themselves — no “switch person”) - PASS
- [x] After create, the user does **not** stay on the empty signed-in home from #2 - PASS
- [x] Submitting create with an empty name does not create a household and shows a visible error; they still have no household - PASS
- [x] A user who **already** belongs to a household sees that household home and is not offered create as the main path - PASS
- [x] A user who already belongs cannot create a second household (they stay in the original household) - PASS
- [x] An anonymous visitor cannot open create or the household home; they are sent to login - PASS
- [x] Automated tests cover create, empty-name failure, already-a-member (no second household), and login-required redirect (in-app only) - PASS

Tests: `uv run python manage.py test`, 12 passed, 0 failed

Migrate check: `uv run python manage.py migrate --check`, ok (`households` 0001_initial applied; no pending migrations)

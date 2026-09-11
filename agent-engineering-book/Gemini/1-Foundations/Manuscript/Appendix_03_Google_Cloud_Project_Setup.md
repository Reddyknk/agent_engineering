# Appendix 03: Getting a Google Cloud Project

## TL;DR

This book runs Gemini through a Google Cloud project. There is no API-key path.
You need a project, with billing enabled, before you build your first agent in
Chapter 5. In the live course, you create it in Class 1.

**Pick your route:**

| Your situation | Route | Time | Cost to you |
| --- | --- | --- | --- |
| Default — you have a card or UPI | **Free trial** (§A3.3) | 15 minutes | $0 ($300 credit, 90 days) |
| Your employer already uses Google Cloud | **Existing project** (§A3.2.2) | 1 email | $0 |
| You're in an instructor-led cohort | **Lab project** (§A3.2.3) | 0 minutes | $0 |
| You're an enrolled student | **Education credits** (§A3.2.4) | Days to weeks | $0 |
| Cards fail where you are | **Reseller** (§A3.2.5) | Days | Varies |

**The four commands that matter,** once you have a project:

```bash
export PROJECT_ID=your-project-id
gcloud config set project "$PROJECT_ID"
gcloud auth login
gcloud auth application-default login
gcloud auth application-default set-quota-project "$PROJECT_ID"
```

**The one mistake everyone makes:** stopping after `gcloud auth login`. That
credentials the `gcloud` command. The *agent* uses Application Default
Credentials, written by the third command. Skip it and the book's labs fail in
ways that look like quota errors — or worse, succeed against the wrong project.
See §A3.5.

**Prove it worked:**

```bash
gcloud auth application-default print-access-token >/dev/null && echo OK
```

---

## A3.1 Why a project, and not an API key

Google offers two ways to call Gemini: an API key from AI Studio, and a Google
Cloud project through Vertex AI — renamed the **Gemini Enterprise Agent
Platform** in 2026, though the service and its environment variables did not
change.

An API key is faster to obtain, and this book does not use it. Chapters 12–14
and the appendices before this one are about *observing* and *deploying*
agents: traces in Cloud Trace, sessions and evaluation in the Agent Platform
console, deployment to Agent Engine. None of that exists without a project. Supporting both paths would
mean two sets of instructions and two sets of failures, so the book supports one.

A missing project is an error to fix, not a condition to route around.

---

## A3.2 Five routes to a project

### A3.2.1 The free trial

The default, and the right choice for most readers. Google gives new customers
**$300 in credit, valid for 90 days**. A payment method is required at sign-up
for identity verification; it is not charged, and billing only begins if you
deliberately upgrade to a paid account.

Full walkthrough in §A3.3.

The real constraint is the 90-day clock, not the money. Working the book at one
class a week, you will spend a rounding error of the $300 — but you can run out
of *days*. If you expect to take longer, start the trial when you reach Class 1,
not when you buy the book.

### A3.2.2 An existing organization project

If you work somewhere that already uses Google Cloud, this is the fastest and
cheapest route: no sign-up, no payment method, no trial clock.

Ask whoever administers it for:

- a project you can use, and its **project ID** (not its display name);
- billing already enabled on it;
- these roles on that project for your account:
  - `roles/aiplatform.user` — to call Gemini,
  - `roles/cloudtrace.agent` — to write traces,
  - `roles/cloudtrace.user` — to read them in the console;
- the four APIs in §A3.3.6 enabled, or permission to enable them yourself.

Do not ask for Owner or Editor. You do not need them, and a reader who requests
broad access to run a training exercise is demonstrating exactly the habit
Chapter 6 argues against.

### A3.2.3 An instructor-provisioned lab project

If you are working through this book as part of an instructor-led cohort, ask
before you pay for anything. Instructors can provision temporary projects
through Google Cloud Skills Boost, each arriving with its own account, its own
project, and no payment method at all.

Two things to know. The account is not your Google account — it is a temporary
one issued with the lab, and you must be signed in as *that* account for
`gcloud` to see the project. And the project is destroyed when the lab session
ends. Anything you want to keep — a deployed agent, a trace history, an
evaluation run — needs a project of your own.

### A3.2.4 Education credits

Students enrolled at eligible degree-granting institutions can apply for Google
Cloud education credits, which redeem into a billing account and remove the
payment-method requirement.

One distinction worth getting right, because the names collide. **Google Skills
credits** — including the monthly allowance that comes with the Innovators
program — pay for *hands-on labs on Google's learning platform*. They are not
credit on your own project and will not run this book's code. What you want is
an **education grant**, which credits a Cloud Billing account.

Both involve an application and verification, so this route takes days to weeks.
Start it early or start the free trial and switch later.

### A3.2.5 Through a reseller

In some regions, sign-up cards are declined for reasons that have nothing to do
with the card — see §A3.4. Google's own billing guidance in that situation is to
work with a local reseller, who bills you through whatever payment rails
actually function where you are. Slower and rarely free, but it is the
documented answer when the self-serve path simply does not work.

---

## A3.3 The free trial, step by step

### A3.3.1 Sign up

Go to `cloud.google.com/free`, sign in with a Google account, and start the free
trial. You will be asked for your name, address, and a payment method.

### A3.3.2 Choose a payment method

See §A3.4 for the full table. The short version: a **debit card** works — you do
not need a credit card — and from India, **UPI** works. Prepaid and virtual
cards do not work anywhere.

### A3.3.3 Create a project

```bash
gcloud projects create widgetware-sdr-$RANDOM --name="WidgetWare SDR"
```

Or in the console: **project picker → New Project**.

Write down the **project ID**. It is not the project name, it is globally
unique, and it is the value every chapter needs. To list what you already have:

```bash
gcloud projects list
```

### A3.3.4 Confirm billing is enabled

A trial account has billing enabled by default. If you are reusing an older
project, check: **Cloud Console → Billing → Link a billing account**. Vertex AI
refuses to serve a project with no billing account attached, and the error does
not say so plainly.

### A3.3.5 Install and authenticate gcloud

Install the Google Cloud CLI per Google's instructions for your platform, then
run all four commands from the TL;DR. Run them again any time you switch
projects.

### A3.3.6 Enable the APIs

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  cloudtrace.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  --project="$PROJECT_ID"
```

In a managed classroom project this may fail with `UREQ_TOS_NOT_ACCEPTED`,
because a student account cannot accept the Cloud terms of service. That is
harmless *if the services are already enabled*. Confirm:

```bash
gcloud services list --enabled --project="$PROJECT_ID" \
  | grep -E 'aiplatform|cloudtrace|logging|monitoring'
```

### A3.3.7 Configure .env

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
MODEL=gemini-2.5-flash
```

`GOOGLE_CLOUD_LOCATION` must be a real region. `global` is not one. It is
accepted at configuration time and fails much later, at deployment, which makes
it one of the more expensive typos in the book.

Never commit `.env`.

### A3.3.8 Verify

```bash
gcloud config get-value project
gcloud auth application-default print-access-token >/dev/null && echo "ADC: OK"
```

The first must print your project ID. The second must print `OK`.

---

## A3.4 Payment methods

| Method | Where | Notes |
| --- | --- | --- |
| **Credit card** | Everywhere | Visa, Mastercard, American Express. Discover in the US; JCB in Japan and the US. |
| **Debit card** | Everywhere | Needs a Visa or Mastercard logo. Most readers who think they are blocked are not — a debit card is enough. |
| **UPI** | India | See below. |
| **Bank account** (direct debit / ACH) | US, UK, parts of Europe | Verification takes 5–10 business days. Cannot serve as a backup method. |
| **PayPal** | Spain, Italy, Mexico | |
| **Pix / Boleto** | Brazil | Pix is manual payment in BRL; Boleto is backup-only. |

**Rejected everywhere:** prepaid cards, virtual or disposable card numbers, and
debit cards that require two-factor authentication on every transaction. A
reader without a credit card reaches for a virtual card first; it will not work,
and the decline message will not explain why.

**India.** UPI works and is usually the easiest route. Expect ₹500–₹1000 to be
debited or held during verification — an identity check or a prepaid balance,
not a fee, and not the $300 credit. It can take several days to reverse. Note
that Google's billing documentation describes UPI for INR-denominated billing
accounts rather than for trial sign-up specifically; if it does not appear as an
option, use a card.

Indian cards carry their own complication. RBI rules require an e-mandate for
recurring charges, and banks decline automatic card payments above the mandate
limit — Google documents ₹15,000. Many Indian debit cards also demand an OTP per
transaction, which places them in the rejected row above. A card declined at
sign-up or at first billing is usually hitting one of these rules, not a problem
with your account. Switch to UPI or make manual payments rather than retrying.

---

## A3.5 The mistake everyone makes

`gcloud auth login` and `gcloud auth application-default login` are different
credentials with confusingly similar names.

| Command | Writes | Used by |
| --- | --- | --- |
| `gcloud auth login` | the gcloud CLI's own credential | the `gcloud` command |
| `gcloud auth application-default login` | Application Default Credentials | **your agent, and the trace exporter** |

Running only the first is the single most common setup failure in this book. It
is dangerous because it is silent: `gcloud` commands work, so the environment
*looks* configured. Then model calls fail with permission errors that read like
quota problems — or, worse, they succeed, and every trace lands in whichever
project ADC still points at.

Switching projects makes this sharper. ADC records a **quota project** inside
its credential file, and changing `.env` does not update it. After any project
change, run all four commands from the TL;DR.

To see what ADC currently believes:

```bash
cat "${CLOUDSDK_CONFIG:-$HOME/.config/gcloud}/application_default_credentials.json" \
  | python3 -c 'import json,sys; print(json.load(sys.stdin).get("quota_project_id"))'
```

If that does not match `GOOGLE_CLOUD_PROJECT` in your `.env`, nothing else you
debug today is the real problem.

---

## A3.6 Keeping the bill at zero

The trial is credit, not a deposit. When the $300 is spent or 90 days pass, the
billing account closes automatically and you are not charged. Charges begin only
if you deliberately upgrade.

The book's own consumption is small: every chapter calls `gemini-2.5-flash`, a
handful of times per exercise. The realistic risk is not the model — it is
leaving something else running, an idle deployed Agent Engine instance being the
usual culprit.

Two habits worth forming:

1. **Set a budget alert** — Cloud Console → Billing → Budgets & alerts — with a
   threshold well under $300. It costs nothing and converts a surprise into an
   email.
2. **Delete deployed agents when a chapter ends.** Chapter 17 covers deployment;
   what it deploys keeps existing until you remove it.

Current pricing is at `cloud.google.com/vertex-ai/pricing`. Trust that page over
any figure printed in a book, including this one.

---

## A3.7 When something fails

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `403` calling the model | ADC points at another project, or the account lacks `aiplatform.user` | §A3.5, then check IAM |
| Traces never appear in Cloud Trace | ADC quota project is stale | §A3.5 |
| Traces appear in the *wrong* project | Same — and this one looks like success | §A3.5 |
| `UREQ_TOS_NOT_ACCEPTED` enabling APIs | Student account cannot accept the Cloud ToS | Harmless if already enabled — §A3.3.6 |
| Card declined at sign-up | Prepaid or virtual card, or per-transaction 2FA | §A3.4 |
| `OR_BACR2_44`, India | RBI e-mandate limits on recurring charges | UPI or manual payment — §A3.4 |
| Deployment rejects the region | `GOOGLE_CLOUD_LOCATION=global` | Use `us-central1` — §A3.3.7 |
| `gcloud` cannot see the project | Signed in as the wrong account (common with lab projects) | `gcloud auth list`, then `gcloud config set account` |

---

## A3.8 Checklist

Before Chapter 5—Class 2 of the live course—all eight of these are true:

- [ ] A Google Cloud project exists, and you know its **project ID**
- [ ] Billing is enabled on it
- [ ] `gcloud` is installed, and `gcloud config get-value project` prints that ID
- [ ] `gcloud config get-value account` prints the account that owns the project
- [ ] `gcloud auth application-default print-access-token` succeeds
- [ ] ADC's quota project matches the project in `.env`
- [ ] All four APIs are enabled
- [ ] `.env` has the four canonical keys, with a real region

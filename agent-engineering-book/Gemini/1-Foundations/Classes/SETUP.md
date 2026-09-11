# Course Setup (Self-Paced Track)

Do this once, before Class 1. Class 1 builds both the WidgetWare charter *and*
the runnable repository harness in one sitting — so Antigravity, Git, Python,
and a Google Cloud project need to already exist before Class 1 starts, not be
learned as part of it. This file is that one-time step, done ahead of time
precisely so Class 1's own exercise isn't also an installation tutorial.

This file is for the **self-paced track**. If you're attending the live,
instructor-led program, start with `00_Course_Framework.md` instead — though the
Google Cloud section below still applies to you.

The conventions every class assumes are stated in `CONVENTIONS.md`. The short
version: one model path (Google Cloud), one shell (bash), one region
(`us-central1`).

For the long version of the Google Cloud part — every route to a project, the
full payment-method table, and a troubleshooting index — see
[`Appendix 03`](../Manuscript/Appendix_03_Google_Cloud_Project_Setup.md).

## Install

1. **Antigravity** — install and authenticate per Google's current instructions
   for your platform.
2. **Git** — any recent version.
3. **Python 3.11+** — confirm with `python3 --version`.
4. **Google Cloud CLI (`gcloud`)** — see "Google Cloud" below.

### A note on shells

Every command in this course is written for **bash**, and every script carries a
bash shebang and is run directly. macOS ships zsh as the login shell; that is
fine and you do not need to change it. Scripts run under bash regardless of what
your prompt is.

## Get the companion repository

```bash
git clone https://github.com/sensei-ji/agent_engineering.git
cd agent_engineering/agent-engineering-book/Gemini/1-Foundations
```

Every class folder referenced from here forward (`class-01/`, `class-02/`, and
so on) is a subdirectory of `Classes/` inside this clone.

## Google Cloud

This course runs Gemini through a Google Cloud project, using Vertex AI — which
Google renamed the **Gemini Enterprise Agent Platform** in 2026. The service and
the environment variables did not change; only the name in the console did.

This is the only supported path. Classes 02C and 02D teach observability,
tracing, and deployment, and none of that exists without a real project.

### 1. Sign up

If you already have a Google Cloud account with billing enabled, skip to step 2.

1. Go to `cloud.google.com/free` and sign in with a Google account.
2. Start the **Google Cloud Free Trial**: $300 in credit, valid for 90 days.
3. Provide a payment method when asked.

**About that payment method.** The trial is genuinely free — the $300 is credit,
not a deposit, and Google does not charge your payment method when the trial
ends or the credit runs out. Billing only starts if you deliberately upgrade to
a paid account. You may see a small pending authorization during verification;
an authorization is not a charge.

But a payment method *is* required at sign-up, and there is no way around that.
What counts as one depends on where you are:

| Method | Where | Notes |
| --- | --- | --- |
| **Credit card** | Everywhere | Visa, Mastercard, American Express. Discover in the US, JCB in Japan and the US. |
| **Debit card** | Everywhere | Must carry a Visa or Mastercard logo. This is the option most students overlook — you do not need a *credit* card. |
| **UPI** | India | See below. |
| **Bank account (direct debit / ACH)** | US, UK, parts of Europe | Verification takes 5–10 business days, so start well before Class 1. Cannot be used as a backup method. |
| **PayPal** | Spain, Italy, Mexico only | |
| **Pix / Boleto** | Brazil | Pix is manual payments in BRL; Boleto is a backup method only. |

**Not accepted anywhere:** prepaid cards, virtual or disposable card numbers,
and debit cards that require two-factor authentication on every transaction.
Students try prepaid and virtual cards first and lose an evening to it. Don't.

**Paying from India.** Two things make India its own case.

UPI works and is the easiest route for students without an international card.
Expect a small amount — typically ₹500–₹1000 — to be debited or held during
verification. It is an identity check or a prepaid balance on your billing
account, not a course fee, and it is not the $300 credit. It can take several
days to reverse or to appear as balance, so don't panic on day one. Note that
Google's billing documentation scopes UPI to INR-denominated billing accounts
rather than to trial sign-up specifically; if it doesn't appear as an option for
you, use a card.

Indian cards are the complication. RBI rules require an e-mandate for recurring
charges, and banks decline automatic card payments above the mandate limit
(Google documents ₹15,000). Many Indian debit cards also demand an OTP on every
transaction, which puts them in the "not accepted" row above. If a card is
declined during sign-up or later billing, that is usually why — switch to UPI or
make manual payments rather than retrying the same card.

**If you are attending an instructor-led cohort,** ask before paying for
anything. Instructors can provision temporary lab projects through Google Cloud
Skills Boost / Qwiklabs, which come with their own account, their own project,
and no payment method at all. The trade-off is that those projects expire when
the lab session ends, so anything you want to keep — a deployed agent, a trace
history — needs your own project.

If you can provide none of the above, you cannot complete this course as
written. Say so early rather than partway through Class 3.

### 2. Create a project

```bash
gcloud projects create widgetware-sdr-$RANDOM --name="WidgetWare SDR"
```

Or use the console: **Cloud Console → project picker → New Project**.

Whichever you use, **write down the project ID**. It is not the project *name*,
and it is the value every class needs. If you already have a project you would
rather use:

```bash
gcloud projects list
```

Then make sure billing is enabled on it: **Cloud Console → Billing → Link a
billing account**.

### 3. Install and authenticate gcloud

Install the Google Cloud CLI per Google's instructions for your platform, then:

```bash
export PROJECT_ID=your-project-id

gcloud config set project "$PROJECT_ID"
gcloud auth login
gcloud auth application-default login
gcloud auth application-default set-quota-project "$PROJECT_ID"
```

**Those last two lines are not optional, and they are not the same as the one
above them.** `gcloud auth login` credentials the `gcloud` command.
`gcloud auth application-default login` writes Application Default Credentials,
and ADC is what the agent and the trace exporter actually use. Skipping it is
the single most common setup failure in this course — and it fails quietly,
often by succeeding against the wrong project.

Run all four again any time you switch projects.

### 4. Enable the APIs

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  cloudtrace.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  --project="$PROJECT_ID"
```

### 5. Configure the project's .env

Each class's package carries a `.env.example`. Copy it and fill in your project:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
MODEL=gemini-2.5-flash
```

`GOOGLE_CLOUD_LOCATION` must be a real region. `global` is not one, and it fails
much later than it should — at deployment, not at configuration.

Never commit `.env`. It is listed in `.gitignore` for a reason.

## Verify

```bash
git --version
python3 --version
gcloud --version

gcloud config get-value project
gcloud auth application-default print-access-token >/dev/null \
  && echo "Application Default Credentials: OK"
```

All five should print something, and the last must print `OK`. Confirm
Antigravity separately per its own installation instructions — there is no
single offline command that verifies it end to end.

## On cost

Vertex AI is pay-as-you-go per token, billed against your $300 trial credit.
This course spends a negligible fraction of it: each class makes at most a
handful of live model calls, all on `gemini-2.5-flash`. The binding constraint
is the trial's 90-day clock, not the credit.

Check current rates at `cloud.google.com/vertex-ai/pricing` rather than trusting
a number printed here, since pricing changes.

To be certain you are never surprised, set a budget alert: **Cloud Console →
Billing → Budgets & alerts**, and set a threshold well below $300.

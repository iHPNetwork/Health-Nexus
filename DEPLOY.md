# Deploy Guide — Get the website live (≈15 minutes)

You are **not** creating a new webpage. It already exists in this repo (`landing/` and `intake/`).
Deploying just points a free host (Netlify) at these files and connects your domain (Namecheap).
Do this once. After that, any change you push to GitHub re-deploys automatically.

**Order of operations:** (0) merge to main → (1) Netlify → (2) form emails → (3) Namecheap domain → (4) test.

---

## Step 0 — Merge the work into `main` (1 min)
Netlify will deploy your `main` branch, so get the finished code there first.
- Go to **https://github.com/iHPNetwork/Health-Nexus/pull/1** and click **Merge pull request → Confirm merge**.
- (Or just ask me to merge it.)

---

## Step 1 — Put the site on Netlify (5 min)
1. Go to **https://app.netlify.com** and **Sign up** — choose **"Sign up with GitHub"** (simplest; it links your repo).
2. Click **Add new site → Import an existing project → Deploy with GitHub**.
3. Authorize Netlify, then pick the **`iHPNetwork/Health-Nexus`** repository.
4. Deploy settings (most are pre-filled from `netlify.toml`):
   - **Branch to deploy:** `main`
   - **Build command:** leave **empty** (it's a static site)
   - **Publish directory:** `.` (a single dot)
5. Click **Deploy**. In ~30 seconds you get a live URL like `https://gentle-otter-12345.netlify.app`.
6. Test it:
   - `your-site.netlify.app/` → the landing page
   - `your-site.netlify.app/intake` → the five-number form
   - `your-site.netlify.app/sample` → the sample Blueprint

> You can rename the random Netlify subdomain under **Site configuration → Change site name**
> (e.g. `campbell3.netlify.app`) if you want a tidy link before your real domain is ready.

---

## Step 2 — Turn on the form emails (3 min)  ← this is the important one
This is what makes the five numbers land in your inbox automatically.
1. In your Netlify site: **Forms** (left sidebar). After the first deploy you should see a form
   named **`practice-intake`** detected automatically.
2. Go to **Forms → Form notifications → Add notification → Email notification.**
3. Set **"Email to notify"** to **denise4183@gmail.com** and save.
4. That's it. Every submission now emails you all the fields — including a ready-to-paste
   `pipeline_json` block you drop straight into `pipeline/inputs_<practice>.json`.

> If `practice-intake` doesn't appear under Forms, trigger one more deploy (Netlify →
> **Deploys → Trigger deploy → Deploy site**) and submit the form once; detection happens at deploy time.

---

## Step 3 — Connect your Namecheap domain (5 min + waiting)
1. Buy your domain at **https://www.namecheap.com** (e.g. `campbell3.com`, ~$12/yr).
2. In **Netlify → Domain management → Add a custom domain →** type `campbell3.com` → **Verify → Add**.
3. Netlify will offer the easiest path: **"Use Netlify DNS."** Choose it. Netlify shows you
   **four nameservers** that look like `dns1.p03.nsone.net`, `dns2.p03.nsone.net`, etc. Copy them.
4. In **Namecheap → Domain List → Manage** (next to your domain) **→ Nameservers →** switch the
   dropdown to **Custom DNS** and paste Netlify's four nameservers. **Save** (the green check).
5. Wait for DNS to propagate — usually 15–60 minutes, sometimes a few hours. Netlify
   **automatically issues free HTTPS** (the padlock) once it resolves.

> Prefer to keep DNS at Namecheap instead of moving nameservers? You can — in Namecheap's
> **Advanced DNS**, add an **A record** `@ → 75.2.60.5` and a **CNAME** `www → your-site.netlify.app`.
> Moving the nameservers (step 3–4) is simpler and lets Netlify manage HTTPS for you.

---

## Step 4 — Test the whole loop (2 min)
1. Visit **https://campbell3.com** → landing page loads with the padlock.
2. Click **Enter your five numbers** → fill the form with test values → **Submit**.
3. Check **denise4183@gmail.com** — the submission should arrive within a minute.
4. Open the email, copy the `pipeline_json`, save it as `pipeline/inputs_test.json`, and run:
   ```
   cd pipeline && python3 generate.py inputs_test.json
   ```
   You should get a gate-PASS and a PDF in `samples/`. That confirms the full pipeline end to end.

---

## After it's live — your repeatable client loop
1. Practice fills the form → you get the email.
2. Paste the `pipeline_json` into `pipeline/inputs_<practice>.json`.
3. `cd pipeline && python3 generate.py inputs_<practice>.json` → review the draft (your ~1-week window).
4. Email the finished PDF with a short cover note → book the 30-minute working session.

That's the business. The website is just the front door; the pipeline on your computer is the engine.

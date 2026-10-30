# MoveYourWayIA.org: website package

Snapshot of the MoveYourWayIA prototype site, packaged on October 29, 2026.
Prepared for Community Connections for Public Health (CCPH), Iowa State University.

## What's in this folder

| File | What it is |
|---|---|
| `index.html` | The whole website. All text, styling, the tracker map and its code are in this one file. Badge and logo images are built into it, so it works on its own. |
| `CNAME` | Tells GitHub Pages to serve the site at `moveyourwayia.org`. Other hosts ignore it. |
| `_redirects` | Short links for Cloudflare Pages or Netlify, for example `moveyourwayia.org/tracker`. GitHub Pages ignores it. |
| `assets/badges/` | The four badge concept images (Iowa and ISU, Champion and Ambassador). |
| `assets/logos/ccph-logo.png` | The CCPH logo. |
| `README.md` | These instructions. |

The `assets` folder holds the original image files for reference. The site does not need it, because the same images are already built into `index.html`.

## Pages and their links

The site is one page with four menu tabs plus About the Campaign. Each section has its own link:

| Section | Link after launch | Short link (Cloudflare Pages or Netlify) |
|---|---|---|
| Home | `moveyourwayia.org` | |
| Tracker Map | `moveyourwayia.org/#tracker` | `moveyourwayia.org/tracker` |
| Getting Started | `moveyourwayia.org/#getting-started` | `moveyourwayia.org/get-started` |
| Badge Up | `moveyourwayia.org/#badge-up` | `moveyourwayia.org/badges` |
| About the Campaign | `moveyourwayia.org/#about` | `moveyourwayia.org/about` |

Use the Tracker Map link in emails, flyers and QR codes.

## Preview it on your computer

Unzip the folder and double-click `index.html`. It opens in your web browser. Everything works except the custom fonts, which load from Google Fonts when you're online.

---

## Going live: step by step

### Step 1. Check with ISU (before buying anything)

- Ask ISU IT whether a website outside `iastate.edu` needs approval.
- Ask University Marketing how the ISU and CCPH names and logos may be used on it.
- The required Move Your Way® trademark line is already in the site footer.

### Step 2. Register the domain

1. Search for `moveyourwayia.org` at a registrar: Cloudflare Registrar, Namecheap or Porkbun. A .org usually costs about $10–20 a year.
2. Register it under a **shared CCPH account and email**, not a personal one, so the domain stays with the program.
3. Turn on **auto-renew** and **WHOIS privacy**.
4. Optional: also register `moveyourwayiowa.org` and forward it to the main site.

Tip: if you register at Cloudflare and host on Cloudflare Pages (Option A below), Cloudflare sets up the DNS for you.

### Step 3. Choose a host and upload the site

Pick one option. Both are free and include HTTPS.

**Option A: Cloudflare Pages (recommended; simplest)**

1. Create a free Cloudflare account with the shared CCPH email.
2. Go to **Workers & Pages → Create → Pages → Upload assets**.
3. Name the project (for example `moveyourwayia`) and drag the unzipped `moveyourwayia-site` folder in. Click **Deploy**.
4. You'll get a test address like `moveyourwayia.pages.dev`. Check it on a phone and a computer.

**Option B: GitHub Pages (good if students will edit through GitHub)**

1. Create a GitHub account or organization for the program (for example `moveyourwayia`).
2. Create a public repository and upload everything in the `moveyourwayia-site` folder.
3. Go to **Settings → Pages**. Under Source, choose **Deploy from a branch**, pick `main` and `/ (root)`, and save.
4. In about a minute it appears at `https://<account>.github.io/<repository>/`.

### Step 4. Connect the domain (DNS)

**If you used Cloudflare Pages:**

1. Open the Pages project, then **Custom domains → Set up a custom domain**.
2. Enter `moveyourwayia.org`, then add `www.moveyourwayia.org` too.
3. If the domain is registered at Cloudflare, it creates the records automatically. If it's registered elsewhere, Cloudflare shows the exact record to add at your registrar.

**If you used GitHub Pages:**

1. In **Settings → Pages → Custom domain**, enter `moveyourwayia.org` and save. The `CNAME` file in this folder already contains it.
2. At your registrar's DNS settings, add these records:

| Type | Name / Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `<account>.github.io` |

3. Delete any old A or CNAME records for `@` or `www` that the registrar added by default (parking pages).

DNS changes usually take a few minutes, and can take up to 24–48 hours.

### Step 5. Turn on HTTPS and test

1. **GitHub Pages:** tick **Enforce HTTPS** in Settings → Pages once it becomes available. **Cloudflare Pages:** HTTPS is automatic.
2. Test `https://moveyourwayia.org` and `https://www.moveyourwayia.org`.
3. Test every tab and the `#tracker` link on a phone, and click each GivePulse button.

---

## Before going public: open items

- [ ] **Map data.** The tracker shows **sample numbers**, and a yellow notice on the page says so. Real counts depend on the GivePulse pledge form and export (see the County Form Build Handbook's questions for GivePulse).
- [ ] **Badge artwork.** The badge images are AI concept mockups. Replace them with final artwork that uses the authorized Move Your Way logo.
- [ ] **Enroll buttons.** "Enroll Your Campus" goes to the MoveYourWayISU GivePulse page. "Enroll Your Organization" goes to the Move Your Way Iowa GivePulse page. Swap in dedicated sign-up or resource pages if you create them.
- [ ] **ISU approvals** from Step 1.

## Making common edits

Open `index.html` in a text editor. VS Code is free and works well. Use Find (Ctrl+F or Cmd+F):

- **Change any wording:** search for the current text and type over it.
- **Change a link:** search for the old address (for example `givepulse.com/group/2031736`) and replace it everywhere.
- **Update tracker numbers:** search for `const D=`. Each county is listed as `"County":[individuals, organizations, population, new this cycle]`. Add or edit counties in that list. A county that isn't listed shows as "not yet reporting."
- After editing, upload the new `index.html` again (Cloudflare: **Create new deployment**; GitHub: upload the file to the repository).

**Later improvement:** when GivePulse exports are set up, the county numbers can move into a separate `counts.csv` that the map reads, so updating the map just means replacing one file. The tracker can also become its own page at `moveyourwayia.org/tracker`.

## Contacts

Community Connections for Public Health, Iowa State University: https://ccph.iastate.edu

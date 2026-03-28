# Mission: Math Blast — MVP Business Plan
*Prepared by Leo | March 2026*

---

## The Idea in One Line
A weekly illustrated adventure story emailed to kids (ages 6–12) where they solve curriculum-aligned maths puzzles to advance the plot — delivered as an interactive webpage, no app required.

---

## 1. The Product

### Core Format (already built ✅)
- Weekly "issue" = 1 adventure story + 3 maths puzzles
- Delivered as a link to an interactive HTML page (hosted, mobile-friendly)
- PDF version included for printing/offline use
- Answers revealed after each attempt — educational, not just right/wrong

### Age Tiers
| Tier | Age | Curriculum Focus |
|------|-----|-----------------|
| Explorer | 6–7 (Year 1–2) | Counting, basic addition, shapes |
| Adventurer | 7–9 (Year 2–4) | Times tables, fractions, time |
| Commander | 9–12 (Year 4–6) | Long division, decimals, area/perimeter |

Start with **Adventurer only** (already built). Add tiers as you grow.

### Content Pipeline (weekly, per issue)
1. Write story + 3 puzzles (~1 hour, or AI-assisted)
2. Generate 4 images via DALL-E (~5 min, automated)
3. Build HTML file from template (~automated)
4. Send via email platform

**Realistic time per issue once systems are built: 2–3 hours**

---

## 2. The Market

### Who's buying
- **Primary:** Parents of primary school kids (ages 6–12)
- **Secondary:** Grandparents buying for grandkids, teachers buying class licenses

### Size (Australia alone)
- ~2 million primary school kids in Australia
- Even 0.1% = 2,000 subscribers = $10,000–$20,000/month

### Why they'll pay
- Tutoring costs $40–$80/hour — this is a fraction of that
- Screen time guilt is real — parents *want* educational digital content
- No app to install, no account for the kid, just works

### Competitors
| Product | Price | Weakness |
|---------|-------|----------|
| Mathletics | ~$15/mo | Boring, feels like homework |
| Prodigy | Free/$10/mo | Game-first, maths feels secondary |
| Khan Academy | Free | No narrative, very dry |
| **Math Blast** | $8/mo | **Story-driven, delightful, no app** |

**The gap:** Nobody is doing *story-first* maths in this format. That's the moat.

---

## 3. Revenue Model

### Pricing
- **Monthly:** $8/month per child
- **Annual:** $69/year per child (save ~28%, ~$5.75/mo)
- **Family plan:** $12/month for up to 3 kids

### Revenue Targets
| Subscribers | Monthly Revenue | Annual Revenue |
|-------------|----------------|---------------|
| 100 | $800 | $9,600 |
| 500 | $4,000 | $48,000 |
| 1,000 | $8,000 | $96,000 |
| 5,000 | $40,000 | $480,000 |

### Cost Structure (lean)
- Hosting: ~$20/month (simple static hosting or Netlify)
- Email platform: ~$30/month (up to 5k subscribers on ConvertKit/Mailchimp)
- Image generation: ~$0.10/image × 4 = ~$0.40/issue
- Payment: Stripe (2.9% + 30c per transaction)
- Total fixed costs to start: **under $100/month**

---

## 4. MVP Build — What's Needed

### Phase 1: Validate (Weeks 1–2) — FREE
**Goal:** Get 10 paying subscribers before building anything more.

- [ ] Set up a simple landing page (can be a Carrd or Notion page)
- [ ] Create a 2-week free trial offer
- [ ] Share with 3 parent Facebook groups / school communities
- [ ] Manually email the HTML file to early subscribers
- [ ] Ask for $8 via bank transfer or PayPal — don't even automate it yet

**Success metric:** 10 people pay $8 before you spend a dollar on tech.

---

### Phase 2: Automate Delivery (Weeks 3–6)
**Goal:** Stop doing things manually.

- [ ] Set up ConvertKit or Beehiiv for email list + weekly sends
- [ ] Build issue template so each week is fill-in-the-blank
- [ ] Automate image generation (I can script this)
- [ ] Host each issue on Netlify (free tier, custom URL per issue)
- [ ] Set up Stripe payment link + webhook to add subscriber to email list

**Stack:**
- Landing page: Carrd ($19/year) or Webflow
- Email: Beehiiv (free to start) or ConvertKit
- Payments: Stripe
- Hosting: Netlify (free)
- Content: AI-assisted + Leo automation

---

### Phase 3: Growth (Month 2+)
**Goal:** Hit 100 paying subscribers.

- [ ] Launch referral program ("Share with a friend, get a free month")
- [ ] Facebook/Instagram ads targeting parents of primary school kids
- [ ] Reach out to 10 primary schools for bulk/class licenses
- [ ] Add second age tier (Explorer — ages 6–7)
- [ ] Build a simple "issue archive" so subscribers can access past issues

---

## 5. Landing Page — What It Needs

**Above the fold:**
- Hook: *"Your kid's favourite screen time — that actually teaches them maths"*
- One GIF/screenshot of the interactive story
- CTA: "Start 2-Week Free Trial — $8/month after"

**Below the fold:**
- How it works (3 steps: subscribe → get weekly email → read + solve)
- Sample issue (link to a free preview)
- Testimonials (get these from your colleague's son + Max!)
- FAQ (What age? What curriculum? Can I cancel?)

---

## 6. Content Roadmap — First 8 Weeks

| Week | Story | Maths Topics |
|------|-------|-------------|
| 1 | Jake on Planet Zog ✅ | Times tables, fractions, telling time |
| 2 | Jake discovers a robot factory | Multiplication, halves & quarters, patterns |
| 3 | Space pirates steal the fuel | Division, thirds, elapsed time |
| 4 | Jake races to the Moon | 2× and 5× tables, fractions of shapes, am/pm |
| 5 | The alien bake-off | 3× and 4× tables, equal sharing, half past |
| 6 | Jake builds a rocket car | 6× and 7× tables, mixed fractions, 24hr time |
| 7 | Mission to the ice planet | 8× and 9× tables, fraction of a number, calendars |
| 8 | Jake comes home — THE FINALE | Mixed review — all topics |

---

## 7. Branding

**Name options:**
- Mission: Math Blast *(current — strong)*
- The Weekly Quest
- Math Adventures
- Blast Off Maths

**Recommendation:** Stick with **Mission: Math Blast** — it's memorable, action-oriented, appeals to boys and girls.

**Visual identity:** Already established — space theme, purple/magenta/yellow, illustrated cartoon characters.

---

## 8. The Ask — What's Needed to Start

**From Art & Beth:**
- Decision: Is this worth 4 weeks of evenings to validate?
- ~$50 to set up Carrd landing page + Stripe
- 2 hours to share in parent groups and school communities

**From Leo:**
- Build the automated content pipeline
- Generate issues 2–8
- Set up the tech stack once you get 10 paying subscribers

---

## 9. 90-Day Success Milestones

| Milestone | Target Date | What It Proves |
|-----------|-------------|----------------|
| 10 paying subscribers | Week 2 | People will pay |
| Landing page live | Week 3 | Professional presence |
| Automated delivery | Week 4 | Scalable |
| 50 subscribers | Month 2 | Word of mouth works |
| 100 subscribers | Month 3 | Real business |
| First school license | Month 3 | B2B opportunity |

---

## Bottom Line

This is a **low-risk, low-cost** business to validate. The product is built. The content pipeline exists. The only question is whether parents will pay — and the fastest way to answer that is to ask 10 of them this week.

**Worst case:** 10 people try it, nobody pays → you've lost nothing but a few hours.
**Best case:** 10 people pay → you have a real signal and a roadmap to $10k/month.

*Let's find out. 🚀*

# Lawyer Review Checklist

Draft legal pages are in `website/legal/`. **Have qualified counsel review before monetization launch.**

## Entity and contact

- [ ] Replace `[Add legal entity name and registered address before launch]` in Privacy Policy
- [ ] Replace `[Specify governing law and venue before launch]` in Terms of Service
- [ ] Replace `[Add DMCA agent name and postal address before US launch if required]` in DMCA Policy
- [ ] Confirm contact emails (`privacy@`, `legal@`, `support@`) are provisioned and monitored

## Payment and commerce

- [ ] Refund language matches Stripe/PayPal (or chosen processor) merchant agreement
- [ ] Services Terms align with actual quote/SOW and invoicing workflow
- [ ] Checkout flow links Terms + Refund before payment; acceptance logged if possible

## Liability and infrastructure

- [ ] Liability cap appropriate for beta infrastructure tooling and paid support
- [ ] Beta disclaimer consistent across site, Terms, Disclaimer, and Services Terms
- [ ] AGPL vs paid support separation is clear to customers

## Privacy and GDPR

- [ ] Subprocessor list complete (hosting, email, payments, analytics, forum)
- [ ] DPA template ready if premium support accesses EU customer VPS data
- [ ] Cookie banner behavior matches actual scripts loaded (analytics/affiliate)
- [ ] Newsletter consent and Privacy Policy checkbox meet GDPR/ePrivacy requirements

## Affiliate and comparisons

- [ ] Affiliate disclosure meets FTC “clear and conspicuous” standard on mobile
- [ ] Inline banner used on all comparison pages with affiliate CTAs
- [ ] Comparison Methodology matches actual editorial process

## Forum and UGC

- [ ] Community Guidelines linked from forum.wpfy.org
- [ ] DMCA process matches forum host requirements (if applicable)

## Files to review

| Page | Path |
|------|------|
| Privacy Policy | `legal/privacy/index.html` |
| Cookie Policy | `legal/cookies/index.html` |
| Terms of Service | `legal/terms/index.html` |
| Affiliate Disclosure | `legal/affiliate-disclosure/index.html` |
| Disclaimer | `legal/disclaimer/index.html` |
| Services Terms | `legal/services-terms/index.html` |
| Refund Policy | `legal/refund/index.html` |
| Comparison Methodology | `legal/comparison-methodology/index.html` |
| Community Guidelines | `legal/community/index.html` |
| DMCA Policy | `legal/dmca/index.html` |

Regenerate pages after content edits: `python3 website/generate_legal_pages.py`

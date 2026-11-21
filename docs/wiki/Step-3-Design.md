# Step 3: Design

🌐 **English** · [Dansk](Step-3-Design-da) · [Bahasa Melayu](Step-3-Design-ms)

Milestone `MIL-003`. Branch and pull request: one for this step.

![Use case UC-001](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/03-design-use-case.png)

## What was done

One use case, UC-001 "Scrape wellness foods to a CSV", with its alternative flows (a page the site disallows, a page without values, a failed request). Two ADRs record the standard-library client and the wellness thresholds. The domain model, the system sequence diagram, the operation contract, the sequence diagram and the design class diagram show how the layers fit.

## What was gained

- The alternative flows found the hard cases before the code did: what to do when `robots.txt` says no, or a page has no nutrient table.
- A port (`FoodSource`) between the use case and the web client lets the use case be tested with a fake and without the network.
- Writing down the thresholds as a decision (ADR) makes clear that "wellness friendly" is a simple study rule, not dietary advice.

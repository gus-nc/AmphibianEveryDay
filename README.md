# The Amphibians Every Day Bot 🐸

A Python-based bot that posts a unique amphibian species every day, sourced from the comprehensive AmphibiaWeb dataset. Each post includes the species' scientific name, common name (if available), IUCN status, and a picture from the AmphibiaWeb profile.

#### A Bluesky account

This bot is located at [@amphibianeveryday.bsky.social]([https://bsky.app/](https://bsky.app/profile/amphibianeveryday.bsky.social)).

#### Schedule

The schedule is controlled by the GitHub Actions workflow in [./.github/workflows/post.yml](./.github/workflows/post.yml). The [schedule trigger](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) uses cron syntax to schedule when the workflow runs and your bot posts. [Crontab Guru](https://crontab.guru/) is a good way to visualise it.

New Species every day at 18 PST.

# The Amphibians Every Day Bot 🐸

A Python-based bot that posts a unique amphibian species every day, sourced from the comprehensive AmphibiaWeb dataset. Each post includes the species' scientific name, common name (if available), IUCN status, and a picture from the AmphibiaWeb profile. The bot uses Python for scripting and posts to a Bluesky account.

#### A Bluesky account

This bot is located at [@amphibianeveryday.bsky.social](https://bsky.app/profile/amphibianeveryday.bsky.social). This is a passion project by 
[@atelopus.bsky.social](https://bsky.app/profile/atelopus.bsky.social). I’m not affiliated with [@amphibiaweb.bsky.social](https://bsky.app/profile/amphibiaweb.bsky.social), but I’m a huge fan of their work! 🐸✨

#### Schedule (not ready yet!)

The schedule is controlled by the GitHub Actions workflow in [./.github/workflows/post.yml](./.github/workflows/post.yml). The [schedule trigger](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) uses cron syntax to schedule when the workflow runs and your bot posts. [Crontab Guru](https://crontab.guru/) is a good way to visualise it.

New Species every day at 18 PST.


# Repository Structure

The repository is organized as follows:

```
AmphibianEveryDay/
├── .github/
│   └── workflows/
│       └── post.yml
├── resources
│   └── amphib_names.txt
│   └── iteration_numbers.txt
│   └── possible_spp.txt
│   └── sampled_spp.txt
│   └── today_sp.jpg
│   └── today_text.txt
├── README.md
├── requirements.txt
├── init__.py
├── bot.py
├── data_fetcher.py
├── post_generator.py
```


- `__init__.py`: Initializes the module.
- `bot.py`: Main bot logic.
- `data_fetcher.py`: Fetches data from AmphibiaWeb.
- `bsky_post_generator.py.py`: Generates the post content.
- `README.md`: This file.
- `requirements.txt`: Lists the Python dependencies.
- `resources/`: Contains the database and the files that keep track of the species and post informations
- `.github/workflows/`: Contains GitHub Actions workflows.
    - `post.yml`: Workflow file for scheduling posts.


## How It Works

1. **Data Fetching**: The bot fetches data from the AmphibiaWeb dataset using `data_fetcher.py`.
2. **Post Generation**: The fetched data is processed and formatted into a post by `bsky_post_generator.py`.
4. **Scheduling**: The posting schedule is managed by GitHub Actions as defined in `post.yml`.

## Getting Started

To get started with the bot, follow these steps:

1. **Clone the repository**:
     ```sh
     git clone https://github.com/yourusername/AmphibianEveryDay.git
     cd AmphibianEveryDay
     ```

2. **Install dependencies**:
     ```sh
     pip install -r requirements.txt
     ```

3. **Run the bot locally**:
     ```sh
     python3 data_fetcher.py
     python3 bsky_post_generator.py resources/today_text.txt --image today_sp.jpg
     ```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


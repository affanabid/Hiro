from django.core.management.base import BaseCommand, CommandError

from applicants.services.github_scraper import scrape_github_user


class Command(BaseCommand):
    help = "Scrape GitHub repositories and language stats for a user"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="GitHub username to scrape")
        parser.add_argument(
            "--max-repos",
            type=int,
            default=50,
            help="Maximum number of repositories to fetch (default: 50)",
        )
        parser.add_argument(
            "--repo-limit",
            type=int,
            default=30,
            help="Number of most recent repos to inspect for stack labels (default: 30)",
        )
        parser.add_argument(
            "--years",
            type=int,
            default=None,
            help="Limit to repositories pushed in the last N years",
        )
        parser.add_argument(
            "--include-forks",
            action="store_true",
            help="Include forked repositories",
        )

    def handle(self, *args, **options):
        username = options["username"]
        max_repos = options["max_repos"]
        repo_limit = options["repo_limit"]
        years = options["years"]
        include_forks = options["include_forks"]

        try:
            lines = scrape_github_user(
                username=username,
                max_repos=max_repos,
                repo_limit=repo_limit,
                years=years,
                include_forks=include_forks,
            )
        except Exception as exc:  # noqa: BLE001
            raise CommandError(str(exc))

        if not lines:
            self.stdout.write(self.style.WARNING(f"No repositories found for '{username}'"))
            return

        for line in lines:
            self.stdout.write(line)

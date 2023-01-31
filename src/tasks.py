from logzero import logger

from src.app import CELERY
from src.config import CELERYBEAT_SCHEDULE
from src.reddit_scraper import calc_percentiles, praw_memes


@CELERY.task(name=CELERYBEAT_SCHEDULE["reddit"]["task"], unique_on=[], lock_expiry=60 * 60 * 12)
def Reddit():
    logger.info("Reddit Scraper Task Started")
    praw_memes(verbose=False)
    calc_percentiles()

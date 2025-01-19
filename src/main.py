import mlflow
from loguru import logger
from datetime import datetime

from src import settings
from src.dataset import DataLoader

mlflow.set_tracking_uri(settings.TRACKING_URI)
mlflow.set_experiment("Movie Recommendation System")


def main():
    with mlflow.start_run(
        run_name="Train" + "/" + datetime.now().strftime("%Y-%m-%d %H:%M")
    ):
        imdb_urls = ["https://www.imdb.com/title/tt0903747/?ref_=nv_sr_srsg_0_tt_8_nm_0_in_0_q_breaking%2520bad",
                     "https://www.imdb.com/title/tt0066921/?ref_=nv_sr_srsg_1_tt_7_nm_0_in_0_q_%25D0%25B7%25D0%25B0%25D0%25B2%25D0%25BE%25D0%25B4%25D0%25BD%25D0%25BE%25D0%25"]

        for el in imdb_urls:
            DataLoader().example(el)
            logger.info('-----')


if __name__ == "__main__":
    main()

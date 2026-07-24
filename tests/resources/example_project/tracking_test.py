import sys

import MLForge


def call_tracking_apis():
    MLForge.log_metric("some_key", 3)


def main(use_start_run):
    if use_start_run:
        with MLForge.start_run():
            call_tracking_apis()
    else:
        call_tracking_apis()


if __name__ == "__main__":
    main(use_start_run=int(sys.argv[1]))

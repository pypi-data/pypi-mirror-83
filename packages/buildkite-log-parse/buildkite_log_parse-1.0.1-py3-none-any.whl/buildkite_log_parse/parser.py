import argparse
import os


class Parser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Extract string from buildkite job"
        )
        parser.add_argument("--group", help="Regex group index, e.g. 1", type=int)
        parser.add_argument("--organization", help="Organization name, e.g. org-1")
        parser.add_argument("--pipeline", help="Pipeline slug")
        parser.add_argument("--token", help="Buildkite token")
        parser.add_argument("--regex", help="Regex to search in logs")
        parser.add_argument("--build_state", help="Build state, e.g. running")
        parser.add_argument("--build_message", help="Build message")
        parser.add_argument("--job", help="Job name")
        parser.add_argument("--debug", help="Dump response logs", action="store_true")
        self.args = parser.parse_args()

    def group(self):
        if self.args.group is None:
            return os.environ.get("GROUP")
        return self.args.group

    def organization(self):
        return self.args.organization or os.environ["ORGANIZATION"]

    def pipeline(self):
        return self.args.pipeline or os.environ["PIPELINE"]

    def token(self):
        return self.args.token or os.environ["TOKEN"]

    def regex(self):
        return self.args.regex or os.environ["REGEX"]

    def build_message(self):
        return self.args.build_message or os.environ["BUILD_MESSAGE"]

    def build_state(self):
        return self.args.build_state or os.environ["BUILD_STATE"]

    def job(self):
        return self.args.job or os.environ["JOB"]

    def debug(self):
        return self.args.debug or os.environ.get("DEBUG")

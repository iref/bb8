import betamax
import os

record_mode = "all" if os.environ.get("GITLAB_CI") else "once"

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = "tests/cassettes"
    print(record_mode)
    config.default_cassette_options["record_mode"] = record_mode

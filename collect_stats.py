import bitbucket as bb
import config

print("Downloading pull requests for ", config.repo)
prs = bb.download_prs(config.project, config.repo)
bb.pretty_print(prs)

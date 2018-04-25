import bitbucket as bb
import config

print("Downloading pull requests for ", config.repo)


def pretty_print_open_prs():
    prs_response = bb.download_prs(config.project, config.repo)
    bb.pretty_print(prs_response)


def print_all_comments(start_id: int, finish_id: int, user: str):
    for i in range(start_id, finish_id):
        pr = bb.download_pr_all(config.project, config.repo, i)
        activities = pr['values']
        for a in activities:
            un = a['user']['name']
            if un == user:
                if 'comment' in a:
                    print("PR #{}".format(i))
                    print(a['comment']['createdDate'])
                    print(a['comment']['text'])


def record_approve_times(start_id: int, finish_id: int):
    with open(config.repo + '-approves.txt', 'w') as f:
        for i in range(start_id, finish_id):
            pr = bb.download_pr_all(config.project, config.repo, i)
            activities = pr['values']
            print("PR #{}".format(i))
            for a in activities:
                if a['action'] == 'APPROVED':
                    un = a['user']['name']
                    t = a['createdDate']
                    print("{}\t{}\t{}".format(i, un, t))
                    f.write("{},{},{}\n".format(i, un, t))
            print("")

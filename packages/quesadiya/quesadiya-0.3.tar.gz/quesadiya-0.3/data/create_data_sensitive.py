from cscan.network import NetworkInterface

import jsonlines
import os


NUM_SAMPLES = 3


def main():
    network = NetworkInterface.create_connection()
    rows = []
    while len(rows) < NUM_SAMPLES:
        a = network.sample_article()
        s = network.sample_section()
        if (len(a['sections']) > 2) and (s not in a['sections']):
            # get id and body of candidates sections
            candidates = []
            for x in a["sections"]:
                a_sec = network.get_section(x)
                cand = {
                    "candidate_sample_id": str(a_sec["_id"]),
                    "candidate_sample_text": a_sec["body"],
                    "candidate_sample_title": a_sec["title"]
                }
                candidates.append(cand)
            # make a json object
            row = {
                "anchor_sample_id": str(s["_id"]),
                "anchor_sample_text": s["body"],
                "anchor_sample_title": s["title"],
                "candidate_group_id": str(a["_id"]),
                "candidates": candidates
            }
            rows.append(row)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with jsonlines.open(os.path.join(this_dir, "sample.jsonl"), mode="w") as jsonl:
        for r in rows:
            jsonl.write(r)


if __name__ == "__main__":
    main()

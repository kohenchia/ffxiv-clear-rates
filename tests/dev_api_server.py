# stdlib
import logging
from typing import Optional, Dict, List

# 3rd-party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Local
from acrossfc.api import submissions, participation_points
from acrossfc.core.model import Member, PointsCategory
from acrossfc.ext.fflogs_client import FFLOGS_CLIENT
from acrossfc.ext.ddb_client import DDB_CLIENT

LOG_FORMAT = (
    "<TEST API> %(asctime)s.%(msecs)03d [%(levelname)s] %(filename)s:%(lineno)d: %(message)s"
)

if len(logging.getLogger().handlers) == 0:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    LOG = logging.getLogger(__name__)
else:
    LOG = logging.getLogger()


logging.getLogger('uvicorn').setLevel(logging.DEBUG)

app = FastAPI(debug=True)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/submissions")
def get_submissions(tier: str):
    subs = submissions.get_submissions_for_tier(tier)
    return subs


@app.get("/submissions/{uuid}")
def get_submission_by_id(uuid: str):
    sub = DDB_CLIENT.get_submission_by_uuid(uuid)
    return sub


@app.get("/submissions_queue")
def get_submissions_queue():
    queue = submissions.get_submissions_queue()
    return queue


@app.get("/current_submissions_tier")
def get_current_submissions_tier():
    return submissions.get_current_submissions_tier()


@app.get("/ppts/{member_id}")
def get_participation_points(member_id: int, tier: str):
    return DDB_CLIENT.get_member_points(member_id, tier)


@app.get("/ppts_leaderboard")
def get_participation_points_leaderboard(tier: str):
    return participation_points.get_points_leaderboard(tier)


@app.get("/ppts_table")
def get_participation_points_table():
    return [
        {
            'category_id': category.value,
            'name': category.name,
            'description': category.description,
            'constraints': category.constraints,
            'points': category.points
        }
        for category in PointsCategory
    ]


class ReviewSubmissionsBody(BaseModel):
    submission_uuid: str
    points_event_to_approved: Dict[str, bool]
    reviewer_id: int
    notes: Optional[str] = None


@app.post("/review_submission")
def review_submission(body: ReviewSubmissionsBody):
    LOG.info(body)
    return submissions.review_submission(
        body.submission_uuid,
        body.points_event_to_approved,
        body.reviewer_id,
        notes=body.notes
    )


@app.get("/fc_roster")
def fc_roster():
    roster: List[Member] = FFLOGS_CLIENT.get_fc_roster()
    return [
        {
            'member_id': m.fcid,
            'name': m.name,
            'rank': m.rank
        }
        for m in roster
    ]

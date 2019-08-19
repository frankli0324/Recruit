import models


def create_challenge(r):
    challenge = models.Challenge()
    challenge.category = r['category']
    challenge.description = r['description']
    models.db.session.add(challenge)
    models.db.session.commit()
    return challenge.id


def challenge_details(chall_id: int):
    challenge = models.Challenge.query.filter_by(id=chall_id)
    return {
        'author': challenge.author,
        'category': challenge.category,
        'description': challenge.description,
    }


def submit_submission(r, solver):
    challenge = models.Challenge.query.filter_by(id=r['id'])
    if challenge is None:
        return False
    submission = models.Submission()
    submission.challenge_id = r['id']
    submission.solver_id = solver
    models.db.session.add(submission)
    models.db.session.commit()
    return submission.id

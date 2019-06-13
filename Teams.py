import firebase_admin
from firebase_admin import firestore

def get_team_by_id(db, team_id):
    doc_ref = db.document("teams",team_id)
    try:
        return doc_ref.get().to_dict()
    except:
        return None

# returns dictionary, key is the abbreviation to the team
def get_all_teams(db):
    ret = {}
    doc_ref = db.collection("teams").get()
    for doc in doc_ref:
        team = doc.to_dict()
        ret[team["TEAM_ABBREVIATION"]] = team
    return ret

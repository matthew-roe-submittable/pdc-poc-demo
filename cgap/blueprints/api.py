import functools
import json

from flask import (
    Blueprint, g, request, redirect, url_for
)

from cgap.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/organizations/', methods=['GET'])
def getOrganizations():
    db = get_db()
    organizations = db.execute(
        'SELECT * FROM organizations',
    ).fetchall()
    return json.dumps([tuple(organization) for organization in organizations])


@bp.route('/organizations/', methods=['POST'])
def createOrganization():
    query_data = [
        request.form.get('name'),
        request.form.get('mission_statement'),
        request.form.get('website'),
        request.form.get('entity_type'),
        request.form.get('registration_number'),
        request.form.get('address'),
        request.form.get('phone'),
        request.form.get('email'),
        request.form.get('dba_name'),
        request.form.get('ceo_name'),
        request.form.get('ceo_title'),
        request.form.get('ceo_address'),
        request.form.get('operating_budget'),
        request.form.get('is_lobbying'),
        request.form.get('start_date'),
        request.form.get('grant_agreement_signatory'),
        request.form.get('fiscal_end_date'),
    ]
    db = get_db()
    cursor = db.cursor()
    organization = cursor.execute(
        '''
        INSERT INTO organizations
        (
            name,
            mission_statement,
            website,
            entity_type,
            registration_number,
            address,
            phone,
            email,
            dba_name,
            ceo_name,
            ceo_title,
            ceo_address,
            operating_budget,
            is_lobbying,
            start_date,
            grant_agreement_signatory,
            fiscal_end_date
        ) VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        ''',
        query_data,
    )
    db.commit()
    return redirect(url_for(
        'api.getOrganizationById',
        organization_id=cursor.lastrowid
    ))

@bp.route('/organizations/<int:organization_id>', methods=['GET'])
def getOrganizationById(organization_id):
    db = get_db()
    organization = db.execute(
        'SELECT * FROM organizations WHERE id=?',
        [organization_id]
    ).fetchone()
    return json.dumps(tuple(organization))


@bp.route('/organizations/<int:organization_id>', methods=['POST'])
def updateOrganization(organization_id):
    query_data = [
        request.form.get('name'),
        request.form.get('mission_statement'),
        request.form.get('website'),
        request.form.get('entity_type'),
        request.form.get('registration_number'),
        request.form.get('address'),
        request.form.get('phone'),
        request.form.get('email'),
        request.form.get('dba_name'),
        request.form.get('ceo_name'),
        request.form.get('ceo_title'),
        request.form.get('ceo_address'),
        request.form.get('operating_budget'),
        request.form.get('is_lobbying'),
        request.form.get('start_date'),
        request.form.get('grant_agreement_signatory'),
        request.form.get('fiscal_end_date'),
        organization_id,
    ]
    db = get_db()
    organization = db.execute(
        '''
        UPDATE organizations
           SET name=?,
               mission_statement=?,
               website=?,
               entity_type=?,
               registration_number=?,
               address=?,
               phone=?,
               email=?,
               dba_name=?,
               ceo_name=?,
               ceo_title=?,
               ceo_address=?,
               operating_budget=?,
               is_lobbying=?,
               start_date=?,
               grant_agreement_signatory=?,
               fiscal_end_date=?
         WHERE id=?
        ''',
        query_data,
    )
    db.commit()
    return redirect(url_for(
        'api.getOrganizationById',
        organization_id=organization_id
    ))


@bp.route('/proposals/', methods=['GET'])
def getProposals():
    db = get_db()
    proposals = db.execute(
        '''
        SELECT proposals.*,
               organizations.*
          FROM proposals
          JOIN organizations ON (organizations.id = proposals.organization_id)
        ''',
    ).fetchall()
    return json.dumps([tuple(proposal) for proposal in proposals], default=str)


@bp.route('/proposals/<int:proposal_id>', methods=['GET'])
def getProposalById(proposal_id):
    db = get_db()
    proposal = db.execute(
        '''
        SELECT proposals.*,
               organizations.*
          FROM proposals
          JOIN organizations ON (organizations.id = proposals.organization_id)
         WHERE proposals.id=?
        ''',
        [proposal_id]
    ).fetchone()
    return json.dumps(tuple(proposal), default=str)


@bp.route('/proposals/', methods=['POST'])
def createProposal():
    query_data = [
        request.form.get('organization_id'),
        request.form.get('primary_contact_name'),
        request.form.get('requested_budget'),
        request.form.get('investment_start_date'),
        request.form.get('investment_end_date'),
        request.form.get('total_budget'),
        request.form.get('fiscal_sponsor_name'),
        request.form.get('description'),
    ]
    insert_query = '''
    INSERT INTO proposals (
        organization_id,
        primary_contact_name,
        requested_budget,
        investment_start_date,
        investment_end_date,
        total_budget,
        fiscal_sponsor_name,
        description
    ) VALUES (?,?,?,?,?,?,?,?)'''

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(insert_query, query_data)
        db.commit()

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))

    return redirect(url_for(
        'api.getProposalById',
        proposal_id=cursor.lastrowid
    ))

from . import db


def table(name):
    return db.Table(name, db.metadata, autoload=True, autoload_with=db.engine)


def denials_by_race_select(msa_md):
    hmda = table("hmda")

    return db.select([db.func.count().label('total'),
                      db.func.sum(db.case([(hmda.c.action_type == 1, 1)],
                                          else_=0)).label('approval_count'),
                      db.func.sum(db.case([(hmda.c.action_type == 3, 1)],
                                          else_=0)).label('denial_count'),
                      hmda.c.applicant_race_1,
                      hmda.c.loan_purpose]) \
            .where(db.and_(hmda.c.msa_md == msa_md, hmda.c.loan_purpose != 2)) \
            .group_by(hmda.c.applicant_race_1, hmda.c.loan_purpose)


def msas():
    cbsa = table("cbsa")
    select = db.select([cbsa], cbsa.c.parent_code == None)
    return db.session.execute(select).fetchall()


def msa(cbsa_code):
    cbsa = table("cbsa")
    select = db.select([cbsa], cbsa.c.cbsa_code == cbsa_code)
    return db.session.execute(select).fetchone()


def total_when(table, param):
    return db.func.sum(db.case([(param, table.c.total)],
                               else_=0))

def to_float(statement):
    return db.cast(statement, db.FLOAT)


def denial_rates(msa_md):
    hmda = table("hmda")
    race = table("race")
    loan_purpose = table("loan_purpose")
    denials_by_race = denials_by_race_select(msa_md).cte("denials_by_race")

    join = db.join(denials_by_race, race,
                   denials_by_race.c.applicant_race_1 == race.c.id) \
             .join(loan_purpose, denials_by_race.c.loan_purpose == loan_purpose.c.id)

    query = db.select([denials_by_race.c.total,
                       denials_by_race.c.approval_count,
                       denials_by_race.c.denial_count,
                       (to_float(denials_by_race.c.denial_count) /
                        to_float(denials_by_race.c.total) *
                        100).label('denial_rate'),
                       race.c.race,
                       loan_purpose.c.loan_purpose]) \
             .select_from(join) \
             .order_by(race.c.race,
                       loan_purpose.c.loan_purpose)

    return db.session.execute(query).fetchall()


def denial_by_income(msa_md=None):
    agg = table("v_hmda_agg_1")
    race = table("race")
    total_denied = total_when(agg, agg.c.action_type_denied == 1)
    join = db.join(agg, race, agg.c.applicant_race_1 == race.c.id)

    query = db.select([db.func.sum(agg.c.total).label("total"),
                       total_denied.label("total_denied"),
                       (to_float(total_denied) /
                        to_float(db.func.sum(agg.c.total)) * 100).label('denial_percent'),
                       race.c.race,
                       agg.c.income_group])

    if msa_md:
        query = query.where(agg.c.msa_md == msa_md)

    query = query.select_from(join) \
                 .group_by(race.c.race, agg.c.income_group) \
                 .order_by(race.c.race, agg.c.income_group)
                      
    return db.session.execute(query).fetchall()


def hal_gov_backed_by_income(msa_md=None):
    agg = table("v_hmda_agg_1")
    total = db.func.sum(agg.c.total)
    total_hal = total_when(agg, agg.c.is_hal == 1)
    total_gov_backed = total_when(agg, agg.c.is_gov_backed == 1)

    query = db.select([total.label("total"),
                       agg.c.income_group,
                       total_hal.label("total_hal"),
                       total_gov_backed.label("total_gov_backed"),
                       (to_float(total_hal) /
                        to_float(total) * 100).label("is_hal_percent"),
                       (to_float(total_gov_backed) /
                        to_float(total) * 100).label("is_gov_backed_percent")]) \
              .where(agg.c.action_type_approved == 1)

    if msa_md:
        query = query.where(agg.c.msa_md == msa_md)

    query = query.group_by(agg.c.income_group).order_by(agg.c.income_group)
    
    return db.session.execute(query).fetchall()


def hal_gov_backed_by_race(msa_md=None):
    agg = table("v_hmda_agg_1")
    total = db.func.sum(agg.c.total)
    race = table("race")
    total_hal = total_when(agg, agg.c.is_hal == 1)
    total_gov_backed = total_when(agg, agg.c.is_gov_backed == 1)
    join = db.join(agg, race, agg.c.applicant_race_1 == race.c.id)

    query = db.select([total,
                       race.c.race,
                       total_hal.label("total_hal"),
                       total_gov_backed.label("total_gov_backed"),
                       (to_float(total_hal) /
                        to_float(total) * 100).label("is_hal_percent"),
                       (to_float(total_gov_backed) /
                        to_float(total) * 100).label("is_gov_backed_percent")]) \
              .select_from(join) \
              .where(agg.c.action_type_approved == 1)              
    
    if msa_md:
        query = query.where(agg.c.msa_md == msa_md)

    query = query.group_by(race.c.race).order_by(race.c.race)
        
    return db.session.execute(query).fetchall()


def gov_backed_by_race_purpose(msa_md=None):
    agg = table("v_hmda_agg_1")
    total = db.func.sum(agg.c.total)
    total_gov_backed = db.func.sum(agg.c.is_gov_backed)
    race = table("race")
    join = db.join(agg, race, agg.c.applicant_race_1 == race.c.id)

    query = db.select([total.label("total"),
                       db.case([(agg.c.loan_purpose == 1, "purchase")],
                               else_='refinance').label("loan_purpose_name"),
                       race.c.race,
                       total_gov_backed.label("total_gov_backed"),
                       (to_float(total_gov_backed) /
                        to_float(total) * 100).label("is_gov_backed_percent")]) \
              .select_from(join) \
              .where(agg.c.action_type_approved == 1) \
              .where(agg.c.loan_purpose != 2)

    if msa_md:
        query = query.where(agg.c.msa_md == msa_md)

    query = query.group_by(race.c.race, agg.c.loan_purpose) \
                 .order_by(race.c.race, agg.c.loan_purpose)
            
    return db.session.execute(query).fetchall()


def gov_backed_by_income_purpose(msa_md=None):
    agg = table("v_hmda_agg_1")
    total = db.func.sum(agg.c.total)
    total_gov_backed = total_when(agg, agg.c.is_gov_backed == 1)

    query = db.select([total.label("total"),
                       db.case([(agg.c.loan_purpose == 1, "purchase")],
                               else_='refinance').label("loan_purpose_name"),
                       agg.c.income_group,
                       total_gov_backed.label("total_gov_backed"),
                       (to_float(total_gov_backed) /
                        to_float(total) * 100).label("is_gov_backed_percent")]) \
              .where(agg.c.action_type_approved == 1) \
              .where(agg.c.loan_purpose != 2)

    if msa_md:
        query = query.where(agg.c.msa_md == msa_md)

    query = query.group_by(agg.c.income_group, agg.c.loan_purpose) \
                 .order_by(agg.c.income_group, agg.c.loan_purpose)

    return db.session.execute(query).fetchall()

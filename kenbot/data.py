from . import db


def table(name):
    return db.Table(name, db.metadata, autoload=True, autoload_with=db.engine)


def denials_by_race_select(msa_md):
    hmda = table("hmda")

    return db.select([db.func.count().label('total'),
                      db.func.sum(db.case([(hmda.c.action_type == 1, 1)],
                                          else_=0)).label(
                      'approval_count'),
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
                       (db.cast(denials_by_race.c.denial_count, db.FLOAT) /
                        db.cast(denials_by_race.c.total, db.FLOAT) *
                        100).label('denial_rate'),
                       race.c.race,
                       loan_purpose.c.loan_purpose]) \
             .select_from(join) \
             .order_by(race.c.race,
                       loan_purpose.c.loan_purpose)

    return db.session.execute(query).fetchall()


def denial_by_income(msa_md=None):
    sql = """
        select sum(total) as total,
               sum(case when action_type_denied = 1 then total else 0 end) as total_denied,
               cast(sum(case when action_type_denied = 1
                             then total
                             else 0 end) as float) / cast(sum(total) as float) * 100 as denial_percent,
               r.race,
               income_group
        from v_hmda_agg_1 v
        join race r on v.applicant_race_1 = r.id
      """
    if msa_md:
        sql = sql + "where msa_md = :msa_md"
    sql = sql + """
        group by r.race, income_group
        order by r.race, income_group
    """

    return db.session.execute(sql, params={'msa_md': msa_md}).fetchall()


def hal_gov_backed_by_income(msa_md=None):
    sql = """
        select sum(total) as total,
               income_group,
               sum(case when is_hal = 1 then total else 0 end) as total_hal,
               sum(case when is_gov_backed = 1 then total else 0 end) as total_gov_backed,
               cast(sum(case when is_hal = 1
                             then total
                             else 0 end) as float) / cast(sum(total) as float) * 100 as is_hal_percent,
               cast(sum(case when is_gov_backed = 1
                             then total
                             else 0 end) as float) / cast(sum(total) as float) * 100 as is_gov_backed_percent
        from v_hmda_agg_1 v
        where action_type_approved = 1
    """
    if msa_md:
        sql = sql + "and msa_md = :msa_md"
    sql = sql + """
        group by income_group
        order by income_group
    """
    return db.session.execute(sql, params={'msa_md': msa_md}).fetchall()


def hal_gov_backed_by_race(msa_md=None):
    sql = """
        select sum(total) as total,
               r.race,
               sum(case when is_hal = 1 then total else 0 end) as total_hal,
               sum(case when is_gov_backed = 1 then total else 0 end) as total_gov_backed,
               cast(sum(case when is_hal = 1
                             then total
                             else 0 end) as float) / cast(sum(total) as float) * 100 as is_hal_percent,
               cast(sum(case when is_gov_backed = 1
                             then total
                             else 0 end) as float) / cast(sum(total) as float) * 100 as is_gov_backed_percent
        from v_hmda_agg_1 v
        join race r on v.applicant_race_1 = r.id
        where action_type_approved = 1
    """
    if msa_md:
        sql = sql + " and msa_md = :msa_md"
    sql = sql + """
        group by  r.race
        order by  r.race
    """
    return db.session.execute(sql, params={'msa_md': msa_md}).fetchall()


def gov_backed_by_race_purpose(msa_md=None):
    sql = """
        select sum(total) as total,
               case when loan_purpose = 1 then 'purchase' else 'refinance' end as loan_purpose_name,
               r.race,
               sum(is_gov_backed) as total_gov_backed,
               cast(sum(is_gov_backed) as float) / cast(sum(total) as float) * 100 as is_gov_backed_percent
        from v_hmda_agg_1 v
        join race r on v.applicant_race_1 = r.id
        where action_type_approved = 1 and v.loan_purpose != 2
    """
    if msa_md:
        sql = sql + " and msa_md = :msa_md"
    sql = sql + """
        group by r.race, loan_purpose
        order by r.race, loan_purpose
    """
    return db.session.execute(sql, params={'msa_md': msa_md}).fetchall()


def gov_backed_by_income_purpose(msa_md=None):
    sql = """
        select sum(total) as total,
               case when loan_purpose = 1 then 'purchase' else 'refinance' end as loan_purpose_name,
               income_group,
               sum(case when is_gov_backed = 1 then total else 0 end) as total_gov_backed,
               cast(sum(case when is_gov_backed = 1
                             then total
                             else 0 end) as float) / cast(sum(total) as float) * 100 as is_gov_backed_percent
        from v_hmda_agg_1 v
        where action_type_approved = 1 and v.loan_purpose != 2
    """
    if msa_md:
        sql = sql + " and msa_md = :msa_md"
    sql = sql + """
        group by income_group,  loan_purpose
        order by income_group,  loan_purpose
    """
    return db.session.execute(sql, params={'msa_md': msa_md}).fetchall()

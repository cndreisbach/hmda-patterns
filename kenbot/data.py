from . import db

def msas():
    res = db.execute("SELECT cbsa_code, name FROM cbsa WHERE parent_code IS NULL")
    return res.fetchall()

def denial_rates(msa_md=None):
    sql = """with denials_by_race as (
                select count(*) as total
                    ,sum(case when action_type = 1 then 1 else 0 end) as approval_count
                    ,sum(case when action_type = 3 then 1 else 0 end) as denial_count
                    , applicant_race_1, loan_purpose
                from hmda
                where  msa_md = :msa_md
                    and applicant_race_1 < 6
                    and loan_purpose != 2
                group by applicant_race_1, loan_purpose
        )

        select total, approval_count, denial_count
        , cast(denial_count as float) / cast(total as float) * 100 as denial_rate
        , r.race, lp.loan_purpose
        from denials_by_race d
        join race r on d.applicant_race_1 = r.id
        join loan_purpose lp on d.loan_purpose = lp.id
        order by loan_purpose, race"""

    return db.execute(sql, params={'msa_md':msa_md}).fetchall()

def denial_by_income(msa_md=None):
    sql = """
        select sum(total) as total, sum(case when action_type_denied = 1 then total else 0 end) as total_denied,
            cast(sum(case when action_type_denied = 1 then total else 0 end) as float) / cast(sum(total) as float) * 100 as denial_percent
            , r.race, income_group
        from v_hmda_agg_1 v
        join race r on v.applicant_race_1 = r.id
      """
    if msa_md:
        sql = sql + "where msa_md = :msa_md"
    sql = sql + """
        group by r.race, income_group
        order by r.race, income_group
    """

    return db.execute(sql, params={'msa_md':msa_md}).fetchall()

def hal_gov_backed_by_income(msa_md=None):
    sql = """
        select sum(total) as total, income_group
        , sum(case when is_hal = 1 then total else 0 end) as total_hal, sum(case when is_gov_backed = 1 then total else 0 end) as total_gov_backed
        ,cast(sum(case when is_hal = 1 then total else 0 end) as float) / cast(sum(total) as float) * 100 as is_hal_percent
        ,cast(sum(case when is_gov_backed = 1 then total else 0 end) as float) / cast(sum(total) as float) * 100 as is_gov_backed_percent
        from v_hmda_agg_1 v
        where action_type_approved = 1
    """
    if msa_md:
        sql = sql + "and msa_md = :msa_md"
    sql = sql + """
        group by  income_group
        order by  income_group
    """
    return db.execute(sql, params={'msa_md':msa_md}).fetchall()

def hal_gov_backed_by_race(msa_md=None):
    sql = """
        select sum(total) as total, r.race
            ,sum(case when is_hal = 1 then total else 0 end) as total_hal, sum(case when is_gov_backed = 1 then total else 0 end) as total_gov_backed
            ,cast(sum(case when is_hal = 1 then total else 0 end) as float) / cast(sum(total) as float) * 100 as is_hal_percent
            ,cast(sum(case when is_gov_backed = 1 then total else 0 end) as float) / cast(sum(total) as float) * 100 as is_gov_backed_percent
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
    return db.execute(sql, params={'msa_md':msa_md}).fetchall()

def gov_backed_by_race_purpose(msa_md=None):
    sql = """
        select sum(total) as total, case when loan_purpose = 1 then 'purchase' else 'refinance' end as loan_purpose_name, r.race
            ,sum(is_gov_backed) as total_gov_backed
            ,cast(sum(is_gov_backed) as float) / cast(sum(total) as float) * 100 as is_gov_backed_percent
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
    return db.execute(sql, params={'msa_md':msa_md}).fetchall()

def gov_backed_by_income_purpose(msa_md=None):
    sql = """
        select sum(total) as total, case when loan_purpose = 1 then 'purchase' else 'refinance' end as loan_purpose_name, income_group
         ,sum(case when is_gov_backed = 1 then total else 0 end) as total_gov_backed
        ,cast(sum(case when is_gov_backed = 1 then total else 0 end) as float) / cast(sum(total) as float) * 100 as is_gov_backed_percent
        from v_hmda_agg_1 v
        where action_type_approved = 1 and v.loan_purpose != 2
    """
    if msa_md:
        sql = sql + " and msa_md = :msa_md"
    sql = sql + """
        group by income_group,  loan_purpose
        order by income_group,  loan_purpose
    """
    return db.execute(sql, params={'msa_md':msa_md}).fetchall()
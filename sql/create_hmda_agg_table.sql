-- quick stab at a view to do some common aggregations. Obviously this is just a starting point
DROP TABLE IF EXISTS v_hmda_agg_1;

with raw as (
  select msa_md, state_code, county_code, applicant_race_1, year, applicant_ethnicity
  , loan_purpose
  , case when loan_type != 1 then 1 else 0 end as is_gov_backed
  , case when rate_spread is null then 0 else 1 end as is_hal
  , case when occupancy = 1 then 1 else 0 end as is_owner_occupied
  , case when action_type = 3 then 1 else 0 end as action_type_denied
  , case when action_type = 1 then 1 else 0 end as action_type_approved
  , case when action_type in(1,3) then 0 else 1 end as action_type_other
  , cast(case
         when applicant_income < 300
         then ceil(applicant_income / 30.0) * 30
         else 300 end as int) as income_group
  from hmda
)
,
v1 as (
select cast(count(*) as int) as total, *
  from raw
group by msa_md, state_code, county_code, applicant_race_1, year, applicant_ethnicity
  , loan_purpose
  , is_gov_backed, is_hal, is_owner_occupied, income_group
  , action_type_approved, action_type_denied, action_type_other
)

select * into v_hmda_agg_1 from v1;

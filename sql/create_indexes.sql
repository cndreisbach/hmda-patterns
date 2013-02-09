create index on hmda(applicant_ethnicity);

create index on hmda(loan_amount);

create index on hmda(msa_md);

create index on hmda(occupancy);

create index on hmda(year);

create index on hmda(rate_spread);

create index on hmda(applicant_race_1, applicant_race_2, applicant_race_3, applicant_race_4, applicant_race_5);

create index on hmda(co_applicant_race_1, co_applicant_race_2, co_applicant_race_3, co_applicant_race_4, co_applicant_race_5);

create index on hmda(denial_reason_1, denial_reason_2, denial_reason_3);

create index on hmda(applicant_sex, co_applicant_sex);

create index on hmda(applicant_income);

create index on hmda(loan_amount);

create index on hmda(msa_md, state_code, county_code, census_tract_number);
